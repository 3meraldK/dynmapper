# dynmapper
Python script to generate a map of towns from EarthMC map website onto an image. Tested on Windows 10 with Python 3.11.5.

## Installation and usage
1. Download Python.
2. Download [`dynmapper.py`](https://raw.githubusercontent.com/3meraldK/dynmapper/main/dynmapper.py) and [`requirements.txt`](https://raw.githubusercontent.com/3meraldK/dynmapper/main/requirements.txt) by clicking hyperlinks and saving files onto your computer to same directory.
3. Open your desired terminal (e.g. Windows' Command Prompt) and navigate to the directory with downloaded files.
4. Run `pip install -r requirements.txt` to download required modules.
5. Run `dynmapper.py` via command:
<pre>python dynmapper.py [default/meganation/alliance] [blocks per pixel] (corner coordinates)</pre>
- ✅ Good example (test it out!): `python dynmapper.py meganation 4 -2280 -13344 7720 -6408`
- ⛔ Wrong example: `python dynmapper.py Some_Pact 1 (-1024, -2048) (1024, 4096)`
- ℹ️ Corner coordinates are optional. When not passed, script generates whole world's map.
- Scale (blocks per pixel) can be any positive number.

## Another generated example
![image](https://github.com/3meraldK/dynmapper/assets/48335651/e54a4191-b103-4ebb-9925-c5dc118269fa)