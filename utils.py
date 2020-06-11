import numpy as np
import scipy
import glob
import os
import random, string

def return_random_uniform(size=[], low=0., high=360.):
    val = np.random.uniform(low=low, high=high, size=size)
    return val


def return_random_startpos(nRows=32,nCols=32):
    randX = np.random.randint(-nCols,nCols)
    randY = np.random.randint(-nRows,nRows)
    return randX, randY

def return_random_startpos_loc(nRows=32,nCols=32,max=256):
    randX = np.random.randint(max-nCols,nCols)
    randY = np.random.randint(max-nRows,nRows)
    return randX, randY

def return_random_startpos_grid(high=64,max=64):
    randX = np.random.randint(max - high, high)
    randY = np.random.randint(max - high, high)
    return [randX, randY]

def mkdir(path):
    f = glob.glob(path)
    if f!=[]:
        return
    print('Creating ',path)
    os.mkdir(path)
    return path

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def make_path_unique(path):
    fn = path.split('.')[0]
    if glob.glob('%s*'%(fn))!=[]:
        all_inds = [int(f.split('-')[1]) for f in glob.glob('%s*' % (fn))]
        dirname, basename = os.path.dirname(path), os.path.basename(path)
        fn, ext = basename.split('.')[0], basename.split('.')[-1]
        fn_ind = max(all_inds)
        fn_ind += 1
        rand_string = randomStringDigits()
        fn = os.path.join(dirname, '%s-%08d-%s.%s'%(fn, fn_ind, rand_string, ext))
        return fn
    else:
        rand_string = randomStringDigits()
        dirname, basename = os.path.dirname(path), os.path.basename(path)
        fn = '%s-00000000-%s.%s'%(basename.split('.')[0],rand_string,basename.split('.')[-1])
        fn = os.path.join(dirname, fn)
        return fn
        
def rad2deg(slopes, return_rad=False):
    """
    Function to convert slope to angles in degrees
    :param slopes: slope between two points
    :param return_rad: Return angle in radians
    :return angles: angle in degrees
    """
    angles = np.arctan(slopes)
    if return_rad:
        return angles
    angles_deg = angles*180/np.pi
    return angles_deg

