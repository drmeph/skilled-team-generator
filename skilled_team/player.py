from pandas import DataFrame


class Player:
    def __init__(self, pid, first_name, last_name, sk_list):
        self.pid = pid
        self.first_name = first_name
        self.last_name = last_name
        self.sk_list = sk_list
        self.sk_total = sum(sk_list)

    def to_string(self):
        return f"pid: {self.pid} - " \
               f"first_name: {self.first_name} - " \
               f"last_name: {self.last_name} - " \
               f"sk_list: {self.sk_list} - " \
               f"sk_total: {self.sk_total}"

    @staticmethod
    def load_players_from_csv(input_data: DataFrame) -> dict:
        #header = input_data.columns.values
        player_list = dict()

        """
        Refactor to make this part dynamic
        hard coding the indexes
        """
        pid = 0
        fn = 1
        ln = 2
        sklz = [3, 4, 5, 6, 7, 8]
        tid = 9

        for index, row in input_data.iterrows():
            sk_list = []

            for idx in sklz:
                sk_list.append(row[idx])

            player = Player(pid=row[pid], first_name=row[fn], last_name=row[ln], sk_list=sk_list)

            if player.pid in player_list:
                exit(f"Found duplicate in player data {player.pid}")

            player_list[player.pid] = player

        return player_list

    @staticmethod
    def get_weight_map_from_player_list(player_list: dict) -> dict:
        weight_map = dict()

        for key in player_list:
            player = player_list[key]
            weight = player.sk_total

            weight_map[key] = weight

        return weight_map
