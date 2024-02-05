import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.svm import SVR

# 取資料
data = pd.read_csv('./data/final_data.csv')
# 取目標變數
X = data[['Weighted_PER', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']]
y = data['PTS']
# 分割資料集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model_svm = SVR(kernel='rbf')

model_svm.fit(X_train, y_train)

y_pred_svm = model_svm.predict(X_test)

mse_svm = mean_squared_error(y_test, y_pred_svm)
r2_svm = r2_score(y_test, y_pred_svm)

print("SVM - Mean Squared Error:", mse_svm)
print("SVM - R2 Score:", r2_svm)
