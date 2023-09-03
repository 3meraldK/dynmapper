# Script by 3meraldK

import requests
import sys
import time
import re
from PIL import Image, ImageDraw

def hex_to_rgba(hex_str, alpha):
	r, g, b = (int(hex_str[i:i+2], 16) for i in range(1, 7, 2))
	return (r, g, b, alpha)

world =  sys.argv[1]
mode = sys.argv[2]
scale = float(sys.argv[3])
corners = None
if len(sys.argv) > 4:
    corners = eval(sys.argv[4])
marker_URL = f'https://earthmc.net/map/{world}/standalone/MySQL_markers.php?marker=_markers_/marker_earth.json'
alliances_api_URL = f'https://emctoolkit.vercel.app/api/{world}/alliances'

if scale <= 0:
	print('Scale must be a positive number, exiting..')
	exit()
if world not in ['aurora', 'nova']:
	print('World must be either nova or aurora, exiting..')
	exit()
if mode not in ['default', 'meganation', 'alliance']:
	print('Wrong mode, exiting..')
	exit()

print(f'Fetching {mode}s from world {world} at scale 1:{scale}')

if mode != 'default':

	print(f'Fetching alliances from {alliances_api_URL}..')
	response = requests.get(alliances_api_URL)
	if response.status_code != requests.codes.ok:
		print('The response status is not OK. Try later, exiting..')
		exit()
	data = response.json()
	arr = []

	lookup = {
		'alliance': 'normal',
		'meganation': 'mega'
	}

	for element in data:
		fetching_req = lookup.get(mode, mode)
		if element.get('type') == fetching_req:
			fill = element.get('colours', {}).get('fill', '#000000')
			outline = element.get('colours', {}).get('outline', '#000000')
			nations = element.get('nations', [])
			sub_arr = [fill, outline, nations]
			arr.append(sub_arr)

print(f'Fetching marker_earth.json from {marker_URL}..')

response = requests.get(marker_URL)
if response.status_code != requests.codes.ok:
	print('The response status is not OK. Try later, exiting..')
	exit()

data = response.json()
areas = data['sets']['townyPlugin.markerset']['areas']
towns = []
# Regex pattern to extract nations
nationPattern = r'>(.*?)<'

for area in areas:
	fill = areas[area]['fillcolor']
	# Don't draw shop areas
	if fill == '#00FF00':
		continue

	outline = areas[area]['color']
	x = areas[area]['x']
	z = areas[area]['z']
	town = areas[area]['label']

	# Calculate width and height for image
	if corners:
		height = round(abs(corners[0][1] - corners[1][1]) / scale)
		coords = [(round((x[i] - corners[0][0]) / scale), round((z[i] - corners[0][1]) / scale)) for i in range(len(x))]
	else:
		coords = [(round((x[i] + 33280) / scale), round((z[i] + 16640) / scale)) for i in range(len(x))]

	if mode != 'default':
		desc = areas[area]['desc']
		desc = desc.replace(' (Shop)', '')

		# If town isn't in nation
		if '()</span><br /> Mayor' in desc:
			fill = outline = '#000000'
		else:

			# Extract nation from town's description
			start_idx = desc.find('(')
			end_idx = desc.find(')')
			if start_idx != -1 and end_idx != -1:
				nation = desc[start_idx + 1:end_idx]

			# If nation still contains </a>
			if '</a>' in nation:
				nation = re.search(nationPattern, nation).group(1)

			if mode == 'alliance':
				fill = outline = '#000000'
			if mode == 'meganation':
				if fill == '#3FB4FF': fill = outline = '#000000'

			for alliance in arr:
				if nation in alliance[2]:
					fill = alliance[0]
					outline = alliance[1]

	town = {'fill': fill, 'outline': outline, 'coords': coords}
	towns.append(town)

if corners:
	width = round(abs(corners[0][0] - corners[1][0]) / scale)
	height = round(abs(corners[0][1] - corners[1][1]) / scale)
else:
	width = round(66360 / scale)
	height = round(33148 / scale)

print(f'Creating image of {width} x {height} px in current directory..')

image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)
[ draw.polygon(town['coords'], hex_to_rgba(town['fill'], 51), hex_to_rgba(town['outline'], 255)) for town in towns ]
file_name = f'{mode}-{world}-{int(time.time())}.png'
image.save(file_name)
print(f'Saved image as {file_name}, exiting..')
