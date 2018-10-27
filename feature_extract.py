import glob
import math
import os

import numpy as np
import pandas as pd
import skimage.measure as measure
from skimage.feature import greycomatrix
from skimage.io import imread
from skimage import exposure
import time
MAX_BINS = 256
FEATURE_FILE = 'feature.csv'


def extract(stego_path, cover_path, save_file=FEATURE_FILE):
    start_time = time.clock()
    print("Starting extract feature at", start_time, "s")
    image_name_list, entropy_list, kurtosis_list, percentile_list, label_list = p_extract(stego_path, 1)
    image_name_list_cover, entropy_list_cover, kurtosis_list_cover, percentile_list_cover, label_list_cover = p_extract(cover_path,0)
    image_name_list.extend(image_name_list_cover)
    entropy_list.extend(entropy_list_cover)
    kurtosis_list.extend(kurtosis_list_cover)
    percentile_list.extend(kurtosis_list_cover)
    label_list.extend(label_list_cover)
    save(save_file, image_name_list, entropy_list, kurtosis_list, percentile_list, label_list)
    end_time = time.clock()
    print("End at", end_time, ", completed in", end_time - start_time, "s")

def p_extract(root_folder, label=0):
    sub_folders = [os.path.join(root_folder, f) for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]

    image_name_list = []
    entropy_list = []
    kurtosis_list = []
    percentile_list = []
    label_list = []

    for folder in sub_folders:
        for file_name in glob.glob(folder + "/*.tiff"):
            image = imread(file_name)
            t_hist, bins = exposure.histogram(image)
            # {pixel : times}
            dhist = dict(zip(bins, t_hist))
            hist = [dhist.get(bin, 0) for bin in range(MAX_BINS)]
            size = image.shape[0]*image.shape[1]

            i_mean = mean(hist, size)
            probs = pdf(hist, size)

            i_kur = kurtosis(hist, size, i_mean, probs)
            i_ent = entropy(image)
            i_cent = percentile25(hist, size, i_mean, probs)

            label_list.append(label)
            kurtosis_list.append(i_kur)
            entropy_list.append(i_ent)
            percentile_list.append(i_cent)
            image_name_list.append(file_name)

    return [image_name_list, entropy_list, kurtosis_list, percentile_list, label_list]


def save(filename, image_name_list, entropy_list, kurtosis_list, percentile_list, label_list):
    raw_data = {
        'image_name': [],
        'entropy': [],
        'kurtosis': [],
        'percentile': [],
        'label': []
    }
    raw_data.get('image_name').extend(image_name_list)
    raw_data.get('entropy').extend(entropy_list)
    raw_data.get('kurtosis').extend(kurtosis_list)
    raw_data.get('percentile').extend(percentile_list)
    raw_data.get('label').extend(label_list)

    df = pd.DataFrame(raw_data, columns=['image_name', 'entropy', 'kurtosis', 'percentile', 'label'])
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv(filename, index=False)


# probability density function
def pdf(histogram=None, size=1):
    return np.array([(float(times)/size) for times in histogram])


# mean: uf
def mean(histogram=None, size=1):
    p = pdf(histogram, size)
    total = len(histogram)
    return np.sum([pixel*p[pixel] for pixel in range(total)])


# kth central moment: mk
def kthmoment(histogram, size, k, uf=None, p=None):
    if uf is None:
        uf = mean(histogram, size)
    if p is None:
        p = pdf(histogram, size)
    return np.sum([((pixel - uf)**k)*p[pixel] for pixel in range(len(histogram))])


def variance(histogram, size, uf=None, p=None):
    m2 = kthmoment(histogram, size, 2, uf, p)
    return m2


def standard_deviation(histogram, size, uf=None, p=None):
    return math.sqrt(variance(histogram, size, uf, p))


def kurtosis(histogram, size, uf=None, p=None):
    m4 = kthmoment(histogram, size, 4, uf, p)
    m2 = kthmoment(histogram, size, 2, uf, p)
    return m4/m2**2


def entropy(image, glcm=None):
    if glcm is None:
        return measure.shannon_entropy(image)
    else:
        return measure.shannon_entropy(glcm)


def cal_glcm(image):
    return greycomatrix(image, [1, 2, 3], [0, np.pi/4, np.pi/2, 3*np.pi/4], symmetric=True, normed=True)


def percentile25(histogram, size, meanf, p=None):
    z25 = -0.67
    deviation_standard = standard_deviation(histogram, size, meanf, p)
    return meanf + z25*deviation_standard

# from PIL import Image, ImaeChops
# im1 = Image.open("images/DCTlenna.png")
# im2 = Image.open("images/lenna.png")
# idiff = ImageChops.subtract(im1, im2)
# hist = idiff.histogram()
# idiff.save('diff_lenna.png')
# w, h = idiff.size
# size = w*h
# i_mean = mean(hist, size)
# probs = pdf(hist, size)
#
# i_kur = kurtosis(hist, size, i_mean, probs)
# i_ent = entropy(imread('diff_lenna.png'))
# i_cent = percentile25(hist, size, i_mean, probs)
# print(i_kur, i_ent, i_cent)