import espn_api.football as fb
import pandas as pd


def build_roster(league: fb.League, add_draft: bool = True):
    """
    Build DataFrame with all players on team rosters

    :param league: input league
    :param add_draft: add draft details to roster data
    :return: roster DataFrame
    """
    # create DF with roster from players across team
    roster = pd.DataFrame()
    for team in league.teams:
        team_df = pd.DataFrame()
        for player in team.roster:
            player_d = {
                'player_id': player.playerId,
                'name': player.name,
                'position': player.position,
                'team': team.team_name,
                'owner': team.owner,
            }
            player_df = pd.DataFrame([player_d])
            team_df = pd.concat([team_df, player_df])
        roster = pd.concat([roster, team_df])

    if add_draft:
        draft_results = build_draft(league=league, add_name=False).reset_index()
        roster = pd.merge(roster, draft_results, how='inner', on='player_id').set_index('pick')
    else:
        roster = roster.set_index('player_id')

    return roster


def build_draft(league: fb.League, add_name: bool = True):
    """
    Build Dataframe with draft results

    :param league: input league
    :param add_name: include name in draft results
    :return: draft DataFrame
    """
    draft = pd.DataFrame()
    for pick in league.draft:
        pick_d = {
            'player_id': pick.playerId,
            'round': pick.round_num,
            'pick': (pick.round_num - 1)*(len(league.teams)) + pick.round_pick,
        }
        if add_name:
            pick_d['name'] = pick.playerName

        pick_df = pd.DataFrame([pick_d])
        draft = pd.concat([draft, pick_df])
    return draft.set_index('pick')


if __name__ == '__main__':
    ff_league = fb.League(league_id=956882, year=2022,
                          espn_s2='AEC1zjIvilzU%2BoF8LkcATCDGm9rgUNsGkxmiIfYLdFoihpMWoCVQgG%2FniIi0G2GoaHrJJYy1r'
                                  'C8BUBELl1oVpO6nwsfY357qzJy9AhNaOx4T2YSNJaL1b8%2FurIUgy8BmuLQZQVKABzc%2BsZudsW'
                                  'oB48F4iiomhKBHeE3Ei%2FA6uaH3kc5bXAw1kGibd8oKKDnuxRy4g%2BkXUGb3u6U2DGAVVoW1Ycd'
                                  '%2F9cRHlYLZR9hyTsPa%2B7AKzCkgAFbFE43xjbGlZ3TEf4SreN6XkjRKN9ZPtcOX',
                          swid='{60221347-8376-4C38-9B79-143C183774C6}')
    ff_roster = build_roster(ff_league)
    print(ff_roster.head())
