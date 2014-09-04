"""
This program finds tournaments and groups them. 
For ex., all the Western Opens and BMW Championships, which the 
tournament was later renamed, are placed in one group.

"""
from bs4 import BeautifulSoup
import urllib2
import time
import json
import sys
from pprint import pprint

"""
Returns the name of the tournament
"""
def get_tourney_name(id):
  f = open('../data/tourney-ids.json', 'r')
  data = json.load(f) # data is a dict
  for year in data.keys():
    for tourney_id in data[year]:
      if tourney_id == str(id):
        return data[year][tourney_id]
        

url = 'http://espn.go.com/golf/leaderboard?tournamentId='

f = open('../data/tourney-ids.json', 'r')
data = json.load(f)

tourneys_all = {}

#print data['2001'].keys()
for id in data['2013-14'].keys():

  tourney = {}
  tourneys_all[id] = tourney
  
  print 'Gathering info on id: ' + id

  try:
    response = urllib2.urlopen(url + id)
    content = response.read()
    soup = BeautifulSoup(content)

    prev_years = soup.select('#prev-years > option');

    # get the ids of the tournament in previous years
    for line in prev_years:
      tourney_id = line['value']
      tourney_year = line.get_text()
      tourney[tourney_year] = {}
      tourney[tourney_year]['id'] = tourney_id
      tourney[tourney_year]['name'] = get_tourney_name(tourney_id)

    tourneys_all[id] = tourney

  except Exception, e:
    print str(e)
    print "Error gathering info on " + id

  finally:
    time.sleep(1)

with open('../data/tournaments.json', 'w') as outfile:
    json.dump(tourneys_all, outfile)
    

