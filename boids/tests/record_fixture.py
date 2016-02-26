import os
import yaml
from boids import Flock
from copy import deepcopy

flock = Flock()
before=deepcopy(flock.data)
flock.move_to_middle()
mtm = deepcopy(flock.data)
flock = Flock.from_data(before)
flock.avoid_nearby_birds()
avoid = deepcopy(flock.data)
flock = Flock.from_data(before)
flock.match_speed_to_nearby_birds()
match = deepcopy(flock.data)
flock = Flock.from_data(before)
flock.update_boids()
after = flock.data
fixture = {"before":before, "after":after, "middle":mtm,
           "avoid":avoid, "match":match}
fixture_file = open(os.path.join(os.path.dirname(__file__),'Fixtures',
                               'fixture.yml'),'w')
fixture_file.write(yaml.dump(fixture))
fixture_file.close()
