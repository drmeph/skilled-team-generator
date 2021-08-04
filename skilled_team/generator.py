import binpacking

from .player import Player
from .stats import Stats


def generate_skilled_team(player_list: dict, stats: Stats) -> list:
    print("Initializing teams...")
    initialize_teams(player_list=player_list, stats=stats)


def initialize_teams(player_list: dict, stats: Stats) -> list:
    weight_map = Player.get_weight_map_from_player_list(player_list=player_list)
    print("Weight Map")
    print(weight_map)

    print("Running bin packing")
    bins = binpacking.to_constant_bin_number(weight_map, stats.total_teams)

    print("===== dict\n", weight_map,"\n", bins)
