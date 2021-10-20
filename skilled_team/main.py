import pandas as pd
import logging
import sys
import json
import csv

from os import path

from .player import Player
from .stats import Stats
from .generator import generate_skilled_team
from .option_handler import default_options
from .utils import complex_handler, get_config
from .csv_formatter import get_rows_from_teams


def main():
    """
    Setting up options
    """
    op = default_options()
    (opts, args) = op.parse_args(sys.argv)

    """
    Validation and configuration
    """
    app_config = get_config()
    logging.basicConfig(level=app_config['skilled_team']['log_level'])
    output_format = app_config['output']['format']

    if len(args) < 2:
        logging.error("Missing parameters!")
        op.print_help()
        sys.exit()

    input_file = args[1]
    output_file = f"data/{opts.output}.json"
    output_team_totals_file = f"data/totals-{opts.output}.csv"
    output_stat_file = f"data/stats-{opts.output}.json"
    output_csv_file = f"data/{opts.output}.csv"

    # Read from CSV file
    if not path.exists(input_file):
        sys.exit('File does not exists!')

    if path.exists(output_file):
        sys.exit('Output file already exists, please use another name of delete the file.')

    if output_format == 'json':
        if path.exists(output_stat_file):
            sys.exit('Stat output file already exists, please use another name of delete the file.')
    else:
        if path.exists(output_csv_file):
            sys.exit('output file already exists, please use another name of delete the file.')
        if path.exists(output_team_totals_file):
            sys.exit('Team total output file already exists, please use another name of delete the file.')

    logging.info("Loading Players...")

    input_data = pd.read_csv(input_file, index_col=False, low_memory=False)
    player_list = Player.load_players_from_csv(input_data=input_data)
    stats = Stats(input_data)
    teams = generate_skilled_team(player_list=player_list, stats=stats)

    if output_format == 'json':
        with open(output_file, 'w') as of:
            of.write(json.dumps(teams, default=complex_handler))
    else:
        rows, total_rows = get_rows_from_teams(teams=teams)

        with open(output_csv_file, 'w', newline='', encoding='utf-8') as of:
            csv_of = csv.writer(of, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for row in rows:
                csv_of.writerow(row)

        with open(output_team_totals_file, 'w', newline='', encoding='utf-8') as tof:
            csv_of = csv.writer(tof, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for row in total_rows:
                csv_of.writerow(row)

    with open(output_stat_file, 'w') as osf:
        osf.write(json.dumps(stats, default=complex_handler))

    logging.info("Skilled Team Creation Done!")
