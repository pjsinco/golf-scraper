import yahoo_scrape as ys
import sys
import json
import csv
import time
from pprint import pprint

def main():
  scraper = ys.YahooPGAScraper()
  
  #get results for all 2013 tournaments
  infile = open('../data/tournaments-yahoo/tourn-2013.json')
  data = json.load(infile)

  for key in data.keys():
    results = scraper.get_tourn_results('2013', key)
    pprint(results)

    with open(
        '/Users/pj/Sites/golf-scraper/data/tourn-2013/tourn-2013-' + 
        key + '.csv', 'w+'
      ) as csv_file:

      if results:
        fieldnames = results[0].keys()
      else:
        fieldnames = []

      csv_writer = csv.DictWriter(csv_file, fieldnames)

      # write header row
      try:
        csv_writer.writerow(dict((fn, fn) for fn in fieldnames))
      except UnicodeEncodeError:
        pass

      for row in results:
        csv_writer.writerow(row)

    time.sleep(1)
  #pprint(scraper.get_tourn_results('1978', '45')) # tricky

  #pprint(scraper.get_tourn_results('1977', '4'))

  # has 'projected cut' row
  #pprint(scraper.get_tourn_results('1977', '33')) 

  #pprint(scraper.get_tourn_results('1977', '6'))  #incomplete results
  #pprint(scraper.get_tourn_results('1977', '45')) #empty results

if __name__ == '__main__':
  main()
