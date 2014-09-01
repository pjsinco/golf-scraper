from bs4 import BeautifulSoup
import urllib2
import time
import json
import sys
from pprint import pprint

url = 'http://espn.go.com/golf/leaderboard?tournamentId='
tourney_data_keys = [
  'name', 'date', 'venue', 'purse', 'winner'
]

# selector for winner:
# jQuery('table.leaderboard > tbody > tr:first-child > td.player > a').text()

f = open('../data/tourney-ids.json', 'r')
data = json.load(f)

tourneys = {}

#print data['2001'].keys()
for year in data.keys():

  tourneys_in_year = {}
  tourneys_in_year[year] = {}

  for id in data[year].keys():
    tourney_data = dict.fromkeys(tourney_data_keys)
  
    #print id, data['2001'][id]
    try:
      response = urllib2.urlopen(url + id)
      content = response.read()
      soup = BeautifulSoup(content)
  
      # set tourney properties
      tourney_data['name'] = data[year][id]
  
      date = soup.select('h3.date')
      if date:
        tourney_data['date'] = date[0].get_text()
  
      venue = soup.select('h3.venue')
      if venue:
        tourney_data['venue'] = venue[0].get_text()
  
      purse = soup.select('.tourney-detail-strip p span')
      if purse:
        tourney_data['purse'] = purse[0].get_text()
  
      winner =tourney_data['winner'] = \
        soup.select('table.leaderboard > tbody > tr:first-child > \
        td.player > a')
      if winner:
        tourney_data['winner'] = winner[0].get_text()
      
      pprint(tourney_data)
      tourneys[year] = tourneys_in_year
      
    except Exception, e:
      print str(e)
      print "Error gathing info on " + id
      pass
  
    time.sleep(1)
pprint(tourneys)
