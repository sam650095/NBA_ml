import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

# 取資料
data = pd.read_csv('./data/final_data.csv')
# 取目標變數
X = data[['Weighted_PER', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']]
y = data['PTS']

# 分割資料集 (8:2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 使用RandomForest
# n_estimators = 100 代表他創建100個分支，樹枝越深代表效果越好，但計算時間越長
# random_state 可以把它想成是random.seed
model_rf = RandomForestRegressor(n_estimators=100, random_state=30)

# 訓練資料集
model_rf.fit(X_train, y_train)

# 定義參數網格
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# 初始化網格搜索模型
grid_search = GridSearchCV(estimator=RandomForestRegressor(random_state=30), param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)

# 對數據進行擬合
grid_search.fit(X_train, y_train)

print("Best parameters found: ", grid_search.best_params_)

# 使用最佳估計器進行預測
y_pred_rf = grid_search.predict(X_test)

# 評估模型
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print("均方誤差:", mse_rf)
print("R2分數:", r2_rf)