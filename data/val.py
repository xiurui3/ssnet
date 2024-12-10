import h5py
import math
import nibabel as nib
import numpy as np
from medpy import metric
import torch
import torch.nn.functional as F
from tqdm import tqdm
from skimage.measure import label
import os
import tqdm
import argparse
import numpy as np
import pandas as pd
import SimpleITK as sitk




h5f = h5py.File('PANCREAS_0004.h5', 'r')
h5f1 = h5py.File('PANCREAS_0005.h5', 'r')
image = h5f['image'][:]
label = h5f['label'][:]
image2 = h5f1['image'][:]
label2 = h5f1['label'][:]
sample = {'image': image, 'label': label.astype(np.uint8)}
image1 = sitk.ReadImage('Pancreas04-1.nii.gz')
label1 = sitk.ReadImage('label0004-1.nii.gz')
image_array = sitk.GetArrayFromImage(image1)
label_array = sitk.GetArrayFromImage(label1)