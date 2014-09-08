import yahoo_scrape as ys
import json
from pprint import pprint

if __name__ == '__main__':

  scraper = ys.YahooPGAScraper()
  
  #get results for all 1978 tournaments
  infile = open('../data/tournaments-yahoo/tourn-1978.json')
  data = json.load(infile)
  for key in data.keys():
    outfile = open(
      '../data/tourn-1978/tourn-1978-' + key + '.json', 'w+')
    results = scraper.get_tourn_results('1978', key)
    scraper.write_json_to_file(results, outfile)

  #pprint(scraper.get_tourn_results('1977', '4'))

  # has 'projected cut' row
  #pprint(scraper.get_tourn_results('1977', '33')) 

  #pprint(scraper.get_tourn_results('1977', '6'))  #incomplete results
  #pprint(scraper.get_tourn_results('1977', '45')) #empty results
