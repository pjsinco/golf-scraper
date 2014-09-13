import yahoo_scrape as ys
import json
import csv
import sys
from pprint import pprint

scraper = ys.YahooPGAScraper()

#infile = open('../data/tournaments-yahoo/tourn-1981.json')
#data = json.load(infile)

#for key in data.keys():

results = scraper.get_tourn_results('2013', 26)

with open('../test-csv.csv', 'w+') as csv_file:
  fieldnames = results[0].keys()
  csv_writer = csv.DictWriter(csv_file, fieldnames)

  # write header row
  csv_writer.writerow(dict((fn, fn) for fn in fieldnames))

  for row in results:
      csv_writer.writerow(row)


