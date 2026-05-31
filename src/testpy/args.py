from .__version__ import VERSION
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    parser.add_argument(
        "--run-all",
        action="store_true"
    )

    parser.add_argument(
        "--no-cli",
        action="store_true"
    )

    parser.add_argument(
        "--config",
        type=str
    )

    return parser.parse_args()