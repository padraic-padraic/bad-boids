"""
A hopefully no longer bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import os
import random
import six
import yaml

class Flock(object):
    """The Flock class: Contains two 2xN arrays detailing the coordinates and velocities of each boid.
    """
    def __init__(self, **kwargs):
        """Constructor: Can take a tuple of initial data and a config dictionary s keyword arguments. Falls back
        to defaults if neither is present."""
        data = kwargs.get('data', None)
        conf = kwargs.get('conf', None)
        self.load_conf(conf)
        if data is None:
            xs = self.random_gen(self.x_window, self.number)
            ys = self.random_gen(self.y_window, self.number)
            xvs = self.random_gen(self.xvs_window, self.number)
            yvs = self.random_gen(self.yvs_window, self.number)
        else:
            xs,ys,xvs,yvs = data
        self.positions = np.array([xs,ys])
        self.velocities = np.array([xvs,yvs])
        self.figure = plt.figure()
        axes=plt.axes(xlim=self.fig_limits, ylim=self.fig_limits)
        self.scatter = axes.scatter(xs,ys)

    def load_conf(self, conf=None):
        """Load the simulation parameters from a config dict. Falls back to the default config if no dict is given. The expected structure can be seen by calling Flock().conf interpreatively."""
        if conf == None:
            with open(os.path.join(os.path.dirname(__file__),'config.yml'),'r') as f:
                conf = yaml.load(f)
        for key in conf.keys():
            for sub_key, item in conf[key].items():
                setattr(self, sub_key, item)

    @staticmethod
    def random_gen(window,number):
        """Generate an array of random values within the specified range"""
        _min,_max = window
        return np.random.uniform(_min,_max,number)

    @classmethod
    def from_data(cls, _data):
        """Wrapper around __init__ to make it easier to load initial data. Takes a tuple of initial values
        in the form (x_coords,y_coords,x_velocities,y_velocities)."""
        flock = cls(data=_data)
        return flock

    @property
    def offset_tuple(self):
        """Helper function to make updating the animation easier"""
        if six.PY3:
            return list(zip(self.positions[0],self.positions[1]))
        else:
            return zip(self.positions[0],self.positions[1])

    @property
    def data(self):
        """Helper function to easily extract data about all the boids. Returns a tuple in the form
        (xcoords,ycoords,x_velocities,y_velocities)"""
        xs,ys = self.positions
        xvs,yvs = self.velocities
        return (xs,ys,xvs,yvs)

    @property
    def conf(self):
        not_conf = ['positions','velocities']
        keys = [key for key in self.__dict__.keys() if not key in not_conf]
        animation_parameters = ['fig_limits','frames','interval']
        boid_parameters = ['x_window','y_window','xvs_window','yvs_window']
        flock_parameters = ['number', 'flocking_factor', 'aware_distance',
                            'alert_distance', 'speedmatching_factor']
        conf = {'animation_parameters':{},
                'boid_parameters':{},
                'flock_parameters':{}}
        for key in keys:
            if key in animation_parameters:
                conf['animation_parameters'][key] = getattr(self, key)
            elif key in boid_parameters:
                conf['boid_parameters'][key] = getattr(self, key)
            else:
                conf['flock_parameters'][key] = getattr(self,key)
        return conf

    def move_to_middle(self):
        flock_com = np.mean(self.positions,1)
        self.velocities -= (self.flocking_factor *
                           (self.positions - flock_com[:, np.newaxis]))

    def avoid_nearby_birds(self):
        separations = self.positions[:,np.newaxis,:] - self.positions[:,:,np.newaxis]
        distant = np.sum(separations*separations,0) > self.alert_distance
        correction = np.copy(separations)
        correction[0,:,:][distant] = 0.
        correction[1,:,:][distant] = 0.
        self.velocities += np.sum(correction,1)
        return separations

    def match_speed_to_nearby_birds(self):
        separations = self.positions[:,np.newaxis,:] - self.positions[:,:,np.newaxis]
        delta_vs = self.velocities[:,np.newaxis,:] - self.velocities[:,:,np.newaxis]
        distant = np.sum(separations*separations,0) > self.aware_distance
        delta_vs[0,:,:][distant] = 0.
        delta_vs[1,:,:][distant] = 0.
        self.velocities += self.speedmatching_factor * np.mean(delta_vs,1)

    def update_boids(self):
        """Move the boids forward one timestep"""
        self.move_to_middle()
        separations = self.avoid_nearby_birds()
        self.match_speed_to_nearby_birds()
        # Move according to velocities
        self.positions += self.velocities

    def animate(self,frame):
        """Helper function used to create the animation"""
        self.update_boids()
        self.scatter.set_offsets(self.offset_tuple)

    def gen_animation(self):
        """Call matplotlib.animation.FuncAnimation to generate the animation."""
        self.anim = animation.FuncAnimation(self.figure, self.animate,
                                       frames=50,interval=50)
    def show_animation(self):
        """Generate and show the animation"""
        self.gen_animation()
        plt.show()

if __name__ == "__main__":
    flock = Flock()
    flock.show_animation()
