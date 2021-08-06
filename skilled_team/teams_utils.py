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
