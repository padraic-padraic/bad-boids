"""Defines argument parsing for use in the boids command line interface"""
from boids import Flock
import argparse
import os
import shutil
import yaml

parse = argparse.ArgumentParser(description='A tool for simulating a flock o\' boids.')
parse.add_argument('--example_config',action='store_true',help='Write out a default config file.')
parse.add_argument('-f','--from_file',
                   help="Load the flock parameters from a .yml file", metavar='config.yml')
def process():
    """Script called by the command line interface: Parses args and then runs a simulation"""
    args = parse.parse_args()
    if args.example_config:
        shutil.copyfile(os.path.join(os.path.dirname(__file__),'config.yml'),
                        os.path.join(os.path.abspath('./'),'config.yml'))
        return
    if args.from_file:
        fname = os.path.abspath(args.from_file)
        flock = Flock(conf=yaml.load(open(fname)))
    else:
        flock = Flock()
    flock.show_animation()
