from bs4 import BeautifulSoup
import urllib2
import time
import json
import pprint

#base_url = 'http://espn.go.com/golf/leaderboard?tournamentId='
url = 'http://espn.go.com/golf/schedule'

#set up our dictionary
tourney = {}

try:
  response = urllib2.urlopen(url)
  content = response.read()
  soup = BeautifulSoup(content)
  
  # example target link: 
  # http://espn.go.com/golf/leaderboard?tournamentId=1319
  tourney_hrefs = soup.select('a[href*="tournament"]')

  tourneys = {}

  for href in tourney_hrefs:
    tourney = {}
    tourney['name'] = href.get_text()
    tourney['id'] = href.get('href').split('=')[-1] # id is last item
    tourneys[tourney['id']] = tourney
    
except:
  pass

print len(tourneys)


