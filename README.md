# dynmapper
Overlay towns from Minecraft Dynmap onto an image

## Requirements
- Python (tested on 3.11)
- Libraries from pip: requests, sys, PIL

## Usage
1. Ensure you meet requirements presented above.
2. Download [the latest release](https://github.com/3meraldK/dynmapper/releases/latest).
3. Open command prompt/terminal in a folder with the script.
4. In command prompt, run: 
- `dynmapper.py [aurora/nova] [default/meganation/alliance] [x blocks per pixel] [(top-left corner XZ coords),(bottom-right corner XZ coords)]`
- ✅ Good example: dynmapper.py aurora meganation 4 ((-2048,-1132),(4516,2964))
- ⚠️ Wrong example: dynmapper.py aurora Russian_Empire 1 ((-1024, -1337), (2999, 3111))

## Generated example
![meganation-aurora](https://user-images.githubusercontent.com/48335651/224452178-dd3f6f07-2131-457b-933f-439cf373d08e.png)
