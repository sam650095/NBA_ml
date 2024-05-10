import pandas as pd
import numpy as np
# modal
import xgboost as xgb
# sklearn
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, RandomizedSearchCV
# preproccess
from preproccess.features_cal import calculate_per, calculate_ts, calculate_usg, calculate_df
# graph
from draw import draw
from accuracy import show_players_acc
# nba_api
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

from math import sqrt
import time

# player = input("Input NBA Player: ")
player = "Lebron James"
season = '2023-24'
data = pd.read_csv('data/Players_Avg_Data.csv')
player_ids = data['Player_ID']
features = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'USG', 'TS', 'PER', 'DF']
X = data[features]
y = data['PTS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 分別進行不同參數的調整，找到最合適的
param_dist = {'max_depth': [3, 5, 7, 9], 'n_estimators': [100, 200, 500], 'learning_rate': [0.01, 0.05, 0.1], 'colsample_bytree': [0.5, 0.7, 1]}
xg_reg = xgb.XGBRegressor(objective='reg:squarederror')
rs = RandomizedSearchCV(xg_reg, param_dist, n_iter=20, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, random_state=42)

# 分割資料集的預測
def seperatedata():
    rs.fit(X_train, y_train)
    y_pred_test = rs.best_estimator_.predict(X_test)
    rmse_test = sqrt(mean_squared_error(y_test, y_pred_test))
    return y_test, y_pred_test, rmse_test

# 選手2023-2024的預測
def _2023playerdata(player, season):
    player_info = players.find_players_by_full_name(player)[0]
    player_id = player_info['id']
    _2024gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    df = _2024gamelog.get_data_frames()[0]
    # if (df.empty): 
    #     return 1.0,1.0,0
    df['PER'] = df.apply(calculate_per, axis=1)
    df['USG'] = df.apply(calculate_usg, axis=1)
    df['TS'] = df.apply(calculate_ts, axis=1)
    df['DF'] = df.apply(calculate_df, axis=1)
    
    X_player = df[features].tail(10)
    y_player = df['PTS'].tail(10)
    rs.fit(X, y)
    y_player_pred = rs.best_estimator_.predict(X_player)
    y_player_pred = np.ceil(y_player_pred)
    rmse_player = sqrt(mean_squared_error(y_player, y_player_pred))
    return y_player, y_player_pred, rmse_player

# 所有選手的
def _2023players():
    pre_player_id = 0
    player_accuracies = []
    count =1
    for pid in player_ids:
        if int(pid) == pre_player_id:continue
        print(count,pid)
        start_time = time.time()
        players_info = players.find_player_by_id(int(pid))
        players_name = players_info['full_name']
        try:
            y_player, y_player_pred, rmse_player = _2023playerdata(players_name, season)
            # print("y_player",y_player,"y_pred",y_player_pred,"rmse_player",rmse_player)
            accuracy = 1 - (sum(abs(y_player - y_player_pred)) / sum(y_player))
            player_accuracies.append({'Name': players_name, 'Accuracy': accuracy})
            pre_player_id = int(pid)
            end_time = time.time()
            print(f"Time: {end_time - start_time:.6f} seconds")
            count+=1
        except:
            print(players_name,"沒有足夠資料")
            continue
        
    return player_accuracies

player_data = _2023players()
y_test, y_pred_test, rmse_test = seperatedata()
y_player, y_player_pred, rmse_player = _2023playerdata(player, season)
draw(y_test, y_pred_test, rmse_test, y_player, y_player_pred, rmse_player,player, season)
show_players_acc(player_data)
