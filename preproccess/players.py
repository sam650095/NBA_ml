import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelog
import time

# 取得隊伍資訊
# 因為要去取這支隊伍每一個球員的數據
def team_data(team_id, team_name):
    # 用team_id去把所有球員的資料取下來
    roster = commonteamroster.CommonTeamRoster(team_id=team_id).get_data_frames()[0]
    all_players_stats = []
    for _, row in roster.iterrows():
        player_id = row['PLAYER_ID']
        # 呼叫playersum_data，取得總和數值
        player_stats = playersum_data(player_id)
        player_stats['TEAM_ID'] = team_id 
        player_stats['Team'] = team_name 
        all_players_stats.append(player_stats)
        # 因為怕api訪問限制，因此將他間隔0.6
        time.sleep(0.6) 

    if all_players_stats:
        # 合併所有資料，並利用轉置，將他的欄位從選手變成特性
        team_stats = pd.concat(all_players_stats, axis=1).transpose()
        return team_stats
    else:
        return pd.DataFrame()
# 計算每一個球員5場比賽的數據總和
def playersum_data(player_id, num_games=10): # num_games設定選手至少參加過有10場比賽
    # 取得球員比賽數據 從2018到2023
    seasons = ['2018-19']
    # , '2019-20', '2020-21', '2021-22', '2022-23'
    all_seasons_data = pd.DataFrame()
    for season in seasons:
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season).get_data_frames()[0]
        
        gamelog['SEASON'] = season
        gamelog['PLAYER_ID'] = player_id
        all_seasons_data = pd.concat([all_seasons_data, gamelog])

    if len(all_seasons_data) >= num_games:
        recent_stats = all_seasons_data.head(num_games)
        sum_stats = recent_stats.sum(numeric_only=True)
        per = calculate_per(sum_stats)
        
        team_id = recent_stats['TEAM_ID'].iloc[0] if 'TEAM_ID' in recent_stats else None
        
        season = recent_stats['SEASON'].iloc[0] if 'SEASON' in recent_stats else None
        total_min = recent_stats['MIN'].sum()  
        return pd.Series({'PLAYER_ID': player_id, 'TEAM_ID': team_id, 'SEASON': season, 'PER': per, 'MIN': total_min})
    else:
       
        return pd.Series({'PLAYER_ID': player_id, 'TEAM_ID': None, 'SEASON': None, 'PER': None, 'MIN': None})
# 計算每一個球員的效率值(PER)
# 因為nba_api並沒有PER，所以要特別計算
def calculate_per(player_stats):
    # PER
    if 'PTS' in player_stats and 'AST' in player_stats and 'REB' in player_stats and 'STL' in player_stats and 'BLK' in player_stats and 'FGA' in player_stats and 'FGM' in player_stats and 'FTA' in player_stats and 'FTM' in player_stats and 'TOV' in player_stats and 'GP' in player_stats:
        per = ((player_stats['PTS'] + player_stats['AST'] + player_stats['REB'] + player_stats['STL'] + player_stats['BLK']) - (player_stats['FGA'] - player_stats['FGM']) - (player_stats['FTA'] - player_stats['FTM']) - player_stats['TOV']) / player_stats['GP']
        return per
    else:
        return None

# 開始
# 取得所有隊伍
nba_teams = teams.get_teams()
# 要儲存所有隊伍資料的地方
all_teams_stats = []
for team in nba_teams:
    team_id = team['id']
    team_name = team['full_name']
    # 呼叫這支隊伍的資料
    team_stats = team_data(team_id, team_name)
    all_teams_stats.append(team_stats)

complete_data = pd.concat(all_teams_stats, ignore_index=True)

complete_data_cleaned = complete_data.dropna()
#確定已經沒有NaN
print(complete_data.isna().any())

#儲存到Players_Sum_Data.csv
complete_data.to_csv('./data/Players_Sum_Data.csv', index=False)

print(complete_data)
print(complete_data_cleaned)