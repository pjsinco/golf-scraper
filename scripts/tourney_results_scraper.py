import yahoo_scrape as ys
import json
import time
from pprint import pprint

def main():
  scraper = ys.YahooPGAScraper()
  
  #get results for all 1978 tournaments
  infile = open('../data/tournaments-yahoo/tourn-1981.json')
  data = json.load(infile)
  for key in data.keys():
    outfile = open(
      '/Users/pj/Sites/golf-scraper/data/tourn-1981/tourn-1981-' + key + '.json', 'w+')
    results = scraper.get_tourn_results('1981', key)
    scraper.write_json_to_file(results, outfile)
    time.sleep(1)

  #pprint(scraper.get_tourn_results('1978', '45')) # tricky

  #pprint(scraper.get_tourn_results('1977', '4'))

  # has 'projected cut' row
  #pprint(scraper.get_tourn_results('1977', '33')) 

  #pprint(scraper.get_tourn_results('1977', '6'))  #incomplete results
  #pprint(scraper.get_tourn_results('1977', '45')) #empty results

if __name__ == '__main__':
  main()
