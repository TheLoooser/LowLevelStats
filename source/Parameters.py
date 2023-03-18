import argparse


def get_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--summoner_name', default='Don Noway', type=str, help="Your LoL Summoner Name")
    parser.add_argument('-r', '--region', default='euw', type=str, choices=['euw'],
                        help='The Server Region. Currently only EUW.')
    return parser.parse_args()
