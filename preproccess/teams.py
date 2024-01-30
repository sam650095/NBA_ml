import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats

players_data = pd.read_csv('./data/players_sum_data.csv')

# 利用上場時間做加權平均
players_data['weighted_PER'] = players_data['PER'] * players_data['MIN']
weighted_per = players_data.groupby('Team').agg(
    Total_MIN=('MIN', 'sum'),
    Total_weighted_PER=('weighted_PER', 'sum')
)
weighted_per['Weighted_PER'] = weighted_per['Total_weighted_PER'] / weighted_per['Total_MIN']
weighted_per = weighted_per.reset_index()[['Team', 'Weighted_PER']]

# 取得隊伍資訊
nba_teams = teams.get_teams()

team_stats = []
for team in nba_teams:
    team_id = team['id']
    team_stats_data = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id).get_data_frames()[0]
    latest_stats = team_stats_data.iloc[-1] 
    team_stats.append({
        'Team': team['full_name'],
        'WinPct': latest_stats['WIN_PCT'] 
    })

team_stats_df = pd.DataFrame(team_stats)

final_data = pd.merge(weighted_per, team_stats_df, on='Team', how='left')

final_data.to_csv('./data/final_data.csv', index=False)
