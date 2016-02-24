"""
A hopefully no longer bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import random

FIG_LIMITS = (-500., 1500.)

class Flock(object):

    def __init__(self, number=50,**kwargs):
        data = kwargs.get('data', None)
        if data is None:
            xs = np.array([random.uniform(-450., 50.) for x in range(number)])
            ys = np.array([random.uniform(300., 600.) for x in range(number)])
            xvs = np.array([random.uniform(0., 10.) for x in range(number)])
            yvs = np.array([random.uniform(-20., 20.) for x in range(number)])
        else:
            xs,ys,xvs,yvs = data
        self.positions = np.array([xs,ys])
        self.velocities = np.array([xvs,yvs])
        self.figure = plt.figure()
        axes=plt.axes(xlim=FIG_LIMITS, ylim=FIG_LIMITS)
        self.scatter=axes.scatter(xs, ys)

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
        self.velocities -= 0.01*(self.positions - flock_com[:,np.newaxis])
        # Fly away from nearby boids
        separations = self.positions[:,np.newaxis,:] - self.positions[:,:,np.newaxis]
        distant = np.sum(separations*separations,0) > 100.
        correction = np.copy(separations)
        correction[0,:,:][distant] = 0.
        correction[1,:,:][distant] = 0.
        self.velocities += np.sum(correction,1)
        # Try to match speed with nearby boids
        delta_vs = self.velocities[:,np.newaxis,:] - self.velocities[:,:,np.newaxis]
        distant = np.sum(separations*separations,0) > 10000.
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
