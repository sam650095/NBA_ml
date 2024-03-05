import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

data = pd.read_csv('data/Players_Sum_Data.csv')  

X = data.drop(['PTS'], axis=1) 
y = data['PTS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

xg_reg = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,
                max_depth = 5, alpha = 10, n_estimators = 10)

# 訓練模型
xg_reg.fit(X_train,y_train)

# 預測
y_pred = xg_reg.predict(X_test)

# 評估
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"RMSE: {rmse}")
