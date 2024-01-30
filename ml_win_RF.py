import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

# 取資料
data = pd.read_csv('./data/final_data.csv')
# 取目標變數
X = data[['Weighted_PER']]  
y = data['WinPct'] 

# 分割資料集 (8:2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 使用RandomForest
# n_estimators = 100 代表他創建100個分支，樹枝越深代表效果越好，但計算時間越長
# random_state 可以把它想成是random.seed
model_rf = RandomForestRegressor(n_estimators=50, random_state=30)

# 訓練資料集
model_rf.fit(X_train, y_train)

# 拿訓練好的資料集對測試資料集做預測
y_pred_rf = model_rf.predict(X_test)

mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print("Mean Squared Error:", mse_rf)
print("R2 Score:", r2_rf)
