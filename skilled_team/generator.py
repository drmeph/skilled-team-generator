import binpacking
import logging

from .player import Player
from .stats import Stats
from .team import Team
from .balancer import Balancer


def generate_skilled_team(player_list: dict, stats: Stats) -> list:
    logging.info("Initializing teams...")
    teams = initialize_teams(player_list=player_list, stats=stats)
    balance_teams(teams=teams, stats=stats)

    return teams


def initialize_teams(player_list: dict, stats: Stats) -> list:
    """
    Use bin packing to create a set of teams based on the skill total of each player

    :param player_list: list of players
    :param stats: game stat object
    :return: list of teams
    """
    weight_map = Player.get_weight_map_from_player_list(player_list=player_list)

    logging.info("Running bin packing")
    bins = binpacking.to_constant_bin_number(weight_map, stats.total_teams)

    logging.info("Generating Teams Objects")
    teams = Team.get_bulk_teams(raw_team_list=bins, player_list=player_list, stats=stats)

    logging.info(f"Stats: {stats.to_string()}\n")
    return teams


def balance_teams(teams: list, stats: Stats):
    balancer = Balancer(teams=teams, stats=stats)
    count_success, count_failures = balancer.balance_teams()
    stats.update_successful_swaps(count_success)

    logging.info(f"Balancer Done!\n"
                 f"count_success: {count_success}\n"
                 f"count_failures: {count_failures}\n")
    logging.info(f"\nStats:\n {balancer.stats.to_string()}")

    if count_success > 0:
        for team in balancer.teams:
            logging.debug(team.to_string())
    else:
        logging.warning("Balancing failed")
