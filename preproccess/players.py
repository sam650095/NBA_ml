import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import playergamelog
from features_cal import calculate_per, calculate_ts, calculate_usg, calculate_df
import time

def get_team_player_data(team_id, min_games=10):
    roster = commonteamroster.CommonTeamRoster(team_id=team_id).get_data_frames()[0]
    all_players_stats = []
    for _, row in roster.iterrows():
        player_id = row['PLAYER_ID']
        print(player_id)
        seasons = [str(year) + '-' + str(year+1)[-2:] for year in range(2017, 2022)]  # 修改為包含多個賽季
        for season in seasons:
            gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season).get_data_frames()[0]
            for col in ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']:
                gamelog[col] = pd.to_numeric(gamelog[col], errors='coerce')
            
            if len(gamelog) >= min_games:
                avg_stats = gamelog.mean(numeric_only=True)
                avg_stats['GP'] = len(gamelog)
                avg_stats['POSITION'] = row['POSITION']
                avg_stats['PER'] = calculate_per(avg_stats)
                avg_stats['USG'] = calculate_usg(avg_stats)
                avg_stats['TS'] = calculate_ts(avg_stats)
                avg_stats['DF'] = calculate_df(avg_stats)
                avg_stats['TEAM_ID'] = team_id
                avg_stats['SEASON'] = season  # 添加賽季列
                all_players_stats.append(avg_stats.to_frame().T)
            time.sleep(0.8)
    if all_players_stats:
        return pd.concat(all_players_stats, ignore_index=True)
    else:
        return pd.DataFrame()

nba_teams = teams.get_teams()
all_teams_stats = []
for team in nba_teams:
    team_id = team['id']
    team_stats = get_team_player_data(team_id)
    print(team_stats)
    all_teams_stats.append(team_stats)
    # break  # 如果想處理所有球隊，需要移除此行

complete_data = pd.concat(all_teams_stats, ignore_index=True)
columns_to_drop = ['PLUS_MINUS', 'VIDEO_AVAILABLE']
complete_data = complete_data.drop(columns=columns_to_drop, errors='ignore')
complete_data = complete_data.dropna(how='all', subset=complete_data.columns.difference(['Team', 'TEAM_ID']))
complete_data.to_csv('./data/Players_Avg_Data.csv', index=False)
print(complete_data)