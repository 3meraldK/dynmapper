# /// script
# dependencies = [
#    "requests",
#    "Pillow",
#    "munch"
# ]
# ///
# astral-sh/uv support above

import sys
import re
import requests
import time
import runpy
from PIL import Image, ImageDraw
from munch import Munch

default_color = '#89c500'

# Utility functions
def hex_to_rgba(hex_string, alpha):
	try: r, g, b = (int(hex_string[i:i+2], 16) for i in range(1, 7, 2))
	except: r, g, b = 255, 255, 255
	return (r, g, b, alpha)

def round_to_16(number):
	return round(number / 16) * 16

print('')
print('Dynmapper by 3meraldK')

# Validating parameters
if len(sys.argv) < 8:
	exit('Usage (read repository\'s readme): python dynmapper.py [map url]' +
		'[world name] [scale] [corner coordinates] <plugin> <plugin arguments>\n')

link = ''.join(re.split('(/)', sys.argv[1])[0:5])
if link.startswith('https://') == False:
	exit('The [map url] is invalid, it should start with https://, exiting..\n')

world = sys.argv[2]

try:
	scale = float(sys.argv[3])
	corners = sys.argv[4:8]
	for i, corner in enumerate(corners):
		corners[i] = int(corner)
except ValueError:
	exit('Command parameters [corner coordinates] or [scale] should be whole numbers, exiting..\n')

min_x = min(corners[0], corners[2])
min_z = min(corners[1], corners[3])
width = round(abs(corners[0] - corners[2]) / scale)
height = round(abs(corners[1] - corners[3]) / scale)

if scale <= 0 or width <= 0 or height <= 0:
	exit('Scale, width, and height must be positive numbers, exiting..\n')

plugin_script = sys.argv[8] if len(sys.argv) > 8 else None
plugin_args = [plugin_script] + sys.argv[9:] if plugin_script else []

# Downloading & processing the town layer
response = requests.get(f'{link}/tiles/{world}/markers.json')

if response.status_code != requests.codes.ok:
	exit('The response status is not OK. Try later, exiting..\n')

data = Munch.fromDict(response.json())

try:
	markers = list(filter(lambda layer: layer.id == 'towny', data))[0].markers
except IndexError:
	exit('This world doesn\'t have id:towny layer, exiting..\n')

towns = list(filter(lambda marker: marker.type == 'polygon', markers))

if plugin_script:
	try:
		sys.argv = plugin_args
		shared_var = {'towns': towns}
		runpy.run_path(plugin_script, init_globals=shared_var)
		towns = shared_var.get('towns', towns)
	except Exception as e:
		exit(f'Unexpected error during execution of the plugin: {e}, exiting..\n')

# Drawing the final image
try:
	image = Image.new(mode='RGBA', size=(width, height))
except MemoryError:
	exit('Can\'t handle such big image, exiting..\n')
draw = ImageDraw.Draw(image)

for town in towns:
	fill = hex_to_rgba(town.fillColor if getattr(town, 'fillColor', None) else default_color, 51)
	outline = hex_to_rgba(town.color if getattr(town, 'color', None) else default_color, 255)
	for polygon in town.points:
		try:
			coords = []
			for vertex in polygon[0]:
				x = round_to_16(vertex.x)
				z = round_to_16(vertex.z)
				coords.append(round((x - min_x) / scale))
				coords.append(round((z - min_z) / scale))
			draw.polygon(coords, fill, outline)
		except:
			pass

try:
	now = int(time.time())
	file_name = f'dynmapper-{now}.png'
	image.save(file_name)
	print(f'Saved image as {file_name}, exiting..\n')
except PermissionError:
	exit('Insufficient permissions to save the image, exiting..\n')