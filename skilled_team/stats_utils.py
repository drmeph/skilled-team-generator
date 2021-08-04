import numpy as np


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
