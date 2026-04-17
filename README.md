# Q.exe: Advanced Game Analysis & Hooking Tool

Q.exe is a high-performance game analysis framework based on the Frida 16.2 engine, designed for Android emulators and physical devices via ADB. This project serves as an educational tool for reverse engineering and security research.

## Key Features
- Engine: Frida 16.2 Dynamic Instrumentation
- Target: Android Emulator (x86_64) & Physical Devices (ARM64) via ADB
- Implemented Modules:
    - Aimbot: Target tracking through memory manipulation and vector calculations.
    - ESP (Extra Sensory Perception): Visualization by intercepting location data.
    - No Spread: Hooking bullet spread function routines and fixing constant values.
    - No Recoil: Bypassing and resetting recoil logic.

## Prerequisites
- Frida 16.2.x installed
- ADB (Android Debug Bridge) environment configuration
- Python 3.10+ (for CLI Wrapper execution)

## Usage
1. Execute frida-server on the target device.
2. Run Q.exe (or the main Python script) on the host PC.
3. Perform injection into the target process via ADB.

## Disclaimer
This program is developed strictly for educational and research purposes. Use in commercial live games is prohibited, and the user assumes all responsibility for any consequences arising from its use.

## made by asp1-rin