def get_rows_from_teams(teams: list):
    header = ["Team #", "ID", "Full Name", "Email", "Development", "Quality Assurance", "Operations",
              "Security", "Strategy", "Data", "Organization", "City", "Region"]
    total_header = ["Team #", "Development", "Quality Assurance", "Operations", "Security", "Strategy", "Data"]

    rows = [header]
    total_rows = [total_header]

    for team in teams:
        t_rows, tt_rows = team.to_csv()
        rows = rows + t_rows
        total_rows.append(tt_rows)

    return rows, total_rows
