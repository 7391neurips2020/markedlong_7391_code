import cmath
from math import atan2
from random import random
import numpy as np

def generateDistractors(n=10, r=0.2, interBarD=16, closed=False):
    N = np.random.randint(low=0.75*n, high=1.25*n)
    angles = np.linspace(0, np.pi, N)
    p1, p2 = np.array((np.cos(angles[1]), np.sin(angles[1]))), \
             np.array((np.cos(angles[0]), np.sin(angles[0])))
    radius = interBarD / np.linalg.norm(p2 - p1)
    r *= radius  # Meaning, r is a proportion of radius eg. 0.25radius
    verts = np.stack((np.cos(angles), np.sin(angles))).T * (radius + r * np.random.uniform(low=-1,
                                                                                           high=1,
                                                                                           size=N))[:, None]
    return verts

def getRandShape(n=10, r=0.2, interBarD=16, closed=True, randomSize=False):
    """
    Function to get vertices of a random shape
    obtained by deforming a unit circle
    :param n: Number of edges in shape
    :param r: Amount of deformation (0 = no deformation
    :param closed: Flag indicating whether contour is open or closed
                    For closed contour, sample angles in [0,2pi] and
                    for open contour, sample angles in [0,pi]
    :return: vertices of random shape polygon
    """
    N = n + 1   # number of points in the Path
    if randomSize:
        N = np.random.randint(low=0.75*N, high=1.25*N)
    if closed:
        angles = np.linspace(0, 2 * np.pi, N)
        p1, p2 = np.array((np.cos(angles[1]),np.sin(angles[1]))), \
                 np.array((np.cos(angles[0]),np.sin(angles[0])))
        radius = interBarD/np.linalg.norm(p2-p1)
        r *= radius # Meaning, r is a proportion of radius eg. 0.25radius
        # ring = np.array([np.random.uniform(-r,r) for i in range(N)])
        verts = np.stack((np.cos(angles), np.sin(angles))).T * (radius + r * np.random.uniform(low=-1,
                                                                                               high=1,
                                                                                               size=N))[:, None]
        verts[-1, :] = verts[0, :]  # Using this instad of Path.CLOSEPOLY avoids an innecessary straight line
    else:
        N_open = int(0.85*N)
        angles = np.linspace(0, 2*np.pi, N) # experimenting same procedure to generate open and closed paths
        # angles = np.roll(angles, 4)
        p1, p2 = np.array((np.cos(angles[1]), np.sin(angles[1]))), \
                 np.array((np.cos(angles[0]), np.sin(angles[0])))
        radius = interBarD / np.linalg.norm(p2 - p1)
        r *= radius  # Meaning, r is a proportion of radius eg. 0.25radius
        verts = np.stack((np.cos(angles), np.sin(angles))).T * (radius + r * np.random.uniform(low=-1,
                                                                                               high=1,
                                                                                               size=N))[:, None]
        # following to remove open curves with opening on the right top
        verts = verts[:-1]
        verts = np.roll(verts, np.random.randint(len(verts)), axis=0)
        verts = verts[:N_open]
    return verts

def vertices2bars(verts):
    # TODO: Check if this function is offsetting verts correctly
    X1, X2 = verts[:-1, 0], verts[1:, 0]
    Y1, Y2 = verts[:-1, 1], verts[1:, 1]
    slopes = (Y2 - Y1) / (X2 - X1)
    angles = rad2deg(slopes, return_rad=True)
    vertsX, vertsY = (X1 + X2) / 2, (Y1 + Y2) / 2
    vertsX, vertsY = list(vertsX), list(vertsY)
    vertsX += [vertsX[0]]
    vertsY += [vertsY[0]]
    verts = np.vstack([vertsX, vertsY]).T
    return angles, verts

# Below portions DEPRECIATED

def get_rand_shape(n=10, r=0.2, interBarD=16, randomSize=False):
    """
    Function to get vertices of a random shape
    obtained by deforming a unit circle
    :param n: Number of edges in shape
    :param r: Amount of deformation (0 = no deformation
    :return: vertices of random shape polygon
    """
    # import ipdb; ipdb.set_trace()
    N = n * 3 + 1  # number of points in the Path
    # TODO: what should be the angular separation r, if the interbar distance is 32 pixels?
    angles = np.linspace(0, 2 * np.pi, N)
    # Added by NAME_REMOVED to adjust radius according to length of chord
    angle = angles[1] - angles[0]
    new_radius = interBarD/(2*np.sin(angle))  # since chord_length = 2*radius*sin(angle)
    # verts = np.stack((np.cos(angles), np.sin(angles))).T * (2 * r * np.random.random(N) + 1 - r)[:, None]
    verts = np.stack((np.cos(angles), np.sin(angles))).T * (2 * r * np.random.uniform(size=N) + 1 - r)[:, None]
    verts[-1, :] = verts[0, :]  # Using this instad of Path.CLOSEPOLY avoids an innecessary straight line
    verts *= np.sqrt(2)*new_radius
    return verts


def convexHull(pts):
    #Graham's scan.
    xleftmost, yleftmost = min(pts)
    by_theta = [(atan2(x-xleftmost, y-yleftmost), x, y) for x, y in pts]
    by_theta.sort()
    as_complex = [complex(x, y) for _, x, y in by_theta]
    chull = as_complex[:2]
    for pt in as_complex[2:]:
        #Perp product.
        while ((pt - chull[-1]).conjugate() * (chull[-1] - chull[-2])).imag < 0:
            chull.pop()
        chull.append(pt)
    return [(pt.real, pt.imag) for pt in chull]


def dft(xs):
    pi = 3.14
    return [sum(x * cmath.exp(2j*pi*i*k/len(xs))
                for i, x in enumerate(xs))
            for k in range(len(xs))]

def interpolateSmoothly(xs, N):
    """For each point, add N points."""
    fs = dft(xs)
    half = (len(xs) + 1) // 2
    fs2 = fs[:half] + [0]*(len(fs)*N) + fs[half:]
    return [x.real / len(xs) for x in dft(fs2)[::-1]]


