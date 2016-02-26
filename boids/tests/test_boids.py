import matplotlib
matplotlib.use('Agg')
from boids.flock import Flock
from mock import patch
from nose.tools import assert_equal, assert_almost_equal
import os
import yaml

def test_bad_boids_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),
                                  'Fixtures','fixture.yml'),'r'))
    boid_data=regression_data["before"]
    flock = Flock.from_data(boid_data)
    flock.update_boids()
    res = flock.data
    for after, calculated in zip(regression_data["after"], res):
        for after_value, calculated_value in zip(after, calculated):
            assert_almost_equal(after_value, calculated_value, delta=0.01)

def test_move_to_middle_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),
                                  'Fixtures','fixture.yml'),'r'))
    flock = Flock.from_data(regression_data['before'])
    flock.move_to_middle()
    res = flock.data
    for after, calculated in zip(regression_data["middle"], res):
        for after_value, calculated_value in zip(after, calculated):
            assert_almost_equal(after_value, calculated_value, delta=0.01)

def test_avoid_nearby_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),
                                  'Fixtures','fixture.yml'),'r'))
    flock = Flock.from_data(regression_data['before'])
    flock.avoid_nearby_birds()
    res = flock.data
    for after, calculated in zip(regression_data["avoid"], res):
        for after_value, calculated_value in zip(after, calculated):
            assert_almost_equal(after_value, calculated_value, delta=0.01)

def test_match_speed_regression():
    regression_data=yaml.load(open(os.path.join(os.path.dirname(__file__),
                                  'Fixtures','fixture.yml'),'r'))
    flock = Flock.from_data(regression_data['before'])
    flock.match_speed_to_nearby_birds()
    res = flock.data
    for after, calculated in zip(regression_data["match"], res):
        for after_value, calculated_value in zip(after, calculated):
            assert_almost_equal(after_value, calculated_value, delta=0.01)

def test_from_data():
    data=yaml.load(open(os.path.join(os.path.dirname(__file__),'Fixtures',
                                     'fixture.yml'),'r'))
    flock = Flock.from_data(data["before"])
    imported = flock.data
    for real,got in zip(data["before"],imported):
        for real_value, got_value in zip(real,got):
            assert_equal(real_value,got_value)

def test_properties():
    data=yaml.load(open(os.path.join(os.path.dirname(__file__),'Fixtures',
                                     'fixture.yml')))
    flock = Flock.from_data(data["after"])
    offset = flock.offset_tuple
    true_offset = list(zip(data['after'][0], data['after'][1])) #Caused python3 test to fail
    got_data = flock.data
    for after,got in zip(data["after"], got_data):
        for after_value,got_value in zip(after, got):
            assert_almost_equal(after_value, got_value,delta=0.01)
    for n, item in enumerate(offset):
        assert item[0] == true_offset[n][0]
        assert item[1] == true_offset[n][1]

def test_conf_loader():
    default_conf = yaml.load(open(os.path.join(os.path.dirname(__file__), '..',
                                       'config.yml'),'r'))
    flock = Flock()
    for key, item in default_conf.items():
        for sub_key in item.keys():
            assert getattr(flock, sub_key) == item[sub_key]
    non_default_conf = yaml.load(open(os.path.join(os.path.dirname(__file__),
                                                 'Fixtures','config.yml'),'r'))
    flock = Flock(conf=non_default_conf)
    for key, item in non_default_conf.items():
        for sub_key in item.keys():
            assert getattr(flock, sub_key) == item[sub_key]
