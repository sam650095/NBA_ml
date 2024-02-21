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

# 每個賽季的平均數據
seasons_data = []
for year in range(2018, 2024):
    season_data = get_season_data(year)
    cols = ['FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    # 确保这些列是数值类型
    for col in cols:
        season_data[col] = pd.to_numeric(season_data[col], errors='coerce')
    avd_data = season_data.groupby(['TEAM_ID', 'SEASON_YEAR'])[cols].mean().reset_index()
    seasons_data.append(avd_data)

# 合并所有赛季的数据
all_avg_Data = pd.concat(seasons_data, ignore_index=True)

# 加载球员的五年平均加权PER数据
players_data = pd.read_csv('./data/Players_Sum_Data.csv')
# weighted_per_avg = players_data['PER'].mean()  # 假设这是已经计算好的

players_data['weighted_PER'] = players_data['PER'] * players_data['MIN']
weighted_per = players_data.groupby('TEAM_ID').agg(
    Total_MIN=('MIN', 'sum'),
    Total_weighted_PER=('weighted_PER', 'sum')
)
weighted_per['Weighted_PER'] = weighted_per['Total_weighted_PER'] / weighted_per['Total_MIN']

# 为所有赛季数据添加五年平均加权PER
all_avg_Data['Weighted_PER'] = weighted_per['Weighted_PER']
# 保存结果
all_avg_Data.to_csv("./data/Seasonal_Team_Avg_Stats_with_PER.csv", index=False)
print("Seasonal team average stats with five-year weighted PER saved successfully.")
