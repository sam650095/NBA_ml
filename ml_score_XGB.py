import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from sklearn.model_selection import train_test_split, GridSearchCV
from math import sqrt

from preproccess.features_cal import calculate_per,calculate_ts,calculate_usg

import matplotlib.pyplot as plt
data = pd.read_csv('data/Players_Avg_Data.csv')
def feature_calculations(df):
    df['PER'] = np.nan
    df['USG'] = np.nan
    df['TS'] = np.nan
    
    for index, row in df.iterrows():
        df.at[index, 'PER'] = calculate_per(row)
        df.at[index, 'USG'] = calculate_usg(row)
        df.at[index, 'TS'] = calculate_ts(row)
        
    return df
# data = feature_calculations(data)
features2 = ['MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','STL','BLK','TOV','PF','PTS','GP','POSITION','USG','TS','TEAM_ID','Player_ID']
features = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT','FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST','STL', 'BLK', 'TOV', 'PF']
X = data[features]
y = data['PTS']

lebron_info = players.find_players_by_full_name('LeBron James')[0]
lebron_id = lebron_info['id']

gamelog_lebron = playergamelog.PlayerGameLog(player_id=lebron_id, season='2023')
df_lebron_games = gamelog_lebron.get_data_frames()[0]
X_lebron = df_lebron_games[features].head(10)  
best_params = {'colsample_bytree': 0.3, 'learning_rate': 0.01, 'max_depth': 5, 'alpha': 10, 'n_estimators': 100}
xg_reg = xgb.XGBRegressor(**best_params, objective='reg:squarederror')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
xg_reg.fit(X_train, y_train)

y_pred_lebron = xg_reg.predict(X_lebron)

print("勒布朗·詹姆斯的預測得分：", y_pred_lebron)

y_actual_lebron = df_lebron_games['PTS'].head(10).values

rmse = sqrt(mean_squared_error(y_actual_lebron, y_pred_lebron))
plt.figure(figsize=(10, 6))
plt.scatter(range(len(y_actual_lebron)), y_actual_lebron, color='blue', label='Actual Score')
plt.scatter(range(len(y_pred_lebron)), y_pred_lebron, color='red', label='Predicted Score')
plt.title(f'Comparison of Actual and Predicted Scores for LeBron James\nRMSE: {rmse:.2f}')
plt.xlabel('Game Index')
plt.ylabel('Score')
plt.legend()
plt.show()