# Script by 3meraldK

import requests
import sys
import time
import re
from PIL import Image, ImageDraw

def hex_to_rgba(hex_string, alpha):
	r, g, b = (int(hex_string[i:i+2], 16) for i in range(1, 7, 2))
	return (r, g, b, alpha)

def round_to_16(number):
	return round(number / 16) * 16

def quit(reason):
	print(reason)
	exit()

print('')

markers_URL = 'https://map.earthmc.net/tiles/minecraft_overworld/markers.json'
alliances_api_URL = 'https://emctoolkit.vercel.app/api/aurora/alliances'
mode = sys.argv[1]
scale = float(sys.argv[2])
corners = None

# Parse corners
if len(sys.argv) > 3:
	if len(sys.argv) < 7:
		quit('Usage: python dynmapper.py [default/meganation/alliance] [blocks per pixel] (corner coordinates)')

	# Parse corner coordinates
	coords = sys.argv[3:7]
	for i, coord in enumerate(coords):
		try:
			# Clamping x and z coordinates
			if i == 0 or i == 2: coords[i] = max(min(int(coord), 33080), -33280)
			else: coords[i] = max(min(int(coord), 16508), -16640)
		except ValueError:
			quit('Corners were not put in correct format, exiting..')

	corners = ((coords[0], coords[1]), (coords[2], coords[3]))

# Parse other unintended inputs
if scale <= 0:
	quit('Scale must be a positive number, exiting..')
if mode not in ['default', 'meganation', 'alliance']:
	quit('Wrong mode, exiting..')

print(f'Fetching {mode}s at scale 1:{scale:g}')

if mode != 'default':
	print(f'Fetching alliances from {alliances_api_URL}..')

	response = requests.get(alliances_api_URL)
	if response.status_code != requests.codes.ok:
		quit('The response status is not OK. Try later, exiting..')

	codes = { 'alliance': 'normal', 'meganation': 'mega' }

	data = response.json()
	alliances = []

	for alliance in data:
		type = codes.get(mode, mode)
		if alliance.get('type') != type: continue
		fill = alliance.get('colours', {}).get('fill', '#000000')
		outline = alliance.get('colours', {}).get('outline', '#000000')
		nations = alliance.get('nations', [])
		alliance_data = [fill, outline, nations]
		alliances.append(alliance_data)

print(f'Fetching markers.json from {markers_URL}..')

response = requests.get(markers_URL)
if response.status_code != requests.codes.ok:
	quit('The response status is not OK. Try later, exiting..')

data = response.json()
regions = []

for marker in data[0]['markers']:
	if marker['type'] != 'polygon':
		continue

	nation = re.search(r'\(\b(?:Member|Capital)\b of (.*)\)\n', marker['tooltip'])
	fill = marker.get('fillColor')
	outline = marker.get('color')

	if fill == None or nation == None: fill = '#000000'
	if outline == None or nation == None: outline = '#000000'

	if mode != 'default' and nation != None:
		nation = nation.group(1)
		if mode == 'alliance':
			fill = outline = '#000000'
		if mode == 'meganation':
			if fill == '#3FB4FF': fill = outline = '#000000'

		for alliance in arr:
			if nation not in alliance[2]: continue
			fill = alliance[0]
			outline = alliance[1]

	for region in marker['points']:
		x = []
		z = []
		for vertex in region[0]:
			x.append(round_to_16(vertex['x']))
			z.append(round_to_16(vertex['z']))

		# Calculate town coordinates
		if corners:
			# Extract min and max coordinates to handle any order of provided corners
			min_x = min(corners[0][0], corners[1][0])
			max_x = max(corners[0][0], corners[1][0])
			min_z = min(corners[0][1], corners[1][1])
			max_z = max(corners[0][1], corners[1][1])
			coords = [(round((x[i] - min_x) / scale), round((z[i] - min_z) / scale)) for i in range(len(x))]
		else:
			coords = [(round((x[i] + 33280) / scale), round((z[i] + 16640) / scale)) for i in range(len(x))]

		region = {'fill': fill, 'outline': outline, 'coords': coords}
		regions.append(region)

# Calculate image size
if corners:
	width = round(abs(corners[0][0] - corners[1][0]) / scale)
	height = round(abs(corners[0][1] - corners[1][1]) / scale)
else:
	width = round(66360 / scale)
	height = round(33148 / scale)

if width <= 0 or height <= 0:
    quit('Width or height of image is not positive, exiting..')

print(f'Creating image of {width} x {height} px in current directory..')

image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)
[ draw.polygon(region['coords'], hex_to_rgba(region['fill'], 51), hex_to_rgba(region['outline'], 255)) for region in regions ]

file_name = f'{mode}-{int(time.time())}.png'
image.save(file_name)
print(f'Saved image as {file_name}, exiting..')