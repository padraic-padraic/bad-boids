import matplotlib
matplotlib.use('Agg')
import os
import yaml
from boids.flock import Flock
from copy import deepcopy

flock = Flock()
before=deepcopy(flock.data)
flock.update_boids()
after=flock.data
fixture = {"before":before, "after":after}
fixture_file = open(os.path.join(os.path.dirname(__file__),'Fixtures',
                               'fixture.yml'),'w')
fixture_file.write(yaml.dump(fixture))
fixture_file.close()
