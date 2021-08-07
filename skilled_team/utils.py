import numpy as np
import yaml


def find_weights(size_list: list):
    s_list = np.array(size_list)
    weight_list = np.array(size_list)
    weight = 1
    sl = np.array(size_list)

    while len(s_list) > 0:
        v_max = max(s_list)
        up_idx_list = np.where(sl == v_max)[0]
        del_idx_list = np.where(s_list == v_max)[0]
        weight_list[up_idx_list] = weight
        weight += 1
        s_list = np.delete(s_list, del_idx_list)

    return weight_list.tolist()


def get_min_and_max_weighted_sk_total_team(teams: list) -> (int, int):
    min_val = max_val = None
    min_team = max_team = None

    for team in teams:
        if min_val is None or min_val > team.weighted_sk_total:
            min_val = team.weighted_sk_total
            min_team = team

        if max_val is None or max_val < team.weighted_sk_total:
            max_val = team.weighted_sk_total
            max_team = team

    return min_team, max_team


def get_config() -> yaml:
    stream = open(f"app-config.yml", 'r')
    return yaml.load(stream, Loader=yaml.Loader)


def complex_handler(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))
