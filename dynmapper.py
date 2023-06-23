# Script by 3meraldK
# Usage: In command prompt, run: dynmapper.py (aurora/nova) (default/meganation/alliance) (x blocks per pixel) ((top-left corner XZ coords),(bottom-right corner XZ coords))
# Example:                       dynmapper.py aurora        meganation                    4                    ((-2048,-1132),(4516,2964)) <- no spaces
import requests
import sys
from PIL import Image, ImageDraw

world =  sys.argv[1]
mode = sys.argv[2]
scale = int(sys.argv[3])
corners = eval(sys.argv[4])
marker_URL = 'https://earthmc.net/map/' + world + '/standalone/MySQL_markers.php?marker=_markers_/marker_earth.json'
alliances_api_URL = 'https://emctoolkit.vercel.app/api/' + world + '/alliances'

if scale = 0:
	print("Scale must not be zero, exiting..")
	exit()

def hex_to_rgba(hex_str, alpha):
	r, g, b = (int(hex_str[i:i+2], 16) for i in range(1, 7, 2))
	return (r, g, b, alpha)

if world not in ["aurora", "nova"]:
	print("Wrong world, please correct, exiting..")
	exit()
if mode not in ["default", "meganation", "alliance"]:
	print("Wrong mode, please correct, exiting..")
	exit()
print("Fetching {}s from world {} at scale 1:{}".format(mode, world, str(scale)))

if mode != "default":
	print("Fetching alliances from {}...".format(alliances_api_URL))
	response = requests.get(alliances_api_URL)
	if response.status_code != requests.codes.ok:
		print('The response status is not OK. Try later, exiting..')
		exit()
	data = response.json()
	arr = []

	lookup = {
		"alliance": "normal",
		"meganation": "mega"
	}
	for element in data:
		fetching_req = lookup.get(mode, mode)
		if element.get('type') == fetching_req:
			fill = element.get('colours', {}).get('fill', '#000000')
			outline = element.get('colours', {}).get('outline', '#000000')
			nations = element.get('nations', [])
			sub_arr = [fill, outline, nations]
			arr.append(sub_arr)

print("Fetching marker_earth.json from {}...".format(marker_URL))
response = requests.get(marker_URL)
if response.status_code != requests.codes.ok:
	print('The response status is not OK. Try later, exiting..')
	exit()
data = response.json()
areas = data["sets"]["townyPlugin.markerset"]["areas"]
towns = []

for area in areas:
	fill = areas[area]["fillcolor"]
	if fill == "#00FF00":
		continue
	outline = areas[area]["color"]
	x = areas[area]["x"]
	z = areas[area]["z"]
	town = areas[area]["label"]
	if corners != ((0, 0), (0, 0)):
		height = round(abs(corners[0][1] - corners[1][1]) / scale)
		coords = [(round((x[i] - corners[0][0]) / scale), round((z[i] - corners[0][1]) / scale)) for i in range(len(x))]
	else:
		coords = [(round((x[i] + 33280) / scale), round((z[i] + 16640) / scale)) for i in range(len(x))]
	

	if mode != "default":
		desc = areas[area]["desc"]
		desc = desc.replace(" (Shop)", "")
		if "()</span><br /> Mayor" in desc:
			fill = outline = "#000000"
		else:
			if "nofollow\">" in desc:
				start = desc.find("nofollow\">")
				end = desc.find("</a>")
				nation = desc[start:end]
				nation = nation.replace("nofollow\">", "")
			else:
				start = desc.find(town + " (") + len(town + " (")
				end = desc.find(")</span><br /> Mayor")
				nation = desc[start:end]

			if mode == "alliance":
				fill = outline = "#000000"
			if mode == "meganation":
				if fill == "#3FB4FF":
					fill = outline = "#000000"
			for alliance in arr:
				if nation in alliance[2]:
					fill = alliance[0]
					outline = alliance[1]
	
	town = {"fill": fill, "outline": outline, "coords": coords}
	towns.append(town)

if corners != ((0, 0), (0, 0)):
	width = round(abs(corners[0][0] - corners[1][0]) / scale)
	height = round(abs(corners[0][1] - corners[1][1]) / scale)
else:
	width = round(66360 / scale)
	height = round(33148 / scale)
print("Data fetched! Creating image of {} x {} px in the script's directory".format(str(width), str(height)))
image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

[ draw.polygon(town["coords"], hex_to_rgba(town["fill"], 51), hex_to_rgba(town["outline"], 255)) for town in towns ]
FILE_NAME = "{}-{}.png".format(mode, world)
image.save(FILE_NAME)
print("Saved image as " + FILE_NAME)
