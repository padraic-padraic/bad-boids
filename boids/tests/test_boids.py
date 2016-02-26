import matplotlib
matplotlib.use('Agg')
from boids.flock import Flock
from mock import Mock, patch
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
@patch('random.uniform',return_value=1)
def test_random_gen(mock_uniform):
    f = Flock()
    assert mock_uniform.call_count == 200
    mock_uniform.assert_any_call(-450.,50.)
    mock_uniform.assert_any_call(300.,600.)
    mock_uniform.assert_any_call(0.,10.)
    mock_uniform.assert_any_call(-20.,20.)

@patch('matplotlib.animation.FuncAnimation')
def test_gen_animation(mock_funcanim):
    f = Flock()
    f.gen_animation()
    mock_funcanim.assert_called_with(f.figure,f.animate,frames=50,interval=50)

@patch('matplotlib.collections.PathCollection.set_offsets')
@patch('boids.Flock.update_boids')
def test_animate(mock_update,mock_scatter):
    f = Flock()
    f.animate(Mock())
    assert mock_update.called
    mock_scatter.assert_called_with(f.offset_tuple)
