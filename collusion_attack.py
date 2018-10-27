import glob
from skimage.io import imread
import numpy as np
from PIL import Image, ImageChops
import os
import time
from os import listdir
from os.path import isfile, join


def collude(root_folder="images/", sub_path=None, window_lenth=1):
    path = root_folder + sub_path
    start_time = time.clock()
    print("Starting collude for ", path, " at", start_time, "s")
    sub_folders = [f for f in os.listdir(path) if
                   os.path.isdir(os.path.join(path, f))]
    for f in sub_folders:
        p_collude(root_folder, sub_path + f + "/", window_lenth)
    end_time = time.clock()
    print("End at", end_time, ", completed in", end_time - start_time, "s")


def diff(root_folder, sub_path, window_lenth=1):
    org_path = root_folder + sub_path
    collude_path = root_folder + "collude/" + sub_path
    start_time = time.clock()
    print("Starting get diff for", sub_path, "at", start_time, "s")
    sub_folders = [f for f in os.listdir(org_path)]

    for f in sub_folders:
        file_list = [sf for sf in listdir(org_path + f + "/") if isfile(join(org_path+f, sf))]
        for im_path in file_list:
            tail = f+"/"+im_path
            url = root_folder + "diff/" + sub_path + f + "/"
            im1 = Image.open(org_path + tail)
            im2 = Image.open(collude_path + tail)
            idiff = ImageChops.subtract(im1, im2)
            createFolder(url)
            idiff.save(url + im_path)


    end_time = time.clock()
    print("End at", end_time, ", completed in", end_time - start_time, "s")


def p_collude(root, path, window_length):
    im_list = []
    for im_path in glob.glob(root + path + "/*.tiff"):
        image = imread(im_path)
        im_list.append([im_path, image])

    N = len(im_list)
    L = window_length
    for idx, im in enumerate(im_list):
        if 0 <= idx < L:
            im_estimate = avg_img(im_list, 0, 2*L+1)
        elif L <= idx < N - L:
            im_estimate = avg_img(im_list, idx-L, idx+L+1)
        else:
            im_estimate = avg_img(im_list, N-2*L-1, N)
        im_path = im_list[idx][0]
        dir = root + "collude/" + path
        createFolder(dir)
        im_estimate.save(dir + im_path.split("/")[-1])
    return

def avg_img(im_list, start, end):
    sub = im_list[start:end]
    images = np.array(np.array([im[1] for im in sub]))
    arr = np.array(np.mean(images, axis=(0)), dtype=np.uint8)
    return Image.fromarray(arr)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

# collude("images/", "stego/sq1/", 2)
# diff("images/", "stego/", 2)