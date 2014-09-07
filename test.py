import unittest
import sys

# include our file in Python path
# http://stackoverflow.com/questions/4383571/
#  importing-files-from-different-folder-in-python
sys.path.append('/Users/pj/Sites/golf-scraper/scripts')

import tourney_results_scraper as trs

class BaseTest(unittest.TestCase):
  
  def setUp(self):
    self.good_url = \
      'http://espn.go.com/golf/leaderboard?tournamentId='
    self.bad_url = \
      'http://espn.go.com/xolf/leaderboard?tournamentId='

    self.good_param = '1351'

    self.id_has_results_true = '1351'

    # 2001 WGC-Accenture Match Play Championship
    self.id_has_results_false = '1'
  
  def test_get_soup(self):
    self.assert_(trs.get_soup(self.good_url, self.good_param) is not None)
    self.assert_(trs.get_soup(self.bad_url, self.good_param) is None)
  
  def test_has_results(self):
    self.assertEquals(
      trs.has_results(
        trs.get_soup(self.good_url, self.id_has_results_true) 
      ),
      True
    )
  
    self.assertEquals(
      trs.has_results(
        trs.get_soup(self.good_url, self.id_has_results_false) 
      ),
      False
    )

if __name__ == '__main__':
  unittest.main()
