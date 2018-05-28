import sys, os
from HuurwoningenScraper.config import config
from HuurwoningenScraper.web import init

def main():
    """Main entry point for the pararius scraper.

       Generaly used for fetching the configuration data 
       and initialising / starting the scraping process.
    """

    config = build_config()
    init(config)


def get_argv():
    """Fetches the command line arguments"""

    return sys.argv


def build_config():
    """Builds configuration class based on the provided command line arguments"""

    conf = config(get_argv())
    return conf 
