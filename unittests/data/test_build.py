import os
import unittest

import espn_api.football as fb
import pandas as pd

from src.core.data.build import build_draft, build_roster


curr_dir = os.path.dirname(os.path.realpath(__file__))


class DataTest(unittest.TestCase):

    def setUp(self) -> None:
        self.ff_league = fb.League(
            league_id=956882, year=2022,
            espn_s2='AEC1zjIvilzU%2BoF8LkcATCDGm9rgUNsGkxmiIfYLdFoihpMWoCVQgG%2FniIi0G2GoaHrJJYy1r'
                    'C8BUBELl1oVpO6nwsfY357qzJy9AhNaOx4T2YSNJaL1b8%2FurIUgy8BmuLQZQVKABzc%2BsZudsW'
                    'oB48F4iiomhKBHeE3Ei%2FA6uaH3kc5bXAw1kGibd8oKKDnuxRy4g%2BkXUGb3u6U2DGAVVoW1Ycd'
                    '%2F9cRHlYLZR9hyTsPa%2B7AKzCkgAFbFE43xjbGlZ3TEf4SreN6XkjRKN9ZPtcOX',
            swid='{60221347-8376-4C38-9B79-143C183774C6}')

    def test_roster(self):
        # complete roster with draft pick info
        built_roster = build_roster(self.ff_league)
        loaded_roster = pd.read_csv(curr_dir + '/datasets/roster.csv', index_col='pick')
        pd.testing.assert_frame_equal(built_roster.sort_index(), loaded_roster.sort_index())

        # roster with no draft info
        built_roster_no_draft = build_roster(self.ff_league, add_draft=False)
        loaded_roster_no_draft = pd.read_csv(curr_dir + '/datasets/roster-no_draft.csv', index_col='player_id')
        pd.testing.assert_frame_equal(built_roster_no_draft.sort_index(), loaded_roster_no_draft.sort_index())

    def test_draft(self):
        built_draft = build_draft(self.ff_league)
        loaded_draft = pd.read_csv(curr_dir + '/datasets/draft.csv', index_col='pick')
        pd.testing.assert_frame_equal(built_draft.sort_index(), loaded_draft.sort_index())


if __name__ == '__main__':
    unittest.main()
