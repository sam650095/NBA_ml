import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelog
from sklearn.impute import KNNImputer
import time
import numpy as np

def playeravg_data(player_id, num_games=5):
    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season='2020-22').get_data_frames()[0]
    if len(gamelog) >= num_games:
        recent_stats = gamelog.head(num_games)
        avg_stats = recent_stats.mean(numeric_only=True)
        return avg_stats
    else:
        # print(f"Player ID {player_id} does not have enough games.")
        return pd.Series(dtype=float) 

def team_data(team_id, team_name):
    roster = commonteamroster.CommonTeamRoster(team_id=team_id).get_data_frames()[0]
    all_players_stats = []

    for _, row in roster.iterrows():
        player_id = row['PLAYER_ID']
        player_stats = playeravg_data(player_id)
        player_stats['Team'] = team_name 
        all_players_stats.append(player_stats)
        time.sleep(0.6) 

    if all_players_stats:
        team_stats = pd.concat(all_players_stats, axis=1).transpose()
        return team_stats
    else:
        return pd.DataFrame()
nba_teams = teams.get_teams()
all_teams_stats = []
for team in nba_teams:
    team_id = team['id']
    team_name = team['full_name']
    team_stats = team_data(team_id, team_name)
    all_teams_stats.append(team_stats)

complete_data = pd.concat(all_teams_stats, ignore_index=True)

columns_to_drop = ['PLUS_MINUS', 'VIDEO_AVAILABLE']
complete_data = complete_data.drop(columns=columns_to_drop, errors='ignore')

complete_data = complete_data.dropna(how='all', subset=complete_data.columns.difference(['Team']))

# imputer = KNNImputer(n_neighbors=5)
# numeric_data = complete_data.select_dtypes(include=[np.number])
# print(numeric_data.head())
# if numeric_data.empty:
#     raise ValueError("numeric_data is empty")

# imputed_data = imputer.fit_transform(numeric_data)

# complete_data[numeric_data.columns] = imputed_data

complete_data.to_csv('./data/players_avg_data.csv', index=False)

print(complete_data)