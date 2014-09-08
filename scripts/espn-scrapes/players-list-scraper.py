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

did_not_get = []

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

  try:
    url = 'http://espn.go.com/golf/player/_/id/'
    page = urllib2.urlopen(url + id)
    soup = BeautifulSoup(page)
    page.close()

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

  except urllib2.URLError:
    did_not_get.append(id)

  finally:
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
  outfile.truncate(0)

  # iterate over each player on the page
  #for i in range(0, 2): # debug
  for player in player_rows:
    player_info = {}
    id_class = player['class']
    #id_class = player_rows[i]['class'] # debug
    if id_class[-1].startswith('player'):
      id = id_class[-1].split('-')[-1]
      name = player.select('td > a')[0].get_text()
      #name = player_rows[i].select('td > a')[0].get_text() # debug
      split_names = name.split(', ')
      f_name = split_names[-1]
      l_name = split_names[0]
  
      player_info['f_name'] = f_name
      player_info['l_name'] = l_name
      player_info['full_name'] = "%s %s" % (f_name, l_name)
      
      
      # player info is inconsistent; let's skip
      #players[id] = dict(player_info.items() + \
        #get_player_info(id).items())
  
      players[id] = player_info

    print players[id]

  json.dump(players, outfile, indent=4, separators=(',', ': '))

print did_not_get
