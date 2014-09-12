import yahoo_scrape as ys
import sys
import json
import csv
import time
from pprint import pprint

def main():
  scraper = ys.YahooPGAScraper()
  
  #get results for all 1978 tournaments
  infile = open('../data/tournaments-yahoo/tourn-1977.json')
  data = json.load(infile)

  for key in data.keys():
    results = scraper.get_tourn_results('1977', key)
    pprint(results)

    if results:
      with open(
          '/Users/pj/Sites/golf-scraper/data/tourn-1977/tourn-1977-' + 
          key + '.csv', 'w+'
        ) as csv_file:
        fieldnames = results[0].keys()
        csv_writer = csv.DictWriter(csv_file, fieldnames)

        # write header row
        csv_writer.writerow(dict((fn, fn) for fn in fieldnames))

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
