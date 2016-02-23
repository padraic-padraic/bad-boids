import matplotlib
matplotlib.use('Agg')
from boids import Flock
from nose.tools import assert_equal, assert_almost_equal
import os
import yaml

def test_bad_boids_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    boid_data=regression_data["before"]
    flock = Flock.from_data(boid_data)
    flock.update_boids()
    res = (flock.xs,flock.ys,flock.xvs,flock.yvs)
    for after,before in zip(regression_data["after"],res):
        for after_value,before_value in zip(after,before):
            assert_almost_equal(after_value,before_value,delta=0.01)

def test_from_data():
    data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    flock = Flock.from_data(data["before"])
    imported = (flock.xs,flock.ys,flock.xvs,flock.yvs)
    for real,got in zip(data["before"],imported):
        for real_value, got_value in zip(real,got):
            assert_equal(real_value,got_value)
