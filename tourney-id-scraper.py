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
  
  rows = soup.select('.tablehead tr[class*="row"]');

  # testing here ------------------

  # row = '\
  #   <tr class="oddrow"> \
  #     <td><nobr>Aug 29 - Sep 1</nobr></td> \
  #     <td><a href="/golf/leaderboard?tournamentId=1343">Deutsche \
  #       Bank Championship</a><br><em>TPC of Boston, Norton, MA</em></br> \
  #     </td> \
  #     <td>NBC/TGC</td> \
  #     <td> \
  #       <a href="http://espn.go.com/golf/player/_/id/576/henrik-stenson"> \
  #         Henrik Stenson \
  #       </a> \
  #     </td> \
  #     <td>$8,000,000</td> \
  #   </tr>'

  # soup = BeautifulSoup(row)
  # print len(soup.select('td'))
  # print soup.select('td')
  # print soup.select('td')[3]
  # print soup.select('td')[3].get_text()

  # finished testing ------------------

  print type(rows)
  print len(rows)

  #for x in range(0, len(rows)):
  for row in rows:
    #print row
    print 'row is a %s' % type(row)
    print '\tits name is %s' % row.name
    print '\tits class is %s' % row['class']
    print '\tits attrs are: %s' % row.attrs
    print '\tit has %d <td> elems' % len(row.find_all('td'))
    print type(row.find_all('td'))
    print len(row.select('td'))
    print '\n'
    #row_soup = BeautifulSoup(row)
    #print len(row_soup.select('td'))

  #for table in tables:
  #for x in range(0, len(tables)):
    #print len(tables[x])
  
except:
  pass



