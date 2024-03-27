def calculate_per(points, assists, rebounds, steals, blocks, field_goal_attempts, field_goals, free_throw_attempts, free_throws, turnovers, games_played):
    per = ((points + assists + rebounds + steals + blocks) - (field_goal_attempts - field_goals) - (free_throw_attempts - free_throws) - turnovers) / games_played
    return per

def calculate_usg(field_goal_attempts, free_throw_attempts, turnovers, team_minutes, player_minutes, team_field_goal_attempts, team_free_throw_attempts, team_turnovers):
    usg = ((field_goal_attempts + 0.44 * free_throw_attempts + turnovers) * (team_minutes / 5)) / (player_minutes * (team_field_goal_attempts + 0.44 * team_free_throw_attempts + team_turnovers))
    return usg * 100  # Convert to percentage

def calculate_ts(points, field_goal_attempts, free_throw_attempts):
    ts = points / (2 * (field_goal_attempts + 0.44 * free_throw_attempts)) * 100
    return ts
