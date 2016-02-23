import yaml
from boids import Flock
from copy import deepcopy

flock = Flock()
before=deepcopy(flock.get_tuple())
flock.update_boids()
after=flock.get_tuple()
fixture={"before":before,"after":after}
fixture_file=open("fixture.yml",'w')
fixture_file.write(yaml.dump(fixture))
fixture_file.close()
