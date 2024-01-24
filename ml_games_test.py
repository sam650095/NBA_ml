import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

data = pd.read_csv('data/games_ori_data.csv')

y = data['WL']
X = data.drop(['WL', 'GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'MATCHUP'], axis=1)

X['GAME_DATE'] = (pd.to_datetime(X['GAME_DATE']) - pd.Timestamp("1970-01-01")).dt.days

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

importances = model.feature_importances_
features = pd.DataFrame({'Feature': X.columns, 'Importance': importances})

features = features.sort_values(by='Importance', ascending=False)

print(features.head(20))
