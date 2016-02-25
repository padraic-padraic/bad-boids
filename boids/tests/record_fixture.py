import matplotlib
matplotlib.use('Agg')
import yaml
from boids.flock import Flock
from copy import deepcopy

flock = Flock()
before=deepcopy(flock.data)
flock.update_boids()
after=flock.data
fixture = {"before":before, "after":after}
fixture_file=open("fixture_test.yml",'w')
fixture_file.write(yaml.dump(fixture))
fixture_file.close()
