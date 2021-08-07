import pandas as pd
import logging
import sys
import json

from os import path

from .player import Player
from .stats import Stats
from .generator import generate_skilled_team
from .option_handler import default_options
from .utils import complex_handler, get_config


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

    if len(args) < 2:
        logging.error("Missing parameters!")
        op.print_help()
        sys.exit()

    input_file = args[1]
    output_file = f"data/{opts.output}"
    output_stat_file = f"data/stats-{opts.output}"

    # Read from CSV file
    if not path.exists(input_file):
        sys.exit('File does not exists!')

    if path.exists(output_file):
        sys.exit('Output file already exists, please use another name of delete the file.')

    if path.exists(output_stat_file):
        sys.exit('Stat output file already exists, please use another name of delete the file.')

    logging.info("Loading Players...")

    input_data = pd.read_csv(input_file, index_col=False, low_memory=False)
    player_list = Player.load_players_from_csv(input_data=input_data)
    stats = Stats(input_data)
    teams = generate_skilled_team(player_list=player_list, stats=stats)

    with open(output_file, 'w') as of:
        of.write(json.dumps(teams, default=complex_handler))

    with open(output_stat_file, 'w') as osf:
        osf.write(json.dumps(stats, default=complex_handler))

    logging.info("Skilled Team Creation Done!")
