from bs4 import BeautifulSoup
import urllib2
import json
from time import sleep
from pprint import pprint

base_url = 'http://espn.go.com/golf/leaderboard?tournamentId='

def get_soup(url, param):
  soup = None
  try:
    page = urllib2.urlopen(url + str(param))
  except urllib2.URLError:
    return soup

  return BeautifulSoup(page)

def has_results(soup):
  return len(soup.find(id='regular-leaderboard').contents) > 1

def is_marked_complete(soup):
  return soup.find(text='Complete')

if __name__ == '__main__':

  #load up all the tourn ids
  f = open('../data/tourn-ids.json')
  data = json.load(f) #data is a dict

  
  for id in data['2013-14']:
    soup = get_soup(base_url, id)

    if has_results(soup) and is_marked_complete(soup, id):
      pass
    #print id, data['2013-14'][id]
  
    sleep(1)
   

  #if has_results(soup):
    


