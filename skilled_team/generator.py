import binpacking

from .player import Player
from .game_stats import GameStats
from .team import Team
from .balancer import Balancer


def generate_skilled_team(player_list: dict, stats: GameStats) -> list:
    print("Initializing teams...")
    teams = initialize_teams(player_list=player_list, stats=stats)
    balance_teams(teams=teams, stats=stats)

    return teams


def initialize_teams(player_list: dict, stats: GameStats) -> list:
    weight_map = Player.get_weight_map_from_player_list(player_list=player_list)
    print("Running bin packing")
    bins = binpacking.to_constant_bin_number(weight_map, stats.total_teams)

    print("Generating Teams Objects")
    teams = Team.get_bulk_teams(raw_team_list=bins, player_list=player_list, stats=stats)

    print(f"Stats: {stats.to_string()}")
    return teams


def balance_teams(teams: list, stats: GameStats):
    balancer = Balancer(teams=teams, stats=stats)
    count_success, count_failures = balancer.balance_teams()

    print(f"Balancer Done!\n"
          f"count_success: {count_success}\n"
          f"count_failures: {count_failures}\n")
    print(f"\nStats:\n {balancer.stats.to_string()}")

    if count_success > 0:
        for team in balancer.teams:
            print(team.to_string())
    else:
        print("Balancing failed")
