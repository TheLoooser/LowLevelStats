import argparse


def get_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--summoner_name', default='Don Noway', type=str, help="Your LoL Summoner Name")
    parser.add_argument('-t', '--tag_line', default='EUW', type=str, help="Your LoL Tag Line")
    parser.add_argument('-q', '--queue_type', default='RANKED_SOLO_5x5', type=str,
                        help="The Queue Type (Solo/Duo or Flex)")
    parser.add_argument('-r', '--region', default='euw', type=str, choices=['euw'],
                        help='The Server Region. Currently only EUW.')
    return parser.parse_args()
