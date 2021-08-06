from pandas import DataFrame

from .utils import find_weights, get_config


class GameStats:
    def __init__(self, players: DataFrame):
        app_config = get_config()
        skills = app_config['skilled_team']['skills']['indexes']
        self.players_per_team = app_config['skilled_team']['players_per_team']
        self.min_val_sk_set_size = app_config['skilled_team']['balancer']['min_val_sk_set_size']
        self.one_side_validation = app_config['skilled_team']['one_size_validation']

        self.total_players = players.shape[0]
        div = self.total_players // self.players_per_team
        mod = self.total_players % self.players_per_team

        self.total_teams = div if mod == 0 else div + 1

        sums = players.iloc[:, skills].sum()
        size_sk = sums.to_list()
        avg_sk_list = sums.divide(self.total_teams).to_list()

        self.avg_sk_list = avg_sk_list
        self.sk_weight_list = find_weights(size_list=size_sk)

        self.avg_team_weighted_sk_total = None

    def to_string(self):
        return f"total_players: {self.total_players} - "\
              f"total_teams: {self.total_teams} - "\
              f"avg_sk_list: {self.avg_sk_list} - "\
              f"sk_weight_list: {self.sk_weight_list} - "\
              f"avg_team_weighted_sk_total: {self.avg_team_weighted_sk_total}"

    def update_avg_team_weighted_sk_total(self, sum_team_weighted_sk_total: float):
        self.avg_team_weighted_sk_total = sum_team_weighted_sk_total / self.total_teams
