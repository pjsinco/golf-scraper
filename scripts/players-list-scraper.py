"""
This program scrapes the names and espn ids of all golfers
"""

from bs4 import BeautifulSoup
import urllib2
import time
import json
import sys
from pprint import pprint

# tr[class*="player-"]

"""
Returns a dict of player info
"""
def get_player_info(id):
  return True


url = 'http://espn.go.com/golf/players'

page = urllib2.urlopen(url)
content = page.read()
soup = BeautifulSoup(content)
page.close()

player_rows = soup.select('tr[class*="player-"]')
#print len(players), type(players)

players = {}

for player in player_rows:
  player_info = {}
  id_class = player['class']
  if id_class[-1].startswith('player'):
    id = id_class[-1].split('-')[-1]
    name = player.select('td > a')[0].get_text()
    split_names = name.split(', ')
    f_name = split_names[-1]
    l_name = split_names[0]

    player_info['f_name'] = f_name
    player_info['l_name'] = l_name
    
    players[id] = player_info

  print players
  sys.exit()

with open('../data/players.json', 'w') as outfile:
    json.dump(players, outfile)

