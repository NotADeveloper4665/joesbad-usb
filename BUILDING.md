# Building OpenUSBIP

This repository contains separate deliverables. Build only the component you
intend to run; the Android app, desktop client, Linux USB/IP server, and
headless hub do not share one runtime.

## Requirements

| Deliverable | Build environment |
|---|---|
| Linux desktop Python package | Linux, Python 3.10+, pip |
| Windows desktop client | Windows 10/11, Python 3.10+ |
| Android server APK | JDK 17, Android SDK platform 34, build-tools 34.0.0 |
| Linux server and headless hub | Linux, Python 3.10+, kernel USB/IP support and distro USB/IP tools |

## Linux desktop client

From the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
openusbip-client
```

For development and tests:

```bash
python -m pip install -e '.[dev]'
ruff check .
QT_QPA_PLATFORM=offscreen pytest
python -m compileall -q src openusbip_client.py openusbip_server.py
```

To produce distributable Python source and wheel archives:

```bash
python -m pip install --upgrade build
python -m build
```

The resulting files are written to `dist/`. The desktop client still needs the
OS USB/IP tools and kernel virtual-host-controller support at runtime; those
are not bundled in the Python wheel.

## Windows desktop client

On Windows PowerShell, from the repository root:

```powershell
.\packaging\windows\build.ps1 -Clean
```

The one-folder application is written to `dist\OpenUSBIP\`. Distribute the
whole folder, not just `OpenUSBIP.exe`. Install
[usbip-win2](https://github.com/vadimgrn/usbip-win2/releases) separately; its
driver is not bundled. The executable is unsigned and may trigger SmartScreen.

## Android server APK

Install JDK 17 and Android SDK platform 34 plus build-tools 34.0.0. Set
`JAVA_HOME` and `ANDROID_HOME`, then:

```bash
cd android
./gradlew :app:testDebugUnitTest
./gradlew :app:assembleDebug
```

The debug APK is
`android/app/build/outputs/apk/debug/app-debug.apk`. On Windows use
`gradlew.bat` with the same Gradle tasks. `local.properties` is machine-local
and should not be committed.

## Linux server and headless hub

These are source-run Python services rather than standalone compiled
executables. On supported Linux systems, use the repository installers:

```bash
./install-server.sh
sudo ./install-hub.sh
```

The server requires the kernel USB/IP host module and the distro's `usbipd`.
The hub requires the virtual host controller (`vhci_hcd`) and the USB/IP
client tools. The hub installer targets Debian-family systems. Read the
[security notes](README.md#security) before exposing either service to a
network.

## Automated builds

GitHub Actions runs the Python checks, Windows executable build, and Android
unit tests/APK build for pull requests and pushes. The separate Build
workflow publishes downloadable build artifacts for manual runs and version
tags. These artifacts are CI outputs, not signed installers or a guarantee
that the target machine has the required USB/IP kernel drivers.
