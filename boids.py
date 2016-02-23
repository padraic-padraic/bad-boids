"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import random

FIG_LIMITS = (-500., 1500.)

class Flock(object):

    def __init__(self, number=50):
        self.xs = np.array([random.uniform(-450., 50.) for x in range(number)])
        self.ys = np.array([random.uniform(300., 600.) for x in range(number)])
        self.xvs = np.array([random.uniform(0., 10.) for x in range(number)])
        self.yvs = np.array([random.uniform(-20., 20.) for x in range(number)])

    @classmethod
    def from_data(cls, data):
        flock = cls()
        data = [np.array(el) for el in data]
        flock.xs, flock.ys, flock.xvs, flock.yvs = data
        return flock

    def get_tuple(self):
        return (self.xs,self.ys,self.xvs,self.yvs)

    def update_boids(self):
        # All of this smells of repetition even with numpy's help
        # Fly towards the middle
        self.xvs -= (self.xs - np.mean(self.xs))*0.01
        self.yvs -= (self.ys - np.mean(self.ys))*0.01
        # Fly away from nearby boids
        sep_x = self.xs[np.newaxis,:] - self.xs[:,np.newaxis]
        sep_y = self.ys[np.newaxis,:] - self.ys[:,np.newaxis]
        distant = (sep_x*sep_x + sep_y*sep_y) > 100.
        x_correct = np.copy(sep_x)
        x_correct[distant] = 0.
        y_correct = np.copy(sep_y)
        y_correct[distant] = 0.
        self.xvs += np.sum(x_correct,0)
        self.yvs += np.sum(y_correct,0)
        # Try to match speed with nearby boids
        for i in range(len(self.xs)):
            for j in range(len(self.xs)):
                if (self.xs[j]-self.xs[i])**2 + (self.ys[j]-self.ys[i])**2 < 10000:
                    self.xvs[i]=self.xvs[i]+(self.xvs[j]-self.xvs[i])*0.125/len(self.xs)
                    self.yvs[i]=self.yvs[i]+(self.yvs[j]-self.yvs[i])*0.125/len(self.xs)
        # Move according to velocities
        self.xs += self.xvs
        self.ys += self.yvs

flock = Flock()
figure=plt.figure()
axes=plt.axes(xlim=FIG_LIMITS, ylim=FIG_LIMITS)
scatter=axes.scatter(flock.xs,flock.ys)

def animate(frame):
    flock.update_boids()
    scatter.set_offsets(zip(flock.xs,flock.ys))


anim = animation.FuncAnimation(figure, animate,
                               frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
