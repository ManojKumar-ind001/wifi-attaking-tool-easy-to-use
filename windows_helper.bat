@echo off
echo MxAI WiFi Tool - Windows Helper
echo ================================
echo.
echo This tool provides basic WiFi scanning on Windows.
echo For full features (deauth, cracking), use Linux with monitor mode.
echo.
echo Options:
echo 1. Scan for WiFi networks
echo 2. Generate wordlist
echo 3. Check WiFi interfaces
echo 4. Exit
echo.

:menu
set /p choice="Select option (1-4): "

if "%choice%"=="1" (
    echo Scanning for WiFi networks...
    netsh wlan show networks mode=bssid
    goto menu
)

if "%choice%"=="2" (
    echo Generating wordlist...
    python wifi_tool.py
    goto menu
)

if "%choice%"=="3" (
    echo Listing WiFi interfaces...
    netsh wlan show interfaces
    goto menu
)

if "%choice%"=="4" (
    echo Exiting...
    exit /b 0
)

echo Invalid choice
goto menu