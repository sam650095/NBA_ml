def calculate_per(player_stats):
    per = ((player_stats['PTS'] + player_stats['AST'] + player_stats['REB'] + player_stats['STL'] + player_stats['BLK']) - (player_stats['FGA'] - player_stats['FGM']) - (player_stats['FTA'] - player_stats['FTM']) - player_stats['TOV']) / player_stats['GP']
    return per

def calculate_usg(player_stats):
    usg = (player_stats['FGA'] + 0.44 * player_stats['FTA'] + player_stats['TOV']) / (player_stats['MIN'] / 5)
    return usg

def calculate_ts(player_stats):
    ts = player_stats['PTS']/ (2 * (player_stats['FGA'] + 0.44 * player_stats['FTA']))
    return ts
