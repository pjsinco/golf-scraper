"""
This program scrapes the names and espn ids of all golfers
"""

from bs4 import BeautifulSoup
import urllib2
import time
import json
import sys
from pprint import pprint
import re

# tr[class*="player-"]

"""
Parses the birthdate and returns as yyyy-mm-dd.
Expects format to be, for ex., 'August 17, 1980'
"""
def parse_birth_date(birthdate):
  date = time.strptime(birthdate, '%B %d, %Y')
  return '%d-%d-%d' % (date.tm_year, date.tm_mon, date.tm_mday)
  

"""
Returns a dict of player info
"""
def get_player_info(id):
  url = 'http://espn.go.com/golf/player/_/id/'
  page = urllib2.urlopen(url + id)
  soup = BeautifulSoup(page)

  keys = [
    'country',
    'pga_debut',
    'college',
    'dob',
    'birthplace',
    'swings',
    'turned_pro',
  ]
  info = dict.fromkeys(keys)

  bio = soup.find(class_='player-bio')

  swings_re = re.compile('Swings:')
  turned_pro_re = re.compile('Turned Pro:')

  try :
    info['country']     = \
      unicode(bio.find(class_='general-info')\
        .find(class_='first').string)
  except Exception: 
    pass

  try: 
    info['pga_debut']   = \
      unicode(bio.find(text='PGA Debut').next).strip()
  except Exception:
    pass

  try:
    info['college']     = \
      unicode(bio.find(text='College').next).strip()
  except Exception:
    pass

  try: 
    info['dob']         = parse_birth_date(\
      unicode(bio.find(text='Birth Date').next).split('(')[0].strip()
    )
  except Exception:
    pass

  try:
    info['birthplace']  = \
      unicode(bio.find(text='Birthplace').next).strip()
  except Exception:
    pass

  try:
    info['swings']      = \
      unicode(bio.find('li', text=swings_re)\
        .string.split(': ')[-1]).strip()
  except Exception:
    pass

  try:
    info['turned_pro']  = \
      unicode(bio.find('li', text=turned_pro_re)\
        .string.split(': ')[-1]).strip()
  except Exception:
    pass

  return info

url = 'http://espn.go.com/golf/players'

page = urllib2.urlopen(url)
content = page.read()
soup = BeautifulSoup(content)
page.close()

player_rows = soup.select('tr[class*="player-"]')
#print len(players), type(players)

players = {}

with open('../data/players.json', 'a') as outfile:
  # delete file contents
  outfile.truncate()

  # iterate over each player on the page
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
      
      
      players[id] = dict(player_info.items() + \
        get_player_info(id).items())
  
    print players[id]


    time.sleep(1)

  json.dump(players[id], outfile, indent=4, separators=(',', ': '))
