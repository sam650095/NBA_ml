import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

lebron = players.find_players_by_full_name("LeBron James")[0]
lebron_id = lebron['id']

gamelog = playergamelog.PlayerGameLog(player_id=lebron_id, season='2023')

df = gamelog.get_data_frames()[0]


data = pd.read_csv('data/Players_Avg_Data.csv')

features = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT',
            'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
            'STL', 'BLK', 'TOV', 'PF']
X = data[features]
y = data['PTS']
# 樂布朗詹姆士的數據
X_LBJ_test = df[features]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

xg_reg = xgb.XGBRegressor(objective ='reg:squarederror')

parameters = {
    'colsample_bytree': [0.3, 0.7],
    'learning_rate': [0.01, 0.1],
    'max_depth': [5, 7],
    'alpha': [10, 15],
    'n_estimators': [50, 100]
}

grid_search = GridSearchCV(estimator=xg_reg, param_grid=parameters, cv=3, scoring='neg_mean_squared_error', verbose=1)

grid_search.fit(X_train, y_train)

print(f"Best parameters found: {grid_search.best_params_}")

# y_pred = grid_search.predict(X_test)

# rmse = mean_squared_error(y_test, y_pred, squared=False)
# print(f"RMSE: {rmse}")
y_test_LBJ = y_test.sample(n=60, random_state=42)  

y_LBJ_pred = grid_search.predict(X_LBJ_test)
rmse = mean_squared_error(y_test_LBJ, y_LBJ_pred, squared=False)
print(f"RMSE: {rmse}")