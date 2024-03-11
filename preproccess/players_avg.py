import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelog
import time
def team_data(team_id):
    roster = commonteamroster.CommonTeamRoster(team_id=team_id).get_data_frames()[0]
    all_players_stats = []
    for _, row in roster.iterrows():
        player_id = row['PLAYER_ID']
        player_stats = playersum_data(player_id)
        if not player_stats.empty: 
            player_stats['TEAM_ID'] = team_id 
            all_players_stats.append(player_stats)
        time.sleep(0.6) 
    if all_players_stats:
        team_stats = pd.concat(all_players_stats, axis=1).transpose()
        return team_stats
    else:
        return pd.DataFrame()

def playersum_data(player_id, min_games=20):
    seasons = [str(year) + '-' + str(year+1)[-2:] for year in range(2016, 2021)]
    all_seasons_stats = []
    for season in seasons:
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season).get_data_frames()[0]
        if len(gamelog) >= min_games:
            avg_stats = gamelog.mean(numeric_only=True)
            avg_stats['GP'] = len(gamelog)  
            all_seasons_stats.append(avg_stats)
        time.sleep(0.6)  
    
    if all_seasons_stats:
        player_avg_stats = pd.concat(all_seasons_stats, axis=1).mean(axis=1)  
        return player_avg_stats
    else:
        return pd.Series(dtype=float)

nba_teams = teams.get_teams()
all_teams_stats = []
for team in nba_teams:
    team_id = team['id']
    team_stats = team_data(team_id)
    all_teams_stats.append(team_stats)
    # break  # 如果想處理所有球隊，需要移除此行

complete_data = pd.concat(all_teams_stats, ignore_index=True)

columns_to_drop = ['PLUS_MINUS', 'VIDEO_AVAILABLE']
complete_data = complete_data.drop(columns=columns_to_drop, errors='ignore')

complete_data = complete_data.dropna(how='all', subset=complete_data.columns.difference(['Team', 'TEAM_ID']))

complete_data.to_csv('./data/Players_Avg_Data.csv', index=False)

print(complete_data)
