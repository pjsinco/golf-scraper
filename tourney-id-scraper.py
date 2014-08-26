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
#  response = urllib2.urlopen(url)
#  content = response.read()
#  soup = BeautifulSoup(content)
  
#  rows = soup.select('.tablehead tr[class*="row"]');

  row = '\
    <tr class="oddrow"> \
      <td><nobr>Aug 29 - Sep 1</nobr></td> \
      <td><a href="/golf/leaderboard?tournamentId=1343">Deutsche \
        Bank Championship</a><br><em>TPC of Boston, Norton, MA</em></br> \
      </td> \
      <td>NBC/TGC</td> \
      <td> \
        <a href="http://espn.go.com/golf/player/_/id/576/henrik-stenson"> \
          Henrik Stenson \
        </a> \
      </td> \
      <td>$8,000,000</td> \
    </tr>'

  soup = BeautifulSoup(row)
  print len(soup.select('td'))
  print soup.select('td')
  print soup.select('td')[3]
  print soup.select('td')[3].get_text()

  #print len(rows)
  #print type(rows)

  for x in range(0, len(rows)):
    print x

  #for table in tables:
  #for x in range(0, len(tables)):
    #print len(tables[x])
  
except:
  pass



