import numpy as np
from tqdm import tqdm
from utils import *
from random_shape_generator import *
import argparse
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

winH, winW = -1, -1
winUnits = "pix"
winColor = [-1,-1,-1]
barH, barW = 7, 1
# barLength = None
barSpacingMult = 30.
# pathRigid = None
interBarD = 0.8*barH
# N, R = None, None
N = None
jitter = interBarD/4
targetAlpha = 255
bgAlpha = 255
gapAlpha = 0
mark_long = True
n_samples = -1


def draw_open_paths(draw, n, num, longest=False):
    """
    Function to draw an open path for iter 3 dataset
    :param draw: window to draw path on
    :param n: Length of path to be drawn
    :param num: Number of distracting paths
    :return: None
    """
    num = np.random.randint(1,num)
    n = 2*n + 1
    for _ in range(num):
        alphas = [(i % 2) * 255 for i in range(n)]
        target_offset = return_random_startpos_grid(high=.8*winH, max=winH)
        alpha = return_random_uniform(low=0, high=np.pi/4)
        start_pos = np.array((0,0))
        start_pos += target_offset
        x1,x2,y1,y2 = [],[],[],[]
        for i in range(n):
            start_x, start_y = start_pos
            beta = alpha + return_random_uniform(low=-np.pi/4, high=np.pi/4)
            next_x = start_x+interBarD*np.cos(beta)
            next_y = start_y+interBarD*np.sin(beta)
            next_pos = (next_x, next_y)
            if i%2:
                draw_rectangle_oddeven(draw,barH,p1=tuple(start_pos),p2=tuple(next_pos),alpha=alphas[i])
            x1+= [start_x]; x2+= [next_x]; y1+= [start_y]; y2+=[next_y]
            start_pos, alpha = next_pos, beta


def draw_open_path_contained(draw, N, num_grids=4, mark_long=True):
    """
    Function to draw an open path for iter 3 dataset
    :param draw: window to draw path on
    :param n: Length of path to be drawn
    :return: None
    """
    index_long = np.random.randint(num_grids)
    if mark_long:
        index_mark = index_long
    else:
        index_mark = np.random.choice(range(0,index_long) + range(index_long+1,num_grids))
    n_long =  2*N + 1
    n_short = N + 1
    for ii in range(num_grids):
        # print('Starting grid %s'%(ii))
        longest = ii==index_long
        if longest:
            n = n_long
        else:
            n = n_short
        # target_offset = [winW/4, winH/4] #
        target_offset = return_random_startpos_grid(high=0.51 * gridSize, max=gridSize)
        # i%2 = 1 for quadrants 1 and 3, i.e, RHS quadrants
        target_offset[0] += ii % 2 * gridSize
        # i/2 = 1 for quadrants 2 and 3, i.e, lower quadrants
        target_offset[1] += ii / 2 * gridSize
        target_offset = (target_offset[0], target_offset[1])
        # target_offset = return_random_startpos_grid(high=0.7*winH, max=winH)
        # currOri = [] #return_random_uniform(low=0, high=np.pi/4)
        start_pos = np.array((0,0))
        start_pos += target_offset
        x1,x2,y1,y2,currOri = [],[],[],[],[]
        alphas = [(i%2)*255 for i in range(n)]
        markers = [0]*n
        if ii==index_mark:
            pos = np.arange(n)[1::2]
            marker = np.random.choice(pos,1)[0]
            alphas[marker] = 255
            markers[marker] = 1
        i=0;
        while(i<n and i>=0):
            start_x, start_y = start_pos
            if start_x > winW or start_y > winH or start_x < 0 or start_y < 0:
                x1, y1, x2, y2 = x1[:-2], y1[:-2], x2[:-2], y2[:-2]
                currOri = currOri[:-2]
                start_x, start_y = x2[-1], y2[-1]
                i -= 3
                i = max(0,i)
            elif i==0:
                beta = float(return_random_uniform(low=0, high=np.pi/4))
            else:
                # sign = np.random.binomial(1,0.5)
                beta = currOri[-1] + return_random_uniform(low=-np.pi/4, high=np.pi/4)
            # next_x = start_x+interBarD*np.cos(beta)
            # next_y = start_y+interBarD*np.sin(beta)
            length = (i%2)*barH + ((i+1)%2)*interBarD
            # next_x = start_x + barH*np.cos(beta)
            # next_y = start_y + barH*np.sin(beta)
            next_x = start_x + length * np.cos(beta)
            next_y = start_y + length * np.sin(beta)
            next_pos = (next_x, next_y)
            x1+= [start_x]; x2+= [next_x]; y1+= [start_y]; y2+=[next_y]
            start_pos = next_pos
            currOri += [beta]
            i += 1
        start_pos = (x1[0],y1[0])
        i=0
        while(i<n-1):
            next_pos = x1[i+1], y1[i+1]
            draw_rectangle_oddeven(draw, barH, p1=tuple(start_pos), p2=tuple(next_pos), alpha=alphas[i],
                                  marker=markers[i])  # (i%2)*255)
            start_pos = next_pos
            i += 1
        longest=False

def get_image():
    """
    Function to draw a new blank image and return instance of Image
    :return: img: Instance of PIL Image
    """
    img = Image.new('RGB', [winH,winW])
    draw = ImageDraw.Draw(img)
    return img, draw


def draw_rectangle_oddeven(draw, height=barH, p1=None, p2=None, width=barW, ori=45, alpha=255, marker=0):
    """
    Draw a rectangle with parameters such as h, w, position, orientation etc
    :param draw: Draw object to draw rectangle on Image
    :param height: Height of rectangle
    :param pos: Position [y,x] of rectangle
    :param width: Width of rectangle
    :param ori: Orientation of rectangle
    :param alpha: Alpha/opacity of rectangle
    :return: Reference to the new rectangle drawn
    """
    if marker==1:
        draw.line(width=width, xy=[p1, p2], fill=(alpha, 0, 0, 1))
    else:
        draw.line(width=width, xy=[p1,p2], fill=(alpha,alpha,alpha, alpha)) # 3:marker,marker))
    return draw


def add_args(parser):
    parser.add_argument('-sd','--save-dir',required=True)
    parser.add_argument('-wd','--win-dim',required=True, type=int)
    parser.add_argument('-pl', '--path-length', required=True, type=int)
    parser.add_argument('-tc', '--target-color', required=False, type=int, default=255)
    parser.add_argument('-bc', '--bg-color', required=False, type=int, default=255)
    parser.add_argument('-ns', '--num-samples', required=True, type=int)
    parser.add_argument('-nosave', '--no-save-samples', required=False, type=bool, default=False)
    parser.add_argument('-d','--debug', required=False, type=bool, default=False)
    parser.add_argument('-en', '--dataset-name', required=True)
    parser.add_argument('-ds', '--dont-show', required=False, default=False)
    parser.add_argument('-ml','--mark-long', required=False, type=bool, default=False)
    parser.add_argument('-ms', '--mark-short', required=False, type=bool, default=False)
    parser.add_argument('-ng','--num-grids', required=False, default=4, type=int)
    return parser


if __name__=='__main__':
    import time
    parser = argparse.ArgumentParser()
    parser = add_args(parser)
    args_ = parser.parse_args()
    args = vars(args_)

    N = args['path_length']
    saveDir = args['save_dir']
    winH = args['win_dim']
    winW = args['win_dim']
    barColor = 255
    targetAlpha = args['target_color']
    bgAlpha = args['bg_color']
    n_samples = args['num_samples']
    dataset_name = args['dataset_name']
    mark_long = args['mark_long']
    openclose = 'mark_short'
    num_grids = args['num_grids']
    num_grids_per_row = np.sqrt(num_grids)
    gridSize = int(winH/num_grids_per_row)
    fileName = 'stim_markshort.png'
    if mark_long:
        openclose = 'mark_long'
        # Do not add hyphen in fileName
        fileName = 'stim_marklong.png'
    savePath = 'data_marked_len18/%s_%s_contours_remote_n_%s_barLength_%s_winH_%s' % (dataset_name,
                                                                                   openclose,
                                                                                   n_samples, N,
                                                                                   winH)
    savePath = os.path.join(os.path.abspath(saveDir), savePath)
    if not args['no_save_samples']:
        mkdir(savePath)
    print('Saving to', savePath)
    imgs = []
    for i in tqdm(range(n_samples)):
        img, draw = get_image()
        draw_open_path_contained(draw, N, num_grids=num_grids,mark_long=mark_long) #drawing main 4 paths
        draw_open_paths(draw, N/3, num_grids) #drawing distractor paths
        if not args['dont_show']:
            img.show()
        if args['debug']:
            time.sleep(3)
        if not args['no_save_samples']:
            imgPath = make_path_unique('%s/%s'%(savePath,fileName))
            img.save(imgPath)
        imgs.append(np.array(img))
        img.close()
