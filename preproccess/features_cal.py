import np
def calculate_per(player_stats):
    per = ((player_stats['PTS'] + player_stats['AST'] + player_stats['REB'] + player_stats['STL'] + player_stats['BLK']) - (player_stats['FGA'] - player_stats['FGM']) - (player_stats['FTA'] - player_stats['FTM']) - player_stats['TOV']) 
    return per

def calculate_usg(player_stats):
    if player_stats['MIN'] <= 0:
        return np.nan
    usg = (player_stats['FGA'] + 0.44 * player_stats['FTA'] + player_stats['TOV']) / (player_stats['MIN'] / 5)
    return usg

def calculate_ts(player_stats):
    if 2 * (player_stats['FGA'] + 0.44 * player_stats['FTA']) == 0:
        return 0
    ts = player_stats['PTS']/ (2 * (player_stats['FGA'] + 0.44 * player_stats['FTA']))
    return ts
def calculate_df(player_status):
    if player_status['MIN']<=0:
        return 0
    df = (player_status['REB']+player_status['BLK']+player_status['STL'])-player_status['PF']/player_status['MIN']
    return df