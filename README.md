# MxAI WiFi Tool

<div align="center">

**A powerful cross-platform WiFi security assessment tool**

Developed by **Manoj Kumar**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)](https://github.com)

</div>

---

## 📱 Connect with Developer

- **Instagram**: [@_golu_.650](https://www.instagram.com/_golu_.650/)
- **Developer**: Manoj Kumar

---

## 🌟 Features

MxAI WiFi Tool provides comprehensive WiFi security assessment capabilities similar to aircrack-ng with an intuitive interface:

### Core Features
- ✅ **Cross-platform Support** - Works on Windows and Linux
- ✅ **WiFi Interface Management** - Auto-detect and select WiFi adapters
- ✅ **Network Scanning** - Discover nearby WiFi networks with detailed information
- ✅ **Wordlist Generation** - Create custom password lists for security testing
- ✅ **Monitor Mode Management** - Easy enable/disable monitor mode (Linux)
- ✅ **Deauthentication Attacks** - Disconnect devices from networks (Linux)
- ✅ **Handshake Capture** - Capture WPA/WPA2/WPA3 handshakes (Linux)
- ✅ **Password Cracking** - Crack captured handshakes using wordlists (Linux)

### User Interface
- 🎯 Clean, professional terminal interface
- 🎯 Intuitive menu-driven navigation
- 🎯 Clear status messages (SUCCESS, FAILED, WARNING)
- 🎯 Automatic menu display after each action
- 🎯 Flexible wordlist selection (default or custom)

---

## 📋 Requirements

### Windows
- Python 3.6 or higher
- netsh (built-in)

### Linux (Full Features)
- Python 3.6 or higher
- aircrack-ng suite
- wireless-tools
- WiFi adapter with monitor mode support

---

## 🚀 Installation

### Quick Start

```bash
# Clone or download the repository
git clone <repository-url>
cd mxai-wifi-tool

# No pip packages required!
# Just run the tool
python wifi_tool.py
```

### Linux Setup (for full features)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install aircrack-ng wireless-tools python3

# Arch Linux
sudo pacman -S aircrack-ng wireless_tools python

# Fedora/RHEL
sudo yum install aircrack-ng wireless-tools python3
```

---

## 💻 Usage

### Starting the Tool

```bash
# On Windows
python wifi_tool.py

# On Linux (recommended for full features)
sudo python3 wifi_tool.py
```

### Main Menu

```
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

### Quick Workflow

1. **Select Option 1** - Auto-detect WiFi interface
   - Choose your WiFi adapter
   - Select wordlist (default or custom)

2. **Select Option 2** - Scan all nearby networks
   - View all WiFi networks in range
   - Select target network
   - Choose attack type

3. **Attack Options**:
   - **Deauth Attack** - Disconnect devices from network
   - **Password Attack** - Capture handshake and crack password
   - **Combined Attack** - Both deauth and password attack

---

## 🎯 Features in Detail

### 1. WiFi Interface Detection
- Automatically finds all WiFi adapters
- Shows interface names and details
- Easy selection process

### 2. Network Scanning
- Scans for all nearby WiFi networks
- Displays:
  - Network name (ESSID)
  - MAC address (BSSID)
  - Channel number
  - Encryption type
- Real-time scanning

### 3. Wordlist Management
Three options for wordlist selection:
- **Default Wordlist**: Auto-generated with 1019 common passwords
- **Custom Wordlist**: Provide your own wordlist file path
- **Back to Menu**: Return without selecting

### 4. Monitor Mode (Linux Only)
- Easy toggle on/off
- Automatic management during attacks
- Status display
- Error handling

### 5. Deauthentication Attack (Linux Only)
- Disconnect devices from target network
- Configurable packet count
- Broadcast or specific client targeting
- Automatic monitor mode management

### 6. Password Attack (Linux Only)
- Capture WPA/WPA2 handshakes
- Crack passwords using wordlists
- Progress indication
- Automatic monitor mode management

### 7. Combined Attack (Linux Only)
- Automated workflow:
  1. Deauth attack to trigger handshake
  2. Capture handshake
  3. Crack password immediately
- Fully automated process

---

## 🛡️ Supported WiFi Adapters

The tool works best with adapters that support monitor mode and packet injection:

### Recommended Adapters
- **Alfa AWUS036NHA** - Excellent compatibility
- **Alfa AWUS036NH** - Great performance
- **TP-Link TL-WN722N v1** - Budget-friendly (v1 only!)
- **Panda PAU09** - Good alternative
- **Alfa AWUS036ACH** - Dual-band support

### Chipsets
- RTL8812AU
- RTL8814AU
- Atheros AR9271
- Ralink RT3070

---

## 📊 Platform Comparison

| Feature | Windows | Linux |
|---------|---------|-------|
| WiFi Interface Detection | ✅ | ✅ |
| Network Scanning | ✅ | ✅ |
| Wordlist Generation | ✅ | ✅ |
| Monitor Mode | ❌ | ✅ |
| Deauth Attacks | ❌ | ✅ |
| Handshake Capture | ❌ | ✅ |
| Password Cracking | ❌ | ✅ |

---

## 📖 Documentation

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detailed usage instructions
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and updates
- **[LICENSE](LICENSE)** - MIT License and legal notices

---

## ⚠️ Legal Disclaimer

**IMPORTANT: Read Before Using**

This tool is intended for:
- ✅ Educational purposes
- ✅ Authorized security testing
- ✅ Network administration on your own networks
- ✅ Penetration testing with written permission

### Legal Requirements

You MUST:
- Only use on networks you own or have explicit written permission to test
- Comply with all applicable laws and regulations
- Understand that unauthorized access is illegal

### Prohibited Uses

You MUST NOT:
- ❌ Access networks without authorization
- ❌ Disrupt network services without permission
- ❌ Use for malicious purposes
- ❌ Violate any laws or regulations

### Legal Consequences

Unauthorized network access may violate:
- Computer Fraud and Abuse Act (CFAA) - United States
- Computer Misuse Act - United Kingdom
- Similar laws in other jurisdictions

**Penalties may include fines and imprisonment.**

### Developer Responsibility

The developer (Manoj Kumar) is NOT responsible for:
- Misuse of this software
- Any illegal activities
- Damages caused by improper use
- Violations of laws or regulations

**By using this tool, you agree to use it responsibly and legally.**

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### How to Contribute
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Manoj Kumar**

- Instagram: [@_golu_.650](https://www.instagram.com/_golu_.650/)
- Tool: MxAI WiFi Tool v1.0

---

## 🙏 Acknowledgments

- Inspired by aircrack-ng suite
- Built with Python standard library
- Thanks to the security research community

---

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact via Instagram: [@_golu_.650](https://www.instagram.com/_golu_.650/)

---

## 🔄 Version

**Current Version**: 1.1

**Last Updated**: 2025

---

<div align="center">

**Made with ❤️ by Manoj Kumar**

**Follow on Instagram**: [@_golu_.650](https://www.instagram.com/_golu_.650/)

⭐ Star this repository if you find it helpful!

</div>

---

## 📸 Screenshots

### Main Menu
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

## 🎓 Educational Use Only

This tool is designed for educational purposes to help users understand:
- WiFi security protocols
- Network security assessment
- Penetration testing methodologies
- Security best practices

Always practice ethical hacking and responsible disclosure.

---

**Remember: With great power comes great responsibility. Use wisely!**
