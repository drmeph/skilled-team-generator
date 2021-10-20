from pandas import DataFrame

from .utils import get_config


class Player:
    def __init__(self, pid, first_name, last_name, sk_list, extra_fields=[]):
        self.pid = pid
        self.first_name = first_name
        self.last_name = last_name
        self.sk_list = sk_list
        self.sk_total = sum(sk_list)
        self.extra_fields = extra_fields

    def to_string(self):
        return f"pid: {self.pid} - " \
               f"first_name: {self.first_name} - " \
               f"last_name: {self.last_name} - " \
               f"sk_list: {self.sk_list} - " \
               f"sk_total: {self.sk_total}"

    def to_json(self):
        return self.__dict__

    @staticmethod
    def load_players_from_csv(input_data: DataFrame) -> dict:
        player_list = dict()

        app_config = get_config()
        pid = app_config['skilled_team']['player_id_index']
        fn = app_config['skilled_team']['first_name']
        ln = app_config['skilled_team']['last_name']
        skills = app_config['skilled_team']['skills']['indexes']
        extra_fields = app_config['skilled_team']['extra_field']

        for index, row in input_data.iterrows():
            sk_list = []
            ext_fields = []

            for idx in skills:
                sk_list.append(row[idx])

            for idx in extra_fields:
                ext_fields.append(row[idx])

            player = Player(pid=row[pid], first_name=row[fn], last_name=row[ln], sk_list=sk_list,
                            extra_fields=ext_fields)

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
