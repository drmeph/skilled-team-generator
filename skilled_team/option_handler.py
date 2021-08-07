from optparse import OptionParser


def default_options() -> OptionParser:
    op = OptionParser()
    op.set_usage("team_generator.py [options] input_file")
    op.add_option("--output-file", dest="output", help="name of the output FILE, Default: output.csv", metavar="FILE")
    op.set_default("output", "output.csv")
    return op