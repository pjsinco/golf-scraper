from bs4 import BeautifulSoup
import urllib2
import time
import json
import pprint

#base_url = 'http://espn.go.com/golf/leaderboard?tournamentId='
url = 'http://espn.go.com/golf/schedule/_/year/'

year_range = range(2001, 2013)
year_range.append('2013-14')
years = []
for y in year_range:
  years.append(str(y)) # turn the ints into strings

tourneys_all = {} 

for year in years:
  try:
    tourneys_year = {}
    response = urllib2.urlopen(url + year)
    content = response.read()
    soup = BeautifulSoup(content)
    response.close()

    # example target link: 
    # http://espn.go.com/golf/leaderboard?tournamentId=1319
    tourney_hrefs = soup.select('a[href*="tournament"]')
    
    for href in tourney_hrefs:
      tourney_name = href.get_text()
      tourney_id  = href.get('href').split('=')[-1] # id is last item
      tourneys_year[tourney_id] = tourney_name
    
  except:
    pass

  finally:
    tourneys_all[year] = tourneys_year
    with open ('tourney-ids.json', 'w') as outfile:
      json.dump(tourneys_all, outfile)


