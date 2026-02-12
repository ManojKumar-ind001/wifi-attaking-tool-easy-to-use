#!/bin/bash

echo "Installing MxAI WiFi Tool dependencies..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux system"
    
    if command -v apt-get &> /dev/null; then
        echo "Installing aircrack-ng..."
        sudo apt-get update
        sudo apt-get install -y aircrack-ng wireless-tools
        
        echo "Setting up Python environment..."
        sudo apt-get install -y python3 python3-pip
        
    elif command -v yum &> /dev/null; then
        echo "Installing aircrack-ng..."
        sudo yum install -y aircrack-ng wireless-tools
        
        echo "Setting up Python environment..."
        sudo yum install -y python3 python3-pip
        
    elif command -v pacman &> /dev/null; then
        echo "Installing aircrack-ng..."
        sudo pacman -S aircrack-ng wireless-tools
        
        echo "Setting up Python environment..."
        sudo pacman -S python python-pip
    fi
    
    echo "Making script executable..."
    chmod +x wifi_tool.py
    
    echo "Installation complete!"
    echo "Run with: sudo python3 wifi_tool.py"
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    echo "Install aircrack-ng via Homebrew: brew install aircrack-ng"
    echo "Run with: python3 wifi_tool.py"
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Detected Windows"
    echo "Windows support is limited to basic scanning"
    echo "For full features, use Linux with monitor mode support"
    echo "Run with: python wifi_tool.py"
    
else
    echo "Unknown OS. Manual installation required."
fi

echo ""
echo "Note: Some features require WiFi adapter with monitor mode support"
echo "Common compatible adapters:"
echo "- Alfa AWUS036NHA"
echo "- TP-Link TL-WN722N"
echo "- Panda PAU09"