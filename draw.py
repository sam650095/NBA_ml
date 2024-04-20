import sys

import numpy as np
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
plt.ion()
def court(ax=None, color="black", lw=1, outer_lines=False):
    if ax is None:
        ax = plt.gca()
    hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw, restricted, corner_three_a, corner_three_b, three_arc, center_outer_arc, center_inner_arc]

    if outer_lines:
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)


def draw_shot_chart(player_name, season_id):
    # 球員資訊
    player_dict = players.find_players_by_full_name(player_name)[0]
    team_id = playercareerstats.PlayerCareerStats(player_id=player_dict['id']).get_data_frames()[0][
        playercareerstats.PlayerCareerStats(player_id=player_dict['id']).get_data_frames()[0]['SEASON_ID'] == season_id]['TEAM_ID']

    # 投籃數據
    shot_data = shotchartdetail.ShotChartDetail(team_id=int(team_id), player_id=int(player_dict['id']),
                                                season_type_all_star='Regular Season',
                                                season_nullable=season_id,
                                                context_measure_simple="FGA").get_data_frames()[0]

    title = f"{player_name} Shot Chart {season_id}"

    fig, ax = plt.subplots(figsize=(8, 6))
    ax = shot_chart(shot_data, title=title, ax=ax)
    plt.show(block=False)

def shot_chart(data, title="", ax=None):
    court(ax)
    x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
    y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']
    x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']

    ax.scatter(x_missed, y_missed, c='r', marker="x", s=90, linewidths=3)
    ax.scatter(x_made, y_made, facecolors='none', edgecolors='g', marker='o', s=30, linewidths=3)

    ax.set_title(title, fontsize=18)
    return ax

# player_name = sys.argv[1] if len(sys.argv) > 1 else "Lebron James"
# season_id = sys.argv[2] if len(sys.argv) > 2 else "2023-24"
# draw_shot_chart(player_name, season_id)

# shotchart end
# plot
def plot_predictions(y_test, y_pred_test, rmse_test,y_player, y_player_pred, rmse_player):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    # 繪製分類資料集的預測
    ax1.scatter(y_test, y_pred_test, color='darkorange', alpha=0.6, label='Actual vs. Predicted')
    ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2, label='Perfect Prediction')
    ax1.set_title(f'Split Data Prediction\nRMSE: {rmse_test:.2f}')
    ax1.set_xlabel('Actual Score')
    ax1.set_ylabel('Predicted Score')
    ax1.legend()

    # 繪製2023-2024近10場的比賽預測
    ax2.scatter(range(len(y_player)), y_player, color='green', label='Actual Score', marker='o')
    ax2.scatter(range(len(y_player_pred)), y_player_pred, color='red', label='Predicted Score', marker='x')
    ax2.set_title(f'Last 10 Games of 2023-2024 Season\nRMSE: {rmse_player:.2f}')
    ax2.set_xlabel('Game')
    ax2.set_ylabel('Score')
    ax2.legend(loc='upper left') 

    # 添加表格
    table_data = [['Actual', 'Predicted']]
    for actual, pred in zip(y_player, y_player_pred):
        table_data.append([f'{actual:.1f}', f'{pred:.1f}'])
    table = ax2.table(cellText=table_data, colLabels=None, cellLoc='center', loc='right')
    table.scale(0.2, 2.52) 
    plt.tight_layout()
    plt.show(block=False)

def draw(y_test, y_pred_test, rmse_test, y_player, y_player_pred, rmse_player,player, season):
    plot_predictions(y_test, y_pred_test, rmse_test, y_player, y_player_pred, rmse_player)
    
    draw_shot_chart(player, season)
    
    plt.show(block=True)