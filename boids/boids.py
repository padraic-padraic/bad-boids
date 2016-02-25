"""
A hopefully no longer bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import os
import random
import yaml

FIG_LIMITS = (-500., 1500.)

class Flock(object):

    def __init__(self, **kwargs):
        data = kwargs.get('data', None)
        conf = kwargs.get('conf',None)
        self.load_conf(conf)
        if data is None:
            xs = np.array([random.uniform(self.x_min, self.x_max) for x in range(number)])
            ys = np.array([random.uniform(self.y_min, self.y_max) for x in range(number)])
            xvs = np.array([random.uniform(self.xvs_min, self.xvs_max) for x in range(number)])
            yvs = np.array([random.uniform(self.yvs_min, self.yvs_max) for x in range(number)])
        else:
            xs,ys,xvs,yvs = data
        self.positions = np.array([xs,ys])
        self.velocities = np.array([xvs,yvs])
        self.figure = plt.figure()
        axes=plt.axes(xlim=self.FIG_LIMITS, ylim=self.FIG_LIMITS)
        self.scatter = axes.scatter(xs, ys)

    def load_conf(self, conf=None):
        if conf == None:
            with open(os.path.join(os.path.dirname(__file__),'config.yml'),'r') as f:
                conf = yaml.load(f)
        self.FIG_LIMITS = tuple(conf['animation_parameters'].get('fig_limits'))
        self.frames = conf['animation_parameters']['frames']
        self.interval = conf['animation_parameters']['interval']
        self.flock_weight = conf['flock_parameters'].get('flocking_factor')
        self.alert_distance = conf['flock_parameters'].get('alert_distance')
        self.aware_distance = conf['flock_parameters'].get('aware_distance')
        self.x_min, self.x_max = conf['boid_parameters'].get('x_window')
        self.y_min, self.y_max = conf['boid_parameters'].get('y_window')
        self.xvs_min, self.xvs_max = conf['boid_parameters'].get('xvs_window')
        self.yvs_min, self.yvs_max = conf['boid_parameters'].get('yvs_window')
    @classmethod
    def from_data(cls, _data):
        flock = cls(data=_data)
        return flock

    @property
    def coord_tuple(self):
        return (self.positions[0],self.positions[1])

    @property
    def data(self):
        xs,ys = self.positions
        xvs,yvs = self.velocities
        return (xs,ys,xvs,yvs)

    def update_boids(self):
        # Fly towards the middle
        flock_com = np.mean(self.positions,1)
        self.velocities -= self.flock_weight*(self.positions - flock_com[:,np.newaxis])
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
        self.velocities += 0.125 * np.mean(delta_vs,1)
        # Move according to velocities
        self.positions += self.velocities

    def animate(self,frame):
        self.update_boids()
        self.scatter.set_offsets(self.coord_tuple)

    def show_animation(self):
        anim = animation.FuncAnimation(self.figure, self.animate,
                                       frames=50,interval=50)
        plt.show()

if __name__ == "__main__":
    flock = Flock()
    flock.show_animation()
