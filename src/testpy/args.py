from .__version__ import VERSION
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    
    # help already added
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    
    parser.add_argument(
        "--no-cli",
        action="store_true"
    )

    parser.add_argument(
        "--config",
        type=str
    )

    parser.add_argument(
        "--run-all",
        action="store_true"
    )

    parser.add_argument(
        "--run-failed",
        action="store_true"
    )
    
    parser.add_argument(
        "--discover",
        action="store_true"
    )

    return parser.parse_args()