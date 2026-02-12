# MxAI WiFi Tool - Installation Guide

Developed by **Manoj Kumar**  
Instagram: [@_golu_.650](https://www.instagram.com/_golu_.650/)

---

## Quick Installation

### Windows

1. **Install Python** (if not already installed)
   - Download from: https://www.python.org/downloads/
   - Version 3.6 or higher required
   - During installation, check "Add Python to PATH"

2. **Download MxAI WiFi Tool**
   ```bash
   # Download and extract the tool
   cd Downloads
   cd mxai-wifi-tool
   ```

3. **Run the Tool**
   ```bash
   python wifi_tool.py
   ```

That's it! No additional packages needed on Windows.

---

### Linux (Ubuntu/Debian)

1. **Install Python and Dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install python3 aircrack-ng wireless-tools
   ```

2. **Download MxAI WiFi Tool**
   ```bash
   cd ~/Downloads
   cd mxai-wifi-tool
   ```

3. **Make Script Executable** (optional)
   ```bash
   chmod +x wifi_tool.py
   ```

4. **Run the Tool**
   ```bash
   sudo python3 wifi_tool.py
   ```

---

### Linux (Arch)

1. **Install Dependencies**
   ```bash
   sudo pacman -S python aircrack-ng wireless_tools
   ```

2. **Download and Run**
   ```bash
   cd ~/Downloads/mxai-wifi-tool
   sudo python3 wifi_tool.py
   ```

---

### Linux (Fedora/RHEL)

1. **Install Dependencies**
   ```bash
   sudo yum install python3 aircrack-ng wireless-tools
   ```

2. **Download and Run**
   ```bash
   cd ~/Downloads/mxai-wifi-tool
   sudo python3 wifi_tool.py
   ```

---

## Verification

After installation, verify the tool works:

```bash
python wifi_tool.py
```

You should see:
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
```

---

## Troubleshooting

### "Python not found"
- **Windows**: Reinstall Python and check "Add to PATH"
- **Linux**: Install with `sudo apt-get install python3`

### "aircrack-ng not found" (Linux)
```bash
sudo apt-get install aircrack-ng
```

### "Permission denied" (Linux)
Run with sudo:
```bash
sudo python3 wifi_tool.py
```

### "No WiFi interfaces found"
- Check if WiFi is enabled
- On Linux, install wireless-tools: `sudo apt-get install wireless-tools`
- Verify WiFi adapter is connected

---

## WiFi Adapter Setup (Linux)

For full features, you need a WiFi adapter that supports monitor mode.

### Recommended Adapters
- Alfa AWUS036NHA
- TP-Link TL-WN722N v1
- Panda PAU09

### Check Monitor Mode Support
```bash
sudo airmon-ng
```

### Enable Monitor Mode Manually
```bash
sudo airmon-ng start wlan0
```

### Disable Monitor Mode
```bash
sudo airmon-ng stop wlan0mon
```

---

## File Structure

After installation, you should have:
```
mxai-wifi-tool/
├── wifi_tool.py          # Main tool
├── requirements.txt      # Dependencies info
├── README.md            # Documentation
├── LICENSE              # MIT License
├── INSTALL.md           # This file
├── USAGE_GUIDE.md       # Usage instructions
├── CHANGELOG.md         # Version history
├── config.json          # Configuration
└── mxai_wordlist.txt    # Generated wordlist (after first run)
```

---

## First Run

On first run, the tool will:
1. Check dependencies
2. Detect WiFi interfaces
3. Generate default wordlist (if needed)

Follow the on-screen menu to use the tool.

---

## Updating

To update to the latest version:
1. Download the new version
2. Replace old files
3. Run the tool

Your wordlists and configurations will be preserved.

---

## Uninstallation

To remove the tool:

### Windows
```bash
# Simply delete the folder
rmdir /s mxai-wifi-tool
```

### Linux
```bash
# Delete the folder
rm -rf mxai-wifi-tool
```

No system files are modified, so uninstallation is clean.

---

## Support

Need help?
- Check [USAGE_GUIDE.md](USAGE_GUIDE.md)
- Open an issue on GitHub
- Contact: [@_golu_.650](https://www.instagram.com/_golu_.650/) on Instagram

---

## Legal Notice

This tool is for educational and authorized testing only.  
Always obtain permission before testing networks.  
See [LICENSE](LICENSE) for full legal terms.

---

**Developed by Manoj Kumar**  
**Instagram**: [@_golu_.650](https://www.instagram.com/_golu_.650/)
