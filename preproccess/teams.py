from nba_api.stats.endpoints import leaguegamelog
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

def get_season_data(year):
    gamelog = leaguegamelog.LeagueGameLog(season=str(year), season_type_all_star='Regular Season').get_data_frames()[0]
    gamelog.drop(['VIDEO_AVAILABLE'], axis=1, inplace=True)
    gamelog['GAME_DATE'] = pd.to_datetime(gamelog['GAME_DATE'])
    gamelog['SEASON_YEAR'] = str(year)  
    return gamelog

seasons_data = []
for year in range(2018, 2024):
    season_data = get_season_data(year)
    cols = ['FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

    for col in cols:
        season_data[col] = pd.to_numeric(season_data[col], errors='coerce')
    avd_data = season_data.groupby(['TEAM_ID', 'SEASON_YEAR'])[cols].mean().reset_index()
    seasons_data.append(avd_data)

all_avg_Data = pd.concat(seasons_data, ignore_index=True)

players_data = pd.read_csv('./data/Players_Sum_Data.csv')

players_data['weighted_PER'] = players_data['PER'] * players_data['MIN']
weighted_per = players_data.groupby('TEAM_ID').agg(
    Total_MIN=('MIN', 'sum'),
    Total_weighted_PER=('weighted_PER', 'sum')
)
weighted_per['Weighted_PER'] = weighted_per['Total_weighted_PER'] / weighted_per['Total_MIN']

all_avg_Data['Weighted_PER'] = weighted_per['Weighted_PER']

all_avg_Data.to_csv("./data/Seasonal_Team_Avg_Stats_with_PER.csv", index=False)
print("Seasonal team average stats with five-year weighted PER saved successfully.")
