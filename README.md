# dynmapper
Python script to overlay towns from Minecraft Dynmap onto an image. Written for EarthMC, because it's the only **serious** Towny server I know of. Can be modified to your needs or servers if you want.

### Requirements
- Python
- Python modules: requests, Pillow

Tested on Windows 10 x64, Python 3.11.5

## Installation and usage
1. Download `dynmapper.py` and `requirements.txt`.
2. Open your desired terminal (e.g. Windows' Command Prompt) and navigate to the directory with downloaded files.
3. Run `pip install -r requirements.txt` to download mandatory modules.
4. Run `dynmapper.py` via the command:
<pre>python dynmapper.py [aurora/nova] [default/meganation/alliance] [x blocks per pixel] ((top-left corner XZ coords),(bottom-right corner XZ coords))</pre>
- ✅ Good example: `python dynmapper.py aurora meganation 4 ((-2048,-1132),(4516,2964))`
- ⛔ Wrong example: `python dynmapper.py aurora Russian_Empire 1 ((-1024, -1337), (2999, 3111))`
- ℹ️ Last parameter is optional.

### Notes
- Scale (x blocks per pixel) can be any positive number, for example `2.5`.
- For the corners parameter, only this form: `((top-left),(bottom-right))` is allowed. That means, `((bottom-left),(top-right))` etc. are disallowed.
    - When not passed, the script will generate whole world's town map.

## Another generated example
![image](https://github.com/3meraldK/dynmapper/assets/48335651/e54a4191-b103-4ebb-9925-c5dc118269fa)

