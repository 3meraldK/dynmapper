# Script by 3meraldK

import requests
import sys
import time
import re
from PIL import Image, ImageDraw

def hex_to_rgba(hex_string, alpha):
	try: r, g, b = (int(hex_string[i:i+2], 16) for i in range(1, 7, 2))
	except: r, g, b = 255, 255, 255
	return (r, g, b, alpha)

def round_to_16(number):
	return round(number / 16) * 16

def clamp(number, min_value, max_value):
	return max(min(number, max_value), min_value)

print('')
print('Dynmapper by 3meraldK')

if len(sys.argv) < 3:
	exit('Usage: python dynmapper.py [default/meganation/alliance] [blocks per pixel] (corner coordinates)\n')

markers_URL = 'https://map.earthmc.net/tiles/minecraft_overworld/markers.json'
alliances_api_URL = 'https://emctoolkit.vercel.app/api/aurora/alliances'
mode = sys.argv[1]
scale = float(sys.argv[2])
# World boundaries. Default option
corners = [-33280, -16640, 33080, 16508]

# Parse corners
if len(sys.argv) > 3:
	if len(sys.argv) < 7:
		exit('Usage: python dynmapper.py [default/meganation/alliance] [blocks per pixel] (corner coordinates)\n')

	# Parse corner coordinates
	corners = sys.argv[3:7]
	for i, corner in enumerate(corners):
		isX = i == 0 or i == 2
		try:
			# Clamping x and z coordinates
			if isX: corners[i] = clamp(int(corner), -33280, 33080)
			else: corners[i] = clamp(int(corner), -16640, 16508)
		except ValueError:
			exit('Corners were not put in correct format, exiting..\n')

# Parse other unintended inputs
if scale <= 0:
	exit('Scale must be a positive number, exiting..\n')
if mode not in ['default', 'meganation', 'alliance']:
	exit('Wrong mode, exiting..\n')

print(f'Creating {mode} map at scale 1:{scale:g}..')

if mode != 'default':
	print(f'Fetching alliances from ({alliances_api_URL})..')

	response = requests.get(alliances_api_URL)
	if response.status_code != requests.codes.ok:
		exit('The response status is not OK. Try later, exiting..\n')

	codes = { 'alliance': 'normal', 'meganation': 'mega' }

	data = response.json()
	alliances = []

	for alliance in data:
		type = codes.get(mode, mode)
		if alliance.get('type') != type: continue
		fill = alliance.get('colours', {}).get('fill', '#000000')
		outline = alliance.get('colours', {}).get('outline', '#000000')
		nations = alliance.get('nations', [])
		alliance_data = {'fill': fill, 'outline': outline, 'nations': nations}
		alliances.append(alliance_data)

print(f'Fetching markers.json from ({markers_URL})..')

response = requests.get(markers_URL)
if response.status_code != requests.codes.ok:
	exit('The response status is not OK. Try later, exiting..\n')

data = response.json()
regions = []

for marker in data[0]['markers']:
	if marker['type'] != 'polygon':
		continue

	nation = re.search(r'\(\b(?:Member|Capital)\b of (.*)\)\n', marker['tooltip'])
	fill = marker.get('fillColor')
	outline = marker.get('color')

	if outline == None: outline = fill
	if nation == None: fill = outline = '#000000'

	if mode != 'default' and nation != None:
		nation = nation.group(1)
		if mode == 'alliance':
			fill = outline = '#000000'
		if mode == 'meganation':
			if fill == '#3FB4FF': fill = outline = '#000000'

		for alliance in alliances:
			if nation not in alliance['nations']: continue
			fill = alliance['fill']
			outline = alliance['outline']

	for region in marker['points']:
		x = []
		z = []
		for vertex in region[0]:
			x.append(round_to_16(vertex['x']))
			z.append(round_to_16(vertex['z']))

		# Calculate town coordinates
		# Extract min coordinates to handle any order of provided corners
		min_x = min(corners[0], corners[2])
		min_z = min(corners[1], corners[3])
		coords = [(round((x[i] - min_x) / scale), round((z[i] - min_z) / scale)) for i in range(len(x))]

		region = {'fill': fill, 'outline': outline, 'coords': coords}
		regions.append(region)

# Calculate image size
width = round(abs(corners[0] - corners[2]) / scale)
height = round(abs(corners[1] - corners[3]) / scale)

if width <= 0 or height <= 0:
	exit('Width or height of image is not positive, exiting..\n')

print(f'Saving image of {width} x {height} px in current directory..')
save_start = time.time()
image = Image.new(mode='RGBA', size=(width, height))
draw = ImageDraw.Draw(image)
for region in regions:
	fill = hex_to_rgba(region['fill'], 51)
	outline = hex_to_rgba(region['outline'], 255)
	draw.polygon(region['coords'], fill, outline)
now = int(time.time())
file_name = f'{mode}-{now}.png'
image.save(file_name)
save_stop = time.time()

print(f'Saved image as {file_name} in {round(save_stop - save_start, 2)}s\n')
