# /// script
# dependencies = [
#    "requests",
#    "Pillow",
#    "munch",
#    "aiohttp"
# ]
# ///

import sys
import re
import requests
import time
import runpy
from PIL import Image, ImageDraw
from munch import Munch
from aiohttp import ClientSession, ClientTimeout
import asyncio

async def get_world():
	global world, link
	async with ClientSession() as session:
		try:
			async with session.get(f'{link}/tiles/settings.json', timeout=ClientTimeout(total=3)) as response:
				if response.status != 200:
					exit('The map website isn\'t responding (try later), exiting..\n')
				settings = await response.json()
				settings = Munch.fromDict(settings)
				print('\nAvailable worlds:')
				options = []
				worlds = []
				for i, _world in enumerate(settings.worlds):
					options.append(f'  {i+1}. {_world.name}')
					worlds.append(_world.name)
				print('\n'.join(options))
		except:
			exit('Response or website URL is invalid, exiting..\n')

		try:
			world = int(input('Enter your choice (number): '))
			if world < 1: raise Exception
			world = worlds[world-1]
		except:
			exit('Input should be one of possible choices, exiting..\n')

def hex_to_rgba(hex_string, alpha):
	try: r, g, b = (int(hex_string[i:i+2], 16) for i in range(1, 7, 2))
	except: r, g, b = 255, 255, 255
	return (r, g, b, alpha)

def round_to_16(number):
	return round(number / 16) * 16

print('')
print('Dynmapper by 3meraldK')

link = input('Enter the map URL: ')
link = ''.join(re.split('(/)', link)[0:5])
if link.startswith('https://') == False:
	exit('The map URL should start with https://, exiting..\n')

asyncio.run(get_world())

print(f'\nHow many blocks should be 1 pixel on image?')
try:
	scale = int(input('Enter your choice: '))
	if scale <= 0: raise Exception
except:
	exit('Input should be a positive number, exiting..\n')

print('')
corners = []
try:
	for (i, x) in [(1, 'x'), (1, 'z'), (2, 'x'), (2, 'z')]:
		corners.append(int(input(f'Enter corner {i} {x}-coordinate: ')))
except:
	exit('Corner coordinates should be whole numbers, exiting..\n')

min_x = min(corners[0], corners[2])
min_z = min(corners[1], corners[3])
width = round(abs(corners[0] - corners[2]) / scale)
height = round(abs(corners[1] - corners[3]) / scale)

if width <= 0 or height <= 0:
	exit('Scale, width, and height must be positive numbers, exiting..\n')

print('')
print('If you want to use a plugin, enter the script\'s full name, for example script.py.')

choice = input('Otherwise enter "n". Enter your choice: ')
plugin_script = None if choice.lower() == 'n' else choice
if plugin_script:
	print('Enter script parameters separated by space or leave blank.')
	plugin_args = input('Enter your choice: ').split(' ')

response = requests.get(f'{link}/tiles/{world}/markers.json')

if response.status_code != requests.codes.ok:
	exit('The map website isn\'t responding (try later), exiting..\n')

data = Munch.fromDict(response.json())

try:
	markers = list(filter(lambda layer: layer.id == 'towny', data))[0].markers
except:
	exit('This world doesn\'t have Towny layer, exiting..\n')

towns = list(filter(lambda marker: marker.type == 'polygon', markers))

if plugin_script:
	try:
		sys.argv = [plugin_script] + plugin_args
		shared_var = {'towns': towns}
		runpy.run_path(plugin_script, init_globals=shared_var)
		towns = shared_var.get('towns', towns)
	except Exception as e:
		exit(f'Unexpected error during execution of the plugin: {e}, exiting..\n')

try:
	image = Image.new(mode='RGBA', size=(width, height))
except:
	exit('Can\'t handle such big image, exiting..\n')

draw = ImageDraw.Draw(image)

for town in towns:
	fill = hex_to_rgba(town.fillColor if getattr(town, 'fillColor', None) else '#89c500', 51)
	outline = hex_to_rgba(town.color if getattr(town, 'color', None) else '#89c500', 255)
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

now = int(time.time())
file_name = f'dynmapper-{now}.png'

try:
	image.save(file_name)
except:
	exit('Could not save the image, exiting..\n')

print('')
print(f'Saved image as {file_name}, exiting..\n')
