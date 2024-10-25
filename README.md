# MicroPython and Zephyr port on FRDM-MCXN947
## Overview
[Zephyr RTOS](https://zephyrproject.org/) is an [open source](https://github.com/zephyrproject-rtos/zephyr) real time operating system used in embedded development. It provides a kernel, file system, device drivers, firmware, high and low level API and a broad hardware support.

[MicroPython](https://docs.micropython.org/en/latest/) is an [open source](https://github.com/micropython/micropython) subset of Python 3 programming language that is optimized
for use on micro controllers and embedded devices.

[FRDM-MCXN947](https://www.nxp.com/design/design-center/development-boards-and-designs/general-purpose-mcus/frdm-development-board-for-mcx-n94-n54-mcus:FRDM-MCXN947) is a NPX's development board that can extend it's capabilities with extension boards.

## Development set up
In this section you will be guided on how to set up you development environment.
All the steps were tested only on Arch Linux, steps provided for other Linux distributions
and other operating systems were taken from the [official get started guide](https://docs.zephyrproject.org/latest/develop/getting_started/index.html)

### Zephyr
First we want to get our Zephyr development environment ready.

* ### System update
First make sure to update your system 
* ### Install dependencies
Then you will need to install development dependencies
### Arch Linux
```
sudo pacman -S git cmake ninja gperf ccache dfu-util dtc wget \
    python-pip python-setuptools python-wheel tk xz file make
```

### Fedora
```
sudo dnf group install "Development Tools" "C Development Tools and Libraries"
sudo dnf install cmake ninja-build gperf dfu-util dtc wget which \
  python3-pip python3-tkinter xz file python3-devel SDL2-devel
```

### Ubuntu
```
sudo apt-get install --no-install-recommends git cmake ninja-build gperf \
  ccache dfu-util device-tree-compiler wget \
  python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \
  make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1
```

**NOTE:** for other distributions, please consult your wiki page and correct package names if needed.
**NOTE**: if you do not have some of the dependencies in your package repository consider using third party package repository.

### macOS

Install [Homebrew](https://brew.sh/):
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After the Homebrew installation script completes, follow the on-screen instructions to add the Homebrew installation to the path.

* On macOS running on Apple Silicon, this is achieved with:
```
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> ~/.zprofile
source ~/.zprofile
```

* On macOS running on Intel, use the command for Apple Silicon, but replace /opt/homebrew/ with /usr/local/.

Use `brew` to install the required dependencies:
```
brew install cmake ninja gperf python3 python-tk ccache qemu dtc libmagic wget openocd
```

Add the Homebrew Python folder to the path, in order to be able to execute python and pip as well python3 and pip3.
```
(echo; echo 'export PATH="'$(brew --prefix)'/opt/python/libexec/bin:$PATH"') >> ~/.zprofile
source ~/.zprofile
```

### Windows
These instructions must be run in a cmd.exe command prompt terminal window. In modern version of Windows (10 and later) it is recommended to install the Windows Terminal application from the Microsoft Store. The required commands differ on PowerShell.

These instructions rely on [Chocolatey](https://chocolatey.org/). If Chocolatey isn’t an option, you can install dependencies from their respective websites and ensure the command line tools are on your `PATH` [environment variable](https://docs.zephyrproject.org/latest/develop/env_vars.html#env-vars).

Install [Chocolatey](https://chocolatey.org/install)

Open a `cmd.exe` terminal window as *Administrator*. To do so, press the Windows key, type `cmd.exe`, right-click the Command Prompt search result, and choose Run as *Administrator*.

Disable global confirmation to avoid having to confirm the installation of individual programs:
```
choco feature enable -n allowGlobalConfirmation
```
Use choco to install the required dependencies:
```
choco install cmake --installargs 'ADD_CMAKE_TO_PATH=System'
choco install ninja gperf python311 git dtc-msys2 wget 7zip
```

* ### Install the Zephyr Software Development Kit
There are two ways how to get Zephyrs SDK: install it with `west` cli util or to download and install it manually. I prefer and will use myself the manual installation, but you can skip it and use `west` later instead.

#### Linux
cd into preferred directory, then:
```
wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.17.0/zephyr-sdk-0.17.0_linux-x86_64.tar.xz
wget -O - https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.17.0/sha256.sum | shasum --check --ignore-missing
```
If you have architecture different from `x86_64` you will need to specify your architecture instead.
You can change 0.17.0 to another version in the instructions if needed; the [Zephyr SDK Releases](https://github.com/zephyrproject-rtos/sdk-ng/tags) page contains all available SDK releases.

Extract the Zephyr SDK bundle archive:
```
tar xvf zephyr-sdk-0.17.0_linux-x86_64.tar.xz
```

Run the Zephyr SDK setup script:
```
cd zephyr-sdk-0.17.0
./setup.sh
```

Install [udev](https://en.wikipedia.org/wiki/Udev) rules, which allow you to flash most Zephyr boards as a regular user:
```
sudo cp ~/zephyr-sdk-0.17.0/sysroots/x86_64-pokysdk-linux/usr/share/openocd/contrib/60-openocd.rules /etc/udev/rules.d
sudo udevadm control --reload
```

#### macOS
Download and verify the [Zephyr SDK bundle](https://github.com/zephyrproject-rtos/sdk-ng/releases/tag/v0.17.0):

```
cd ~
curl -L -O https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.17.0/zephyr-sdk-0.17.0_macos-x86_64.tar.xz
curl -L https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.17.0/sha256.sum | shasum --check --ignore-missing
```
If your host architecture is 64-bit ARM (Apple Silicon), replace `x86_64` with `aarch64` in order to download the 64-bit ARM macOS SDK.



Extract the Zephyr SDK bundle archive:
```
tar xvf zephyr-sdk-0.17.0_macos-x86_64.tar.xz
```

Run the Zephyr SDK bundle setup script:
```
cd zephyr-sdk-0.17.0
./setup.sh
```

#### Windows
Open a `cmd.exe` terminal window as a **regular user**

Download the [Zephyr SDK bundle](https://github.com/zephyrproject-rtos/sdk-ng/releases/tag/v0.17.0):
```
cd %HOMEPATH%
wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.17.0/zephyr-sdk-0.17.0_windows-x86_64.7z
```

Extract the Zephyr SDK bundle archive:
```
7z x zephyr-sdk-0.17.0_windows-x86_64.7z
```

Run the Zephyr SDK bundle setup script:
```
cd zephyr-sdk-0.17.0
setup.cmd
```

* ### Get Zephyr and install Python dependencies
You will need to install Zephyr's additional python dependencies and get Zephyrs source code

* First install Python `venv`:
#### Arch Linux
Python 3.3+ [comes preinstalled](https://wiki.archlinux.org/title/Python/Virtual_environment#Installation) with `venv` module.

#### Fedora
```
sudo dnf install python-virtualenv
```

#### Ubuntu
```
sudo apt install python3-venv
```

#### macOS & Windows
`venv` should have been installed along with Python.

* Create a new virtual environment:
#### Linux & macOs

```
python3 -m venv ~/zephyrproject/.venv
```
#### Windows:
Open a `cmd.exe` terminal window as a *regular user*

```
cd %HOMEPATH%
python -m venv zephyrproject\.venv
```

* Activate the virtual environment:

#### Linux & macOS
```
source ~/zephyrproject/.venv/bin/activate
```

#### Windows
```
zephyrproject\.venv\Scripts\activate.bat
```

* Install `west`:

```
pip install west
```
* Get Zephyr source code:
cd into your `zephyrproject` directory and run:
```
west init
west update
```
This will download the latest Zephyr version.

* Export a Zephyr CMake package. This allows CMake to automatically load boilerplate code required for building Zephyr applications.
```
west zephyr-export
```
* Zephyr’s scripts/requirements.txt file declares additional Python dependencies. Install them with pip.
```
pip install -r ~/zephyrproject/zephyr/scripts/requirements.txt
```

* ### Install the Zephyr SDK(if you haven't yet)

```
west sdk install
```


