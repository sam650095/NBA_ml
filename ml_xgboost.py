import pandas as pd
import numpy as np
# modal
import xgboost as xgb
# sklearn
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, RandomizedSearchCV
# preproccess
from preproccess.features_cal import calculate_per, calculate_ts, calculate_usg
# plot
import matplotlib.pyplot as plt
# nba_api
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

from math import sqrt

data = pd.read_csv('data/Players_Avg_Data.csv')
data['PER'] = data.apply(calculate_per, axis=1)
data['USG'] = data.apply(calculate_usg, axis=1)
data['TS'] = data.apply(calculate_ts, axis=1)

features = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'USG', 'TS', 'PER']
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
def _2023playerdata():
    player_info = players.find_players_by_full_name('LeBron James')[0]
    player_id = player_info['id']
    _2024gamelog = playergamelog.PlayerGameLog(player_id=player_id, season='2023-24')
    df = _2024gamelog.get_data_frames()[0]
    df['PER'] = df.apply(calculate_per, axis=1)
    df['USG'] = df.apply(calculate_usg, axis=1)
    df['TS'] = df.apply(calculate_ts, axis=1)
    X_player = df[features].tail(10)
    y_player = df['PTS'].tail(10)
    rs.fit(X, y)
    y_player_pred = rs.best_estimator_.predict(X_player)
    y_player_pred = np.ceil(y_player_pred)
    rmse_player = sqrt(mean_squared_error(y_player, y_player_pred))
    return y_player, y_player_pred, rmse_player

def plot_predictions():
    y_test, y_pred_test, rmse_test = seperatedata()
    y_player, y_player_pred, rmse_player = _2023playerdata()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # 繪製分類資料集的預測
    ax1.scatter(y_test, y_pred_test, color='darkorange', alpha=0.6, label='Actual vs. Predicted')
    ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2, label='Perfect Prediction')
    ax1.set_title(f'Split Data Prediction\nRMSE: {rmse_test:.2f}')
    ax1.set_xlabel('Actual Score')
    ax1.set_ylabel('Predicted Score')
    ax1.legend()

    # 繪製2023-2024近10場的比賽預測
    ax2.scatter(range(len(y_player)), y_player, color='green', label='Actual Score', marker='o')
    ax2.scatter(range(len(y_player_pred)), y_player_pred, color='red', label='Predicted Score', marker='x')
    ax2.set_title(f'Last 10 Games of 2023-2024 Season\nRMSE: {rmse_player:.2f}')
    ax2.set_xlabel('Game')
    ax2.set_ylabel('Score')
    ax2.legend(loc='upper left') 

    # 添加表格
    table_data = [['Actual', 'Predicted']]
    for actual, pred in zip(y_player, y_player_pred):
        table_data.append([f'{actual:.1f}', f'{pred:.1f}'])
    table = ax2.table(cellText=table_data, colLabels=None, cellLoc='center', loc='right')
    table.scale(0.2, 2.52) 
    plt.tight_layout()
    plt.show()

plot_predictions()