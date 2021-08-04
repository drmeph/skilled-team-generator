from pandas import DataFrame

from .stats_utils import find_weights


class Stats:
    def __init__(self, players: DataFrame):
        """
       Refactor to make this part dynamic
       hard coding the indexes
       """
        sklz = [3, 4, 5, 6, 7, 8]

        self.total_players = players.shape[0]
        """
        Move the number of player per team to the config file
        """
        div = self.total_players // 5
        mod = self.total_players % 5

        self.total_teams = div if mod == 0 else div + 1

        sums = players.iloc[:, sklz].sum()
        size_sk = sums.to_list()
        avg_sk_list = sums.divide(self.total_teams).to_list()

        self.avg_sk_list = avg_sk_list
        self.sk_weight_list = find_weights(size_list=size_sk)

    def to_string(self):
        print(f"total_players: {self.total_players} - "
              f"total_teams: {self.total_teams} - "
              f"avg_sk_list: {self.avg_sk_list} - "
              f"sk_weight_list: {self.sk_weight_list}")

