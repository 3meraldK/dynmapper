# dynmapper
Python script to generate the Squaremap's (not Dynmap) image of the Towny layer, with [astral-sh/uv](https://github.com/astral-sh/uv) support. Tested on Windows 11 with Python 3.13.13 on EarthMC Minecraft server.

## Installation

### 1. Prerequisites
1. Download [`dynmapper.py`](https://raw.githubusercontent.com/3meraldK/dynmapper/main/dynmapper.py) to a directory of choice.
2. Open a terminal of choice (e.g. the Command Prompt) and navigate to the directory.

### 2.a. Classic way
1. Download Python, preferably 3.13.13 or newer.
2. Download [`requirements.txt`](https://raw.githubusercontent.com/3meraldK/dynmapper/main/requirements.txt) to the same directory.
3. In the terminal you opened before, run `pip install -r requirements.txt` to download required dependencies.
4. Run `python dynmapper.py`.

### 2.b. astral.sh/uv
1. Install [astral-sh/uv](https://docs.astral.sh/uv/#installation) with Python, preferably 3.13.13 or newer.
2. In the terminal you opened before, run `uv run dynmapper.py`.

## Program

### 1. What to expect
It will run a wizard where you input a map URL, scale and map bounds.

### 2. About plugins
Wizard will ask you if you want to use plugins. They are small scripts designed for modifying the output image. There is one plugin in `plugins/earthmc_emcstats.py` for a specific Minecraft server to color towns according to which alliance they belong to. This is a proof of concept for plugins in this script. Plugins work simply: they have `towns` variable already defined and they're intended to modify it.

## Example output
<img src="https://github.com/user-attachments/assets/48e6dae2-a3e3-4e06-bf2a-d819bc3eb5c4" />

