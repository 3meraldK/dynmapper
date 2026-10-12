# dynmapper
Python script to generate the Squaremap's .png image of the Towny layer, with [the uv](https://github.com/astral-sh/uv) support. Tested on Windows 11 with Python 3.13.13 on EarthMC Minecraft server.

## Installation

### 1. Prerequisites
1. Download [`dynmapper.py`](https://raw.githubusercontent.com/3meraldK/dynmapper/main/dynmapper.py) to a directory of choice.
2. Open a terminal of choice (e.g. the Command Prompt) and navigate to the directory.

### 2.a. Classic way
1. Download Python, 3.13.13 is preferred, but older versions likely work too.
2. Download [`requirements.txt`](https://raw.githubusercontent.com/3meraldK/dynmapper/main/requirements.txt) to the same directory.
3. In the terminal you opened before, run `pip install -r requirements.txt` to download required dependencies.
4. Run `python dynmapper.py [map url] [world name] [scale] [corner coordinates]`.

### 2.b. astral.sh/uv
1. Follow [official docs](https://docs.astral.sh/uv/#installation) to install uv and Python.
2. In the terminal you opened before, run `uv run dynmapper.py [map url] [world name] [scale] [corner coordinates]`.

## Usage
- `[map url]` - URL to the map
- `[world name]` - name of the world you want to get the map of. To get it, click the small link button in bottom-left corner on a website. The page should refresh and the updated URL should include the world's name in it, for example: `?world=world_name`.
- `[scale]` - how many blocks should be 1 pixel. This can be any positive number, decimal or whole.
- `[corner coordinates]` - series of whole numbers in format "x1 z1 x2 z2" representing any diagonal corners (their in-game coordinates) of the output map.
- ✅ Good example (test it out!): `python dynmapper.py https://map.earthmc.net minecraft_overworld 1 -2280 -13344 7720 -6408`
- ⛔ Wrong example: `python dynmapper.py map.earthmc.net earth -4.4 (-1000, -2000) (1000, 4000)`

## Example output
![image](https://github.com/3meraldK/SquaremapImageExport/assets/48335651/2c08b50f-8d18-4a86-a75a-adcc7021a125)
