from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.text import Annotation
import math

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

#define bases
#H/V
V = np.array([[0, 0], [0, 1], [0, 0]])
H = -1*V

#D/A
A = np.array([[0, 1], [0, 0], [0, 0]])
D = -1*A

#R/L
R = np.array([[0, 0], [0, 0], [0, 1]])
L = -1*R

# draw cube
r = [-1, 1]
for s, e in combinations(np.array(list(product(r, r, r))), 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
        ax.plot3D(*zip(s, e), color="b")

# draw sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:20j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color="#2a68a2", alpha=0.5)

# draw a point
ax.scatter([0], [0], [0], color="g", s=100)

#Draw basis points
#H/V
ax.scatter([0], [-1], [0], color="b", s=100)
ax.scatter([0], [1], [0], color="b", s=100)

#D/A
ax.scatter([-1], [0], [0], color="y", s=100)
ax.scatter([1], [0], [0], color="y", s=100)

#R/L
ax.scatter([0], [0], [-1], color="r", s=100)
ax.scatter([0], [0], [1], color="r", s=100)

# draw a vector
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


class Arrow3D(FancyArrowPatch):

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

class Annotation3D(Annotation):
    '''Annotate the point xyz with text s'''

    def __init__(self, s, xyz, *args, **kwargs):
        Annotation.__init__(self,s, xy=(0,0), *args, **kwargs)
        self._verts3d = xyz        

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.xy=(xs,ys)
        Annotation.draw(self, renderer)

def annotate3D(ax, s, *args, **kwargs):
    '''add anotation text s to to Axes3d ax'''
    tag = Annotation3D(s, *args, **kwargs)
    ax.add_artist(tag)

def stokesToVector(sVector):
    #print("The sVector is: ", sVector)
    vector = V*(-sVector[2]) + A*(-sVector[0]) + R*sVector[1]
    a = Arrow3D(*vector, mutation_scale=20,
            lw=1, arrowstyle="->", color="r")
    ax.add_artist(a)

#H/V labels
annotate3D(ax, s="|H>", xyz=[0,-1,0], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom')
annotate3D(ax, s="|V>", xyz=[0,1,0], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom')

#D/A labels
annotate3D(ax, s="|D>", xyz=[-1,0,0], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom')
annotate3D(ax, s="|A>", xyz=[1,0,0], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom')


#R/L labels
annotate3D(ax, s="|L>", xyz=[0,0,-1], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom')
annotate3D(ax, s="|R>", xyz=[0,0,1], fontsize=10, xytext=(-3,3),
               textcoords='offset points', ha='right',va='bottom')
def show():
    plt.show()
