from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd

lebron = players.find_players_by_full_name("LeBron James")[0]
lebron_id = lebron['id']

gamelog = playergamelog.PlayerGameLog(player_id=lebron_id, season='2023')

df = gamelog.get_data_frames()[0]

columns = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT',
           'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
           'STL', 'BLK', 'TOV', 'PF', 'PTS']

print(df[columns])