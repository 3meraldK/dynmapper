# dynmapper
Python script to overlay towns from Minecraft Dynmap onto an image. Supports EarthMC, because it's the only **serious** Towny server I know of. Can be adapted to your needs or servers if you know Python.

### Requirements
- Python
- Python libraries: requests, sys, PIL, time, re

Tested on Windows 10 x64, Python 3.11.2

## Usage
Run this script from desired terminal. It should look like this:
<pre>$ python dynmapper.py [aurora/nova] [default/meganation/alliance] [x blocks per pixel] ((top-left corner XZ coords),(bottom-right corner XZ coords))</pre>
- ✅ Good example: python dynmapper.py aurora meganation 4 ((-2048,-1132),(4516,2964))
- ⚠️ Wrong example: python dynmapper.py aurora Russian_Empire 1 ((-1024, -1337), (2999, 3111))

### Notes
- Scale (x blocks per pixel) can be any positive number, for example `2.5`.
- For the corners parameter, only this form: `((top-left),(bottom-right))` is allowed. That means, `((bottom-left),(top-right))` etc. are disallowed.
    - Optionally, corners may be `((0,0),(0,0))`, which will generate whole world town map.
    - Don't put spaces in the last parameter.

## Another generated example
![image](https://github.com/3meraldK/dynmapper/assets/48335651/e54a4191-b103-4ebb-9925-c5dc118269fa)

