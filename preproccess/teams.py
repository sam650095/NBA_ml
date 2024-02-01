from nba_api.stats.endpoints import leaguegamelog
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)

def getgameinfo(year):
    try:
        gamelog = leaguegamelog.LeagueGameLog(season=str(year), season_type_all_star='Regular Season')
        games_df = gamelog.get_data_frames()[0]
        games_df.drop(['VIDEO_AVAILABLE'], axis=1, inplace=True)
        games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE'])
        return games_df
    except Exception as e:
        print(f"Error occurred while fetching data for {year} season: {e}")
        return pd.DataFrame()

all_seasons_data = []

for i in range(2018, 2024):
    season_data = getgameinfo(i)
    all_seasons_data.append(season_data)

all_seasons_data = pd.concat(all_seasons_data, ignore_index=True)
team_avg_stats = all_seasons_data.select_dtypes(include=[np.number]).groupby('TEAM_ID').mean()
team_avg_stats.reset_index(inplace=True)

columns_to_keep = ['TEAM_ID', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
team_avg_stats = team_avg_stats[columns_to_keep]

players_data = pd.read_csv('./data/players_sum_data.csv')
# 利用上場時間做加權平均
players_data['weighted_PER'] = players_data['PER'] * players_data['MIN']
weighted_per = players_data.groupby('TEAM_ID').agg(
    Total_MIN=('MIN', 'sum'),
    Total_weighted_PER=('weighted_PER', 'sum')
)
weighted_per['Weighted_PER'] = weighted_per['Total_weighted_PER'] / weighted_per['Total_MIN']
weighted_per = weighted_per.reset_index()[['TEAM_ID','Weighted_PER']]
merged_data = pd.merge(weighted_per, team_avg_stats, left_on='TEAM_ID', right_on='TEAM_ID')


merged_data.to_csv("./data/Final_Data.csv", index=False)
print("Team average stats data saved successfully.")
