from .flock import Flock
import argparse
import os
import shutil
import yaml

parse = argparse.ArgumentParser(description='A tool for simulating a flock o\' boids.')
parse.add_argument('--example_config',action='store_true',help='Write out a default config file.')
parse.add_argument('-f','--from_file',
                   help="Load the flock parameters from a .yml file")
# parse.add_argument('-n','--number', help="Number of boids in the flock",
#                    type=int)
# parse.add_argument('-ps','--position_window', nargs=4, help="")
# parse.add_argument('-vs','--velocity_window', nargs=4,help="")
# parse.add_argument('-ff','--flockfactor', help="How strongly birds flock")
# parse.add_argument('-ald','--alertdist', help="How close birds fly to each other")
# parse.add_argument('-ad','--awaredist', help="How close birds are to match their speeds")
# parse.add_argument('-smw','--speedweight', help="How strongly birds try to match speeds")
# parse.add_argument('-fl','--fig_limits', help="Limits of the figure")

def process():
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
