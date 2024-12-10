import os
import wandb
import numpy as np
import nibabel as nib

import torch
import torch.nn as nn
import torch.nn.functional as F
from base.base_modules import TensorBuffer, NegativeSamplingPixelContrastiveLoss

os.environ['CUDA_VISIBLE_DEVICES'] = '1'
contrastive_loss = NegativeSamplingPixelContrastiveLoss(sample_num=400,
                                                                     bidirectional=True, temperature=0.1)


project_l_t1 = torch.ones(4,4,112,112).cuda()
project_l_t2 = torch.ones(4,4,112,112).cuda()
project_l_negative= torch.ones(4,4,112,112).cuda()
map_l_positive = torch.ones(4,4,112,112).cuda()
map_l_negative = torch.ones(4,4,112,112).cuda()

contrastive_l_loss = contrastive_loss(project_l_t1,project_l_t2,project_l_negative,input_seg=map_l_positive,negative_seg=map_l_negative)