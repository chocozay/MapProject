import argparse
import logging

import client_google_map as cli

logging.basicConfig(level=logging.INFO)

# TODO switch over to click
if "__main__" == __name__:
    parser = argparse.ArgumentParser("CLI for My Project")
    parser.add_argument("-U", dest="username", type=str)
    parser.add_argument("--all-users", dest="get_all_users", action="store_true")
    parser.add_argument("--delete", dest="delete", action="store_true")
    parser.add_argument("--create", dest="create", action="store_true")
    parser.add_argument("--history", dest="history", action="store_true")
    parser.add_argument("--nearby", dest="nearby_location", action="store_true")
    parser.add_argument("--address", dest="address", action="store_true")
    parser.add_argument("-f", dest="config_file", type=str)
    parser.add_argument("-C", dest="coordinates", type=str)
    args = parser.parse_args()

    if args.create and args.delete:
        raise RuntimeError("Creation and Deletion is not permitted")
    elif args.get_all_users:
        logging.info("All users: %s", cli.get_all_user())
    elif args.create:
        logging.info(
            "User profile creation results: %s",
            cli.create_user(args.username, args.config_file)
        )
    elif args.delete:
        logging.info("User profile deletion results: %s", cli.delete_user(args.username))
    if args.history:
        cli.get_user_history(args.username)
    if args.nearby_location:
        logging.info(
            "User nearby location results: %s",
            cli.get_nearby_location(args.username, args.coordinates)
        )
    if args.address:
        logging.info(
            "User address results: %s",
            cli.get_address(args.username, args.coordinates)
        )
