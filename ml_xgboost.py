import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from math import sqrt
from preproccess.features_cal import calculate_per, calculate_ts, calculate_usg
import matplotlib.pyplot as plt

data = pd.read_csv('data/Players_Avg_Data.csv')

features = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT','FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST','STL', 'BLK', 'TOV', 'PF']
X = data[features]
y = data['PTS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
best_params = {'colsample_bytree': 0.3, 'learning_rate': 0.01, 'max_depth': 5, 'alpha': 10, 'n_estimators': 100}
xg_reg = xgb.XGBRegressor(**best_params, objective='reg:squarederror')
xg_reg.fit(X_train, y_train)

y_pred_test = xg_reg.predict(X_test)

rmse = sqrt(mean_squared_error(y_test, y_pred_test))

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_test, color='darkorange', alpha=0.6, label='Actual vs. Predicted')

plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2, label='Perfect Prediction')

plt.title(f'Comparison of Actual and Predicted Scores\nRMSE: {rmse:.2f}')
plt.xlabel('Actual Score')
plt.ylabel('Predicted Score')
plt.legend()
plt.show()