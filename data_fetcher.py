from cfbd.rest import ApiException
from datetime import datetime
import pandas as pd

def get_current_week():
    today = datetime.now()
    season_start = datetime(today.year, 8, 1)
    week = ((today - season_start).days // 7) + 1
    return min(week, 15)

from cfbd.rest import ApiException

def get_game_data(api, year, week, team):
    try:
        games = api['games'].get_games(year=year, week=week, team=team)
        if not games:
            print(f"No games found for {team} in week {week} of {year}")
            return None, None
        
        game = games[0]
        
        # Use get_team_game_stats instead of get_box_score
        game_stats = api['games'].get_team_game_stats(year=year, week=week, team=team)
        
        return game, game_stats
    except ApiException as e:
        print(f"Exception when calling API: {e}")
        return None, None

def get_betting_data(api, year, week, team):
    try:
        lines = api['betting'].get_lines(year=year, week=week)
        betting_data = [
            {
                'home_team': game.home_team,
                'away_team': game.away_team,
                'provider': line.provider,
                'spread': line.spread,
                'formatted_spread': line.formatted_spread,
                'over_under': line.over_under,
                'home_moneyline': line.home_moneyline,
                'away_moneyline': line.away_moneyline,
                'game_date': game.start_date
            }
            for game in lines
            for line in game.lines
            if game.home_team == team or game.away_team == team
        ]
        return pd.DataFrame(betting_data)
    except ApiException as e:
        print(f"Exception when calling BettingApi->get_lines: {e}")
        return pd.DataFrame()
