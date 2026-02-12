# Linux Setup Guide for MxAI WiFi Tool

**Developed by Manoj Kumar**  
**Instagram**: [@_golu_.650](https://www.instagram.com/_golu_.650/)

---

## Quick Setup

### 1. Install Dependencies

```bash
# Ubuntu/Debian/Kali
sudo apt-get update
sudo apt-get install -y aircrack-ng wireless-tools python3

# Arch Linux
sudo pacman -S aircrack-ng wireless_tools python

# Fedora/RHEL
sudo yum install -y aircrack-ng wireless-tools python3
```

### 2. Verify Installation

```bash
# Check if aircrack-ng is installed
which airmon-ng
which airodump-ng
which aireplay-ng
which aircrack-ng

# Check if wireless-tools is installed
which iwconfig
```

### 3. Check WiFi Interface

```bash
# List all network interfaces
iwconfig

# You should see your WiFi interface (usually wlan0, wlan1, etc.)
```

---

## Troubleshooting Monitor Mode

### Issue: "FAILED: Failed to enable monitor mode"

This means airmon-ng couldn't enable monitor mode. Here's how to fix it:

### Solution 1: Kill Interfering Processes

```bash
# Kill processes that might interfere
sudo airmon-ng check kill

# Then try enabling monitor mode manually
sudo airmon-ng start wlan0
```

### Solution 2: Check if Adapter Supports Monitor Mode

```bash
# Check adapter capabilities
iw list | grep -A 10 "Supported interface modes"

# You should see "monitor" in the list
```

### Solution 3: Manual Monitor Mode

If airmon-ng doesn't work, try manual method:

```bash
# Stop network manager
sudo systemctl stop NetworkManager

# Bring interface down
sudo ip link set wlan0 down

# Set monitor mode
sudo iw wlan0 set monitor control

# Bring interface up
sudo ip link set wlan0 up

# Verify
iwconfig wlan0
# Should show "Mode:Monitor"
```

### Solution 4: Check for Driver Issues

```bash
# Check current driver
lsmod | grep -i wifi
lsmod | grep -i 80211

# Some adapters need specific drivers
# For Realtek adapters:
sudo apt-get install realtek-rtl88xxau-dkms

# For other adapters, search for your specific chipset
```

---

## Compatible WiFi Adapters

### Recommended Adapters for Monitor Mode:

1. **Alfa AWUS036NHA** (Best choice)
   - Chipset: Atheros AR9271
   - Excellent Linux support
   - Built-in monitor mode

2. **TP-Link TL-WN722N v1** (Budget option)
   - Chipset: Atheros AR9271
   - Good compatibility
   - **Note**: Only v1 works! v2 and v3 don't support monitor mode

3. **Panda PAU09**
   - Chipset: Ralink RT5372
   - Good Linux support

4. **Alfa AWUS036ACH**
   - Chipset: Realtek RTL8812AU
   - Dual-band support
   - May need driver installation

### Check Your Adapter:

```bash
# Find your adapter chipset
lsusb

# Get detailed info
lsusb -v | grep -i wireless
```

---

## Running the Tool

### Method 1: With sudo (Recommended)

```bash
sudo python3 wifi_tool.py
```

### Method 2: As root

```bash
sudo su
python3 wifi_tool.py
```

### Method 3: Add to sudoers (Advanced)

```bash
# Edit sudoers file
sudo visudo

# Add this line (replace 'username' with your username):
username ALL=(ALL) NOPASSWD: /usr/bin/python3 /path/to/wifi_tool.py
```

---

## Testing Monitor Mode

### Test 1: Check if airmon-ng works

```bash
# Start monitor mode
sudo airmon-ng start wlan0

# Check if wlan0mon was created
iwconfig

# You should see wlan0mon in Mode:Monitor

# Stop monitor mode
sudo airmon-ng stop wlan0mon
```

### Test 2: Scan for networks

```bash
# Enable monitor mode
sudo airmon-ng start wlan0

# Scan for networks (Ctrl+C to stop)
sudo airodump-ng wlan0mon

# You should see networks being detected

# Stop monitor mode
sudo airmon-ng stop wlan0mon
```

---

## Common Issues and Solutions

### Issue 1: "No WiFi interfaces found"

**Solution:**
```bash
# Check if interface is up
sudo ip link set wlan0 up

# Restart network manager
sudo systemctl restart NetworkManager

# Check again
iwconfig
```

### Issue 2: "Operation not permitted"

**Solution:**
```bash
# Run with sudo
sudo python3 wifi_tool.py

# Or become root
sudo su
python3 wifi_tool.py
```

### Issue 3: "Device or resource busy"

**Solution:**
```bash
# Kill interfering processes
sudo airmon-ng check kill

# Restart network manager after testing
sudo systemctl start NetworkManager
```

### Issue 4: "Monitor mode not supported"

**Solution:**
- Your WiFi adapter doesn't support monitor mode
- Buy a compatible adapter (see recommendations above)
- Or use a USB WiFi adapter that supports monitor mode

---

## Kali Linux Specific

If you're using Kali Linux, everything should work out of the box:

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade

# Install if missing
sudo apt-get install aircrack-ng

# Run tool
sudo python3 wifi_tool.py
```

---

## Virtual Machine Users

If you're running Linux in a VM (VirtualBox, VMware):

### Important Notes:
- USB WiFi adapters work better than built-in WiFi
- You need to pass through the USB device to the VM
- Some adapters don't work well in VMs

### VirtualBox Setup:
1. Install VirtualBox Extension Pack
2. Plug in USB WiFi adapter
3. In VM settings: USB → Add USB Device Filter
4. Select your WiFi adapter
5. Start VM and the adapter should be available

### VMware Setup:
1. Plug in USB WiFi adapter
2. VM → Removable Devices → Your WiFi Adapter → Connect
3. Adapter should now be available in the VM

---

## Verification Checklist

Before using the tool, verify:

- [ ] aircrack-ng installed: `which airmon-ng`
- [ ] wireless-tools installed: `which iwconfig`
- [ ] Python 3 installed: `python3 --version`
- [ ] WiFi adapter detected: `iwconfig`
- [ ] Running as root: `whoami` (should show "root")
- [ ] Monitor mode works: `sudo airmon-ng start wlan0`

---

## Getting Help

If you still have issues:

1. Check system logs:
   ```bash
   dmesg | tail -50
   journalctl -xe
   ```

2. Check airmon-ng output:
   ```bash
   sudo airmon-ng start wlan0
   # Read the output carefully for errors
   ```

3. Search for your specific adapter:
   ```bash
   lsusb
   # Google: "your adapter name + monitor mode linux"
   ```

4. Contact developer:
   - Instagram: [@_golu_.650](https://www.instagram.com/_golu_.650/)

---

## Additional Resources

- Aircrack-ng Documentation: https://www.aircrack-ng.org/
- Kali Linux WiFi Guide: https://www.kali.org/docs/
- Compatible Adapters List: https://github.com/morrownr/USB-WiFi

---

**Developed by Manoj Kumar**  
**Instagram**: [@_golu_.650](https://www.instagram.com/_golu_.650/)

**Use responsibly and legally!**
