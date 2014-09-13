from bs4 import BeautifulSoup
from bs4 import element
import urllib2
import re
from pprint import pprint
import json
import sys
import csv

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


  def process_year(self, year):
    pass

  """
  Returns the passed string with a replacement
  for unicode-encoded nonbreaking space (%nbsp;)
  """
  def nbsp_formatter(self, string):
    return string.replace(u'\xa0', '')


  """
  Returns the tournament results as a list, 
  with a dictionary for each row
  """
  def get_tourn_results(self, year, t_id):
    # give the user some feedback
    print('Processing %s, id #%s...' %
      (str(year), str(t_id)))

    url = '%s/leaderboard/%s/%s' % \
      (self.url_base, str(year), str(t_id))

    results = []

    try:
      soup = self.get_soup(url)      
    except urllib2.URLError:
      return results  

    # find out what fields are showing in on this results page
    fields_avail = []
    
    #get header row; sometimes there are two--we want the last
    t_headers = soup\
      .find(id='leaderboardtable')\
      .find('table')\
      .find('thead')\
      .find_all('tr')[-1]

    # grab each header field; we will iterate through these
    for t_header in t_headers:
      if type(t_header) is element.Tag:
        if t_header.a:
          fields_avail.append(unicode(t_header.a.string))
        elif t_header.string:
          fields_avail.append(unicode(t_header.string))

    # these are the rows of the tournament results
    rows = soup\
      .find(id='leaderboard')\
      .find(id='leaderboardtable')\
      .find('table')\
      .find('tbody')\
      .find_all('tr')

    # nothing there, so let's get out of here
    if len(rows) == 0:
      return results

    # ok, let's go through the rows one by one
    for i in range(0, len(rows)):
      player = {}
      fields = rows[i].find_all('td')
      if len(fields) < 2: #this row is unusual; prolly don't need it
        continue
      for j in range(0, len(fields_avail)):
        # we need to clip the $ off the purse
        if fields_avail[j] == 'Purse':
          player[fields_avail[j]] =\
            ''.join( unicode(fields[j].string)\
              .strip()\
              .split('$')[-1]\
              .split(','))

        # we need to grab the player's id
        elif fields_avail[j] == 'Name':

          # fields[j].next is a string that's not part of the link;
          # a playoff winner, denoted by '-x', is what we're 
          # trying to capture
          player[fields_avail[j]] = \
            unicode(
              ''.join(
                (fields[j].next, fields[j].a.string)
              )
              .strip()
              )
          player[u'player_id'] = \
            unicode(fields[j].a['href'].split('/')[-1]) 
        else:
          player[fields_avail[j]] = unicode(fields[j].string).strip()

      results.append(player)
        
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
  Accepts a list of dicts and writes it as csv into the csvfile
  """
  def write_csv_to_file(self, data, csvfile):
    if type(data) != dict:
      return False

    

  """
  Accepts a dict and writes it is as json into the outfile
  """
  def write_json_to_file(self, data, outfile):
    
    if type(data) != dict:
      return False

    json.dump(
      data, outfile, indent=4, separators=(',', ': ')
    )
