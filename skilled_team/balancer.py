import random
import numpy as np

from operator import sub, abs

from .team import Team
from .game_stats import GameStats
from .utils import get_config


class Balancer:
    def __init__(self, teams: list, stats: GameStats):
        self.teams = teams
        self.stats = stats

    def balance_teams(self) -> (int, int):
        app_config = get_config()
        count_failure = 0
        count_success = 0
        max_failure = app_config['skilled_team']['balancer']['max_failures']

        while count_failure < max_failure:

            left_team_player_id, left_team, right_team_player_id, right_team = self.get_random_players_to_swap()

            left_team_old_sk_total_list = np.array(left_team.sk_total_list)
            right_team_old_sk_total_list = np.array(right_team.sk_total_list)
            left_team_old_weighted_sk_total = left_team.weighted_sk_total
            right_team_old_weighted_sk_total = right_team.weighted_sk_total

            self.swap_players(left_team_player_id=left_team_player_id, left_team=left_team,
                              right_team_player_id=right_team_player_id, right_team=right_team)

            weighted_sk_total_validation = \
                self.validate_weighted_sk_total(old_left_value=left_team_old_weighted_sk_total,
                                                old_right_value=right_team_old_weighted_sk_total,
                                                new_left_value=left_team.weighted_sk_total,
                                                new_right_value=right_team.weighted_sk_total)

            """
            Validate that each team's weighted skill total improve after the swap 
            """
            if not weighted_sk_total_validation:
                self.swap_players(left_team_player_id=right_team_player_id, left_team=left_team,
                                  right_team_player_id=left_team_player_id, right_team=right_team)
                count_failure += 1
                continue

            sk_total_list_validation = self.validate_sk_total_list(old_left_list=left_team_old_sk_total_list.tolist(),
                                                                   old_right_list=right_team_old_sk_total_list.tolist(),
                                                                   new_left_list=left_team.sk_total_list,
                                                                   new_right_list=right_team.sk_total_list,
                                                                   left_team_size=len(left_team.player_list.keys()),
                                                                   right_team_size=len(right_team.player_list.keys()))

            """
            Validate that the minimum amount of skill has improved after the swap for each team
            """
            if not sk_total_list_validation:
                self.swap_players(left_team_player_id=right_team_player_id, left_team=left_team,
                                  right_team_player_id=left_team_player_id, right_team=right_team)
                count_failure += 1
                continue

            if len(left_team.player_list.keys()) < self.stats.players_per_team or \
                    len(right_team.player_list.keys()) < self.stats.players_per_team:

                print("Swap successful for small team! Bravo!\n")
                print(f"Old Values:\n"
                      f"left_team_old_sk_total_list: {left_team_old_sk_total_list}\n"
                      f"right_team_old_sk_total_list: {right_team_old_sk_total_list}\n"
                      f"left_team_old_weighted_sk_total: {left_team_old_weighted_sk_total}\n"
                      f"right_team_old_weighted_sk_total: {right_team_old_weighted_sk_total}")
                print(f"New Values:\n "
                      f"left_team_sk_total_list: {left_team.sk_total_list}\n"
                      f"right_team_sk_total_list: {right_team.sk_total_list}\n"
                      f"left_team_weighted_sk_total: {left_team.weighted_sk_total}\n"
                      f"right_team_weighted_sk_total: {right_team.weighted_sk_total}")

            count_success += 1

        return count_success, count_failure

    def get_random_players_to_swap(self) -> (int, Team, int, Team):
        """
        Returns 2 random players and their respective 2 different teams
        :return:
        """
        random_team_numbers = random.sample(range(0, len(self.teams)), 2)
        left_team = self.teams[random_team_numbers[0]]
        right_team = self.teams[random_team_numbers[1]]
        left_team_player_id = random.choice(list(left_team.player_list.keys()))
        right_team_player_id = random.choice(list(right_team.player_list.keys()))

        return left_team_player_id, left_team, right_team_player_id, right_team

    def swap_players(self, left_team_player_id: str, left_team: Team,
                     right_team_player_id: str, right_team: Team):

        left_team_size = len(left_team.player_list)
        right_team_size = len(right_team.player_list)

        left_player = left_team.player_list[left_team_player_id]
        right_player = right_team.player_list[right_team_player_id]

        left_team.swap_player(old_player_id=left_team_player_id, new_player=right_player, stats=self.stats)
        right_team.swap_player(old_player_id=right_team_player_id, new_player=left_player, stats=self.stats)

        if len(left_team.player_list) != left_team_size or len(right_team.player_list) != right_team_size:
            exit(f"Something went wrong while swapping players from teams\n Left Player: {left_team_player_id} - "
                 f"Right Player: {right_team_player_id}")

    def validate_weighted_sk_total(self, old_left_value: int, old_right_value: int,
                                   new_left_value: int, new_right_value: int) -> bool:

        left_old_distance_to_avg = abs(self.stats.avg_team_weighted_sk_total - old_left_value)
        right_old_distance_to_avg = abs(self.stats.avg_team_weighted_sk_total - old_right_value)
        left_new_distance_to_avg = abs(self.stats.avg_team_weighted_sk_total - new_left_value)
        right_new_distance_to_avg = abs(self.stats.avg_team_weighted_sk_total - new_right_value)

        if self.stats.one_side_validation:
            if left_new_distance_to_avg < left_old_distance_to_avg or \
                    right_new_distance_to_avg < right_old_distance_to_avg:
                return True
            else:
                return False
        else:
            if left_new_distance_to_avg < left_old_distance_to_avg and \
                    right_new_distance_to_avg < right_old_distance_to_avg:
                return True
            else:
                return False

    def validate_sk_total_list(self, old_left_list: list, old_right_list: list,
                               new_left_list: list, new_right_list: list,
                               left_team_size: int, right_team_size: int) -> bool:

        left_min_sk_size = self.__get_min_sk_sizes(team_size=left_team_size)
        right_min_sk_size = self.__get_min_sk_sizes(team_size=right_team_size)

        left_old_distance_to_avg = list(map(sub, self.stats.avg_sk_list, old_left_list))
        left_old_distance_to_avg = list(map(abs, left_old_distance_to_avg))

        right_old_distance_to_avg = list(map(sub, self.stats.avg_sk_list, old_right_list))
        right_old_distance_to_avg = list(map(abs, right_old_distance_to_avg))

        left_new_distance_to_avg = list(map(sub, self.stats.avg_sk_list, new_left_list))
        left_new_distance_to_avg = list(map(abs, left_new_distance_to_avg))

        right_new_distance_to_avg = list(map(sub, self.stats.avg_sk_list, new_right_list))
        right_new_distance_to_avg = list(map(abs, right_new_distance_to_avg))

        left_diff = np.array(list(map(sub, left_old_distance_to_avg, left_new_distance_to_avg)))
        right_diff = np.array(list(map(sub, right_old_distance_to_avg, right_new_distance_to_avg)))

        left_improvement = np.where(left_diff > 0)[0]
        right_improvement = np.where(right_diff > 0)[0]

        if len(left_improvement) >= left_min_sk_size and \
                len(right_improvement) >= right_min_sk_size:
            return True
        else:
            return False

    def __get_min_sk_sizes(self, team_size: int) -> int:

        if team_size >= self.stats.players_per_team:
            return self.stats.min_val_sk_set_size
        else:
            size_diff = self.stats.players_per_team - team_size
            return self.stats.min_val_sk_set_size - size_diff
