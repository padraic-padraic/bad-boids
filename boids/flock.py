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
        """Load the simulation parameters from a config dict. Falls back to the default config if no dict is given."""
        if conf == None:
            with open(os.path.join(os.path.dirname(__file__),'config.yml'),'r') as f:
                conf = yaml.load(f)
        self.fig_limits = conf['animation_parameters'].get('fig_limits')
        self.frames = conf['animation_parameters']['frames']
        self.interval = conf['animation_parameters']['interval']
        self.number = conf['flock_parameters'].get('number')
        self.flocking_factor = conf['flock_parameters'].get('flocking_factor')
        self.alert_distance = conf['flock_parameters'].get('alert_distance')
        self.aware_distance = conf['flock_parameters'].get('aware_distance')
        self.speedmatching_weight = conf['flock_parameters'].get('speedmatching_weight')
        self.x_window = conf['boid_parameters'].get('x_window')
        self.y_window = conf['boid_parameters'].get('y_window')
        self.xvs_window = conf['boid_parameters'].get('xvs_window')
        self.yvs_window = conf['boid_parameters'].get('yvs_window')

    @staticmethod
    def random_gen(window,number):
        """Generate an array of random values within the specified range"""
        _min,_max = window
        return np.array([random.uniform(_min, _max) for x in range(number)])

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

    def update_boids(self):
        """Move the boids forward one timestep"""
        # Fly towards the middle
        flock_com = np.mean(self.positions,1)
        self.velocities -= self.flocking_factor*(self.positions - flock_com[:,np.newaxis])
        # Fly away from nearby boids
        separations = self.positions[:,np.newaxis,:] - self.positions[:,:,np.newaxis]
        distant = np.sum(separations*separations,0) > self.alert_distance
        correction = np.copy(separations)
        correction[0,:,:][distant] = 0.
        correction[1,:,:][distant] = 0.
        self.velocities += np.sum(correction,1)
        # Try to match speed with nearby boids
        delta_vs = self.velocities[:,np.newaxis,:] - self.velocities[:,:,np.newaxis]
        distant = np.sum(separations*separations,0) > self.aware_distance
        delta_vs[0,:,:][distant] = 0.
        delta_vs[1,:,:][distant] = 0.
        self.velocities += self.speedmatching_weight * np.mean(delta_vs,1)
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
