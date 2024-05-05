from nba_api.stats.static import players
def NBAS():
    curry_info = players.find_player_by_id(201939)
    curry_name = curry_info['full_name']
    print(curry_name) 
    return
NBAS()