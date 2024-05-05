import sys

import numpy as np
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
plt.ion()
def court(ax: mpl.axes, color="white") -> mpl.axes:
    # Short corner 3PT lines
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    # 3PT Arc
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
    ax.plot([-250, 250], [0, 0], linewidth=4, color='black')
    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    return ax

def shot_chart(df: pd.DataFrame, name: str, season=None, RA=True, extent=(-250, 250, 422.5, -47.5),
                gridsize=25, cmap="Reds"):
    fig = plt.figure( figsize=(6, 6), facecolor='white', edgecolor='white', dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], facecolor='white')
    
    # Plot hexbin of shots
    if RA == True:
            x = df.LOC_X
            y = df.LOC_Y + 60
            # Annotate player name and season
            plt.text(-240, 430, f"{name}", fontsize=21, color='black')
            season = f"NBA {season[0][:4]}-{season[-1][-2:]}"
            plt.text(-250, -20, season, fontsize=8, color='black')
            plt.text(110, -20, '@codegym_tech', fontsize=8, color='black')
    else:
            cond = ~((-45 < df.LOC_X) & (df.LOC_X < 45) & (-40 < df.LOC_Y) & (df.LOC_Y < 45))
            x = df.LOC_X[cond]
            y = df.LOC_Y[cond] + 60
            # Annotate player name and season
            plt.text(-240, 430, f"{name}", fontsize=21, color='black')
            plt.text(-240, 400, "(Remove Restricted Area)", fontsize=10, color='red')
            season = f"NBA {season[0][:4]}-{season[-1][-2:]}"
            plt.text(-250, -20, season, fontsize=8, color='black')
            plt.text(110, -20, '@codegym_tech', fontsize=8, color='black')

    hexbin = ax.hexbin(x, y, cmap=cmap,
            bins="log", gridsize=25, mincnt=2, extent=(-250, 250, 422.5, -47.5))

    # Draw court
    ax = court(ax, 'black')                

    return fig
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

    shot_chart(shot_data,player_name,season_id)
    plt.show(block=False)
# -----------------------------------------------------------------------
def plot_predictions(y_test, y_pred_test, rmse_test,y_player, y_player_pred, rmse_player):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
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
# -----------------------------------------------------------------------
def show_players_acc(player_data):
    player_names = [data['Name'] for data in player_data]
    accuracies = [data['Accuracy'] for data in player_data]

    plt.figure(figsize=(12, 6))
    plt.plot(player_names, accuracies, 'b-o', markersize=5)
    plt.xlabel('Player Name', fontsize=14)
    plt.ylabel('Accuracy', fontsize=14)
    plt.ylim(0, 1)
    plt.xticks(rotation=45, ha='right')
    plt.legend(['Prediction Accuracy'], loc='upper left')
    plt.subplots_adjust(bottom=0.3)
    plt.show()
# -----------------------------------------------------------------------

def draw(player_data, y_test, y_pred_test, rmse_test, y_player, y_player_pred, rmse_player,player, season):
    plot_predictions(y_test, y_pred_test, rmse_test, y_player, y_player_pred, rmse_player)
    
    draw_shot_chart(player, season)

    show_players_acc(player_data)
    plt.show(block=True)