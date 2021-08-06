from operator import add, mul

from .game_stats import GameStats
from .player import Player


class Team:
    def __init__(self, player_list: dict, stats: GameStats):
        self.player_list = player_list
        self.sk_total_list = None
        self.weighted_sk_total = None

        self.__update_team(stats=stats)

    def to_string(self):
        return f"player_list: {list(self.player_list.keys())} - " \
               f"sk_total_list: {self.sk_total_list} - " \
               f"weighted_sk_total: {self.weighted_sk_total}"

    @staticmethod
    def get_bulk_teams(raw_team_list: list, player_list: dict, stats: GameStats) -> list:
        team_list = []
        team_number = 0
        sum_team_weighted_sk_total = 0

        for raw_team in raw_team_list:
            team_number += 1
            team_player_list = dict()

            for key in raw_team:
                team_player_list[key] = player_list[key]

            team = Team(player_list=team_player_list, stats=stats)
            sum_team_weighted_sk_total += team.weighted_sk_total
            team_list.append(team)

        stats.update_avg_team_weighted_sk_total(sum_team_weighted_sk_total=sum_team_weighted_sk_total)

        return team_list

    def swap_player(self, old_player_id: str, new_player: Player, stats: GameStats):
        self.player_list[new_player.pid] = new_player
        self.player_list.pop(old_player_id)
        self.__update_team(stats=stats)

    def __update_team(self, stats: GameStats):
        self.sk_total_list, self.weighted_sk_total = self.calculate_stats(player_list=self.player_list,
                                                                          stats=stats)

    @staticmethod
    def calculate_stats(player_list: dict, stats: GameStats) -> (list, int):
        sk_total_list = None

        for key in player_list:
            player = player_list[key]

            if sk_total_list is None:
                sk_total_list = player.sk_list
            else:
                sk_total_list = list(map(add, sk_total_list, player.sk_list))

        weighted_sk_total = sum(list(map(mul, sk_total_list, stats.sk_weight_list)))

        return sk_total_list, weighted_sk_total
