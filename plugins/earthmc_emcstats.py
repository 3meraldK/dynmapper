# Last update on 13 October 2026
# Will go outdated sooner or later... ¯\_(ツ)_/¯

import sys
import re
import requests
from munch import Munch

apiURL = 'https://emcstats.bot.nu/nostra/alliances'
print('EarthMC Stats plugin by 3meraldK')

alliance_type = sys.argv[1] if len(sys.argv) > 1 else None
if alliance_type not in ['mega', 'pact']:
    raise Exception('Wrong alliance type (mega, pact)')
if alliance_type == 'mega': alliance_type = r'mega'
else: alliance_type = r'pact|org'

response = requests.get(apiURL)

if response.status_code != requests.codes.ok:
	exit('The response status is not OK. Try later')

def is_correct_type(alliance):
    match = re.search(alliance_type, alliance.type)
    return match is not None

alliances = Munch.fromDict(response.json())
alliances = list(filter(is_correct_type, alliances))

for town in towns:
    town.fillColor = '#000000'
    town.color = '#000000'
    nation = re.search(r'\((?:Member|Capital) of (.*?)\)', town.tooltip)
    if not nation: continue
    nation = nation.group(1)
    found_alliance = list(filter(lambda alliance: nation in alliance.ownNations, alliances))
    if not found_alliance: continue
    alliance = found_alliance[0]
    if not getattr(alliance.optional, 'colours', None): continue
    town.fillColor = '#' + alliance.optional.colours.fill
    town.color = '#' + alliance.optional.colours.outline