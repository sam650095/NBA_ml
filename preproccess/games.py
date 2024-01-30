from nba_api.stats.endpoints import leaguegamelog
import pandas as pd

pd.set_option('display.max_columns', None)

def getgameinfo(year):
    try:
        gamelog = leaguegamelog.LeagueGameLog(season=str(year))
        games_df = gamelog.get_data_frames()[0]
        games_df.drop('VIDEO_AVAILABLE', axis=1, inplace=True)
        games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE'])

        return games_df
    except Exception as e:
        print(f"Error occurred whildae fetching data for {year} season: {e}")
        return pd.DataFrame()

all_seasons_data = []

for i in range(2020, 2022):
    season_data = getgameinfo(i)
    all_seasons_data.append(season_data)

all_seasons_data = pd.concat(all_seasons_data, ignore_index=True)

missing_values = all_seasons_data.isnull().sum()
print("Missing values in each column:\n", missing_values)

all_seasons_data.to_csv("./data/games_ori_data.csv", index=False)
print("All seasons data saved successfully.")
