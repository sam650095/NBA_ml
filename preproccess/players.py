import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelog
from sklearn.impute import KNNImputer
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
    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season='2018-23').get_data_frames()[0]
    # 判斷如果選手的場次低於10場，則將他設置為NaN
    if len(gamelog) >= num_games:
        # 找尋近期10場比賽
        recent_stats = gamelog.head(num_games)
        # 並將他加起來
        sum_stats = recent_stats.sum(numeric_only=True)
        # 場次
        sum_stats['GP'] = num_games
        # 計算他的PER
        sum_stats['PER'] = calculate_per(sum_stats)
        return sum_stats
    else:
        return pd.Series(dtype=float) 
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
# m = 0
for team in nba_teams:
    team_id = team['id']
    team_name = team['full_name']
    # 呼叫這支隊伍的資料
    team_stats = team_data(team_id, team_name)
    all_teams_stats.append(team_stats)
    # m+=1
    # if(m == 10):
    #     break

complete_data = pd.concat(all_teams_stats, ignore_index=True)

#刪掉PLUS_MINUS VIDEO_AVALABLE
columns_to_drop = ['PLUS_MINUS', 'VIDEO_AVAILABLE']
complete_data = complete_data.drop(columns=columns_to_drop, errors='ignore')

#刪掉所有NaN值
complete_data = complete_data.dropna(how='all', subset=complete_data.columns.difference(['Team','TEAM_ID']))
#確定已經沒有NaN
#print(complete_data.isna().any())

#儲存到Players_Sum_Data.csv
complete_data.to_csv('./data/Players_Sum_Data.csv', index=False)

print(complete_data)