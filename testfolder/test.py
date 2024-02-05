from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

# LeBronJames的訊息
player_info = players.find_players_by_full_name("LeBron James")[0]
# 選手生涯紀錄
career = playercareerstats.PlayerCareerStats(player_id=player_info['id'])
career_data = career.get_data_frames()[0]

print(career_data)
