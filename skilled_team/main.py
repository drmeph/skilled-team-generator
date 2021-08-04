import pandas as pd


from .player import Player
from .stats import Stats
from .generator import generate_skilled_team


def main():
    print("Loading Players...")
    input_data = pd.read_csv("data/sample-data.csv", index_col=False, low_memory=False)

    player_list = Player.load_players_from_csv(input_data=input_data)

    stats = Stats(input_data)
    print(stats.to_string())


    generate_skilled_team(player_list=player_list, stats=stats)
