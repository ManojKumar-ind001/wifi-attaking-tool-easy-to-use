# MxAI WiFi Tool - Usage Guide

**Developed by Manoj Kumar**  
**Instagram**: [@_golu_.650](https://www.instagram.com/_golu_.650/)

---

## Quick Start

```bash
# Windows
python wifi_tool.py

# Linux (for full features)
sudo python3 wifi_tool.py
```

---

## Main Menu

When you start the tool, you'll see:

```
============================================================
Starting MxAI WiFi Tool...
Developed by Manoj Kumar
Instagram: @_golu_.650
============================================================

        ╔══════════════════════════════════════════════════════════╗
        ║                    MxAI WiFi Tool v1.0                   ║
        ║                 Developed by Manoj Kumar                 ║
        ║         Cross-platform WiFi Security Assessment          ║
        ╚══════════════════════════════════════════════════════════╝

Checking dependencies...

============================================================
=== MxAI WiFi Tool - Main Menu ===
============================================================
1. Auto-detect WiFi interface
2. Scan all nearby networks
3. Select target network
4. Choose attack type
5. Manual mode
6. Monitor mode toggle (Linux only)
7. Exit
============================================================
```

---

## Option 1: Auto-detect WiFi Interface

### What it does:
- Detects all available WiFi adapters
- Lets you select which one to use
- Configures wordlist for attacks

### Steps:
1. Select option `1`
2. Choose your WiFi interface from the list
3. Select wordlist option:
   - `1` - Use default wordlist (1019 passwords)
   - `2` - Use custom wordlist (provide file path)
   - `3` - Back to menu

### Example:
```
Select option (1-7): 1

============================================================
=== WiFi Interface Detection ===
============================================================

Detecting WiFi interfaces...
Found interfaces: Wi-Fi 2, Wi-Fi

Select WiFi interface:
1. Wi-Fi 2
2. Wi-Fi
Enter number: 1
Selected: Wi-Fi 2

------------------------------------------------------------
=== Wordlist Selection ===
------------------------------------------------------------
1. Use default wordlist
2. Use custom wordlist
3. Back to menu

Select wordlist option (1-3): 1

Generating default wordlist...
Wordlist generated: mxai_wordlist.txt
Total passwords: 1019

Interface and wordlist configured successfully!
```

---

## Option 2: Scan All Nearby Networks

### What it does:
- Scans for WiFi networks in range
- Shows network details (ESSID, BSSID, Channel, Encryption)
- Lets you select a target for attack

### Requirements:
- Must run Option 1 first to select interface

### Steps:
1. Select option `2`
2. Wait for scan to complete (10-15 seconds)
3. View list of networks
4. Choose:
   - `1` - Select a target network for attack
   - `2` - Back to menu

### Example:
```
Select option (1-7): 2

============================================================
=== Network Scanning ===
============================================================

Scanning for nearby WiFi networks...
This may take 10-15 seconds...

Found 5 network(s) in range:
============================================================
1. HomeWiFi
   BSSID: AA:BB:CC:DD:EE:FF
   Channel: 6 | Encryption: WPA2-Personal
------------------------------------------------------------
2. Office_Network
   BSSID: 11:22:33:44:55:66
   Channel: 11 | Encryption: WPA2-Personal
------------------------------------------------------------
...

Options:
1. Select a target network for attack
2. Back to menu

Select option (1-2): 1

Select target network (1-5): 1

============================================================
=== Target Selected ===
============================================================
Network: HomeWiFi
BSSID: AA:BB:CC:DD:EE:FF
Channel: 6
Encryption: WPA2-Personal
============================================================
```

---

## Attack Types

After selecting a target, you'll see:

```
============================================================
=== Select Attack Type ===
============================================================
1. Deauthentication Attack (Disconnect devices)
2. Password Attack (Capture & Crack handshake)
3. Both attacks (Combined)
4. Back to menu
============================================================
```

### Attack 1: Deauthentication Attack

**What it does:**
- Sends deauth packets to disconnect devices from the network
- Forces devices to reconnect
- Can target specific device or all devices (broadcast)

**Requirements:**
- Linux system
- Monitor mode support
- Root privileges

**Steps:**
1. Select attack option `1`
2. Enter client MAC (or press Enter for broadcast)
3. Enter number of packets (default: 10)
4. Attack executes automatically

**Example:**
```
Select attack (1-4): 1

============================================================
=== Deauthentication Attack ===
============================================================
Target: HomeWiFi

Enter specific client MAC (or press Enter for broadcast): 
Using broadcast MAC (will disconnect all devices)
Number of deauth packets (default 10): 20

Enabling monitor mode...
Sending 20 deauth packets...
SUCCESS: Deauth attack completed! Sent 20 packets.
Devices should be disconnected from the network.

Disabling monitor mode...

Press Enter to continue...
```

---

### Attack 2: Password Attack

**What it does:**
- Captures WPA/WPA2 handshake when device connects
- Cracks the password using wordlist
- Shows password if found

**Requirements:**
- Linux system
- Monitor mode support
- Root privileges
- Wordlist configured

**Steps:**
1. Select attack option `2`
2. Confirm to start capture
3. Wait for handshake capture (30 seconds)
4. Password cracking starts automatically
5. View results

**Example:**
```
Select attack (1-4): 2

============================================================
=== Password Attack ===
============================================================
Target: HomeWiFi
This will capture handshake and attempt to crack password.

Enabling monitor mode...
Monitor mode enabled

Capturing handshake on channel 6...
Tip: You need to wait for a device to connect to the network.
     Or trigger connection by running deauth attack first.

Start capture? (y/n): y

Capturing... (This will take about 30 seconds)
SUCCESS: Handshake captured: handshake_AABBCCDDEEFF.cap

Starting password cracking...
Using wordlist: mxai_wordlist.txt
This may take several minutes...

SUCCESS! Password found: password123
Network: HomeWiFi
Password: password123

Disabling monitor mode...
Monitor mode disabled

Press Enter to continue...
```

---

### Attack 3: Combined Attack

**What it does:**
- Runs deauth attack to force reconnection
- Captures handshake automatically
- Cracks password immediately
- Fully automated process

**Requirements:**
- Linux system
- Monitor mode support
- Root privileges
- Wordlist configured

**Example:**
```
Select attack (1-4): 3

============================================================
=== Combined Attack ===
============================================================
Target: HomeWiFi

Enabling monitor mode...

Step 1: Deauth attack to trigger handshake...
Deauth packets sent. Waiting for reconnection...

Step 2: Capturing handshake...
SUCCESS: Handshake captured: handshake_AABBCCDDEEFF.cap

Step 3: Cracking password...
Using wordlist: mxai_wordlist.txt
SUCCESS! Password: password123
Network: HomeWiFi
Password: password123

Disabling monitor mode...

Press Enter to continue...
```

---

## Option 3: Manual Target Selection

### What it does:
- Manually enter target network details
- Useful when you know the target information

### Steps:
1. Select option `3`
2. Enter BSSID (MAC address)
3. Enter ESSID (network name)
4. Enter channel number
5. Select attack type

---

## Option 4: Choose Attack Type

### What it does:
- Quick access to attack type selection
- Requires running Option 2 first

---

## Option 5: Manual Mode

### What it does:
- Advanced options for manual control
- Individual tools access

### Sub-options:
1. Detect WiFi interfaces
2. Scan networks
3. Generate wordlist
4. Deauth attack
5. Capture handshake
6. Crack password
7. Back to main menu

---

## Option 6: Monitor Mode Toggle (Linux Only)

### What it does:
- Manually enable/disable monitor mode
- Useful for troubleshooting

### Steps:
1. Select option `6`
2. Choose:
   - `1` - Enable monitor mode
   - `2` - Disable monitor mode
   - `3` - Back to menu

### Example:
```
Select option (1-7): 6

============================================================
=== Monitor Mode Toggle (Linux Only) ===
============================================================
Current interface: wlan0

1. Enable monitor mode
2. Disable monitor mode
3. Back to menu

Select: 1

Enabling monitor mode...
SUCCESS: Monitor mode enabled
Interface: wlan0mon

Press Enter to continue...
```

---

## Tips & Best Practices

### For Best Results:
1. **Use Linux** - Full features require Linux
2. **Compatible Adapter** - Use Alfa AWUS036NHA or similar
3. **Run as Root** - Use `sudo` on Linux
4. **Wait for Handshake** - Be patient during capture
5. **Good Wordlist** - Use comprehensive wordlists

### Troubleshooting:

**"No WiFi interfaces found"**
- Check if WiFi is enabled
- Install wireless-tools on Linux
- Verify adapter is connected

**"Password attack requires Linux"**
- You're on Windows
- Use Linux for full features
- Or use deauth attack only

**"Failed to enable monitor mode"**
- Install aircrack-ng: `sudo apt-get install aircrack-ng`
- Run with sudo: `sudo python3 wifi_tool.py`
- Check if adapter supports monitor mode

**"Password not found in wordlist"**
- Password not in the wordlist
- Generate larger wordlist
- Use custom wordlist with more passwords

---

## Wordlist Management

### Default Wordlist:
- Auto-generated
- 1019 common passwords
- Includes variations with numbers, years, special characters

### Custom Wordlist:
- Provide your own file path
- Must be text file with one password per line
- Can be any size

### Generating Custom Wordlist:
1. Go to Manual Mode (option 5)
2. Select "Generate wordlist" (option 3)
3. Enter base words (comma separated)
4. Wordlist will be generated

---

## Legal & Ethical Use

### ⚠️ IMPORTANT:

**Only use on networks you own or have permission to test!**

### Legal Requirements:
- ✅ Own the network
- ✅ Have written permission
- ✅ Educational purposes
- ✅ Authorized security testing

### Prohibited:
- ❌ Unauthorized access
- ❌ Malicious use
- ❌ Illegal activities
- ❌ Network disruption without permission

---

## Support

For help:
- Check [README.md](README.md)
- See [INSTALL.md](INSTALL.md)
- Contact: [@_golu_.650](https://www.instagram.com/_golu_.650/) on Instagram

---

**Developed by Manoj Kumar**  
**Instagram**: [@_golu_.650](https://www.instagram.com/_golu_.650/)

**Use responsibly and legally!**
