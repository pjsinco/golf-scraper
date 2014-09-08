from bs4 import BeautifulSoup
from bs4 import element
import urllib2
from time import sleep
import re
from pprint import pprint
import json

class YahooPGAScraper:

  def __init__(self):
    self.url_base = 'http://sports.yahoo.com/golf/pga'

  """
  Returns a BeautifulSoup object for the given url
  """
  def get_soup(self, url):
    soup = None 
    try:
      page = urllib2.urlopen(url)
      soup = BeautifulSoup(page)
      page.close()
    except urllib2.URLError: 
      return soup

    return soup


  """
  Returns the passed string with a replacement
  for unicode-encoded nonbreaking space (%nbsp;)
  """
  def nbsp_formatter(self, string):
    return string.replace(u'\xa0', '')


  """
  Returns the tournament results as a dict
  """
  def get_tourn_results(self, year, t_id):
    url = '%s/leaderboard/%s/%s' % \
      (self.url_base, str(year), str(t_id))

    results = {}

    try:
      soup = self.get_soup(url)      
    except urllib2.URLError:
      return results  

    # find out what fields are showing in on this results page
    fields_avail = []
    
    #get header row; sometimes there are 2--we want the last
    t_headers = soup\
      .find(id='leaderboardtable')\
      .find('table')\
      .find('thead')\
      .find_all('tr')[-1]

    for t_header in t_headers:
      if type(t_header) is element.Tag:
        fields_avail.append(unicode(t_header.a.string))

    rows = soup\
      .find(id='leaderboard')\
      .find(id='leaderboardtable')\
      .find('table')\
      .find('tbody')\
      .find_all('tr')

    if len(rows) == 0:
      return results

    for i in range(0, len(rows)):
      player = {}
      fields = rows[i].find_all('td')
      for j in range(0, len(fields_avail)):
        if fields_avail[j] == 'Purse':
          player[fields_avail[j]] =\
            unicode(fields[j].string).strip().split('$')[-1]
        elif fields_avail[j] == 'Name':
          player[fields_avail[j]] = unicode(fields[j].a.string).strip()
          player[u'player_id'] = unicode(fields[j].a['href'].split('/')[-1]) 
        else:
          player[fields_avail[j]] = unicode(fields[j].string).strip()

      results[i] = player
        
    return results      

    
  


  """
  Returns a dict of with key, value of--
    id: name
  """
  def get_schedule(self, year):
    url = self.url_base + '/schedule' + '?season=' + str(year)
    schedule = {}

    try:
      soup = self.get_soup(url)
    except urllib2.URLError: 
      return schedule

    purse_re = re.compile('Purse:')

    e_params = ['name', 'date', 'course', 'purse']

    try:
      events = soup.find_all('td', class_='event')
      for e in events:
        event = dict.fromkeys(e_params)

        # canceled tournaments won't have an a tag
        if e.a:
          event['name'] = unicode(e.a.string)
          id = unicode(e.a['href']).split('/')[-1]
          event['date'] = self.nbsp_formatter(
            e.find_previous_sibling('td').string
          )
        else:
          event['name'] = unicode(e.next)
          id = None
          event['date'] = self.nbsp_formatter(
            e.find_previous_sibling('td').next.string
          )
        
        event['course'] = unicode(e.find_next_sibling('td').next)
        event['purse'] = \
          unicode(e.find(text=purse_re)).split('$')[-1].replace(',', '')

        schedule[id] = event

    except:
      pass 
    
    return schedule


  """
  Accepts a dict and writes it is as json into the outfile
  """
  def write_json_to_file(self, data, outfile):
    
    if type(data) != dict:
      return False

    json.dump(
      data, outfile, indent=4, separators=(',', ': ')
    )
    



if __name__ == '__main__':
  scraper = YahooPGAScraper()
#  for year in range(1977, 2015):
#    schedule = scraper.get_schedule(year)
#    f = open('../data/tournaments-yahoo/tourn-' + \
#      str(year) + '.json', 'w+')
#    scraper.write_json_to_file(schedule, f)
#    f.close()

  infile = open('../data/tournaments-yahoo/tourn-1977.json')
  data = json.load(infile)
  for key in data.keys():
    outfile = open(
      '../data/tourn-1977/tourn-1977-' + key + '.json', 'w+')
    scraper.\
      write_json_to_file(\
        scraper.get_tourn_results('1977', key), outfile\
      )
  
  #pprint(scraper.get_tourn_results('1977', '4'))
  #pprint(scraper.get_tourn_results('1977', '6'))  #incomplete results
  #pprint(scraper.get_tourn_results('1977', '45')) #empty results
