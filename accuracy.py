import matplotlib.pyplot as plt
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
    plt.show(block = True)
