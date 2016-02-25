import matplotlib
matplotlib.use('Agg')
from boids import Flock
from nose.tools import assert_equal, assert_almost_equal
import numpy as np
import os
import yaml

def test_bad_boids_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    boid_data=regression_data["before"]
    flock = Flock.from_data(boid_data)
    flock.update_boids()
    res = flock.data
    for after,calculated in zip(regression_data["after"],res):
        for after_value,calculated_value in zip(after,calculated):
            assert_almost_equal(after_value,calculated_value,delta=0.01)

def test_from_data():
    data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    flock = Flock.from_data(data["before"])
    imported = flock.data
    for real,got in zip(data["before"],imported):
        for real_value, got_value in zip(real,got):
            assert_equal(real_value,got_value)

def test_properties():
    data=yaml.load(open(os.path.join(os.path.dirname(__file__),'fixture.yml')))
    flock = Flock.from_data(data["after"])
    xs,ys = flock.coord_tuple
    got_data = flock.data
    for after,got in zip(data["after"],got_data):
        for after_value,got_value in zip(after,got):
            assert_almost_equal(after_value,got_value,delta=0.01)
    assert np.allclose(data["after"][0], xs)
    assert np.allclose(data["after"][1], ys)
