# -*- coding: utf-8 -*-
import os
import tqdm
import argparse
import numpy as np
import pandas as pd
import SimpleITK as sitk


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', type=str, default='../../pancrease/Pancreas/manifest-1599750808610', help='base dir for data')
    parser.add_argument('--meta', type=str, default='./pancreas.csv', help='data split metadata')
    parser.add_argument('--output_dir', type=str, default='./Pancreaspos1', help='outputs')
    return parser.parse_args()


def get_filenames_in_folder(folder_path):
    filenames = []
    # 遍历文件夹下的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 获取文件的完整路径
            file_path = os.path.join(root, file)
            # 获取文件名
            filename = os.path.basename(file_path)
            filenames.append(filename)
    return filenames




def crop_roi(image, label, output_size=(96, 96, 96)):
    assert (image.shape == label.shape)
    w, h, d = label.shape

    tempL = np.nonzero(label)
    minx, maxx = np.min(tempL[0]), np.max(tempL[0])
    miny, maxy = np.min(tempL[1]), np.max(tempL[1])
    minz, maxz = np.min(tempL[2]), np.max(tempL[2])

    px = max(output_size[0] - (maxx - minx), 0) // 2
    py = max(output_size[1] - (maxy - miny), 0) // 2
    pz = max(output_size[2] - (maxz - minz), 0) // 2
    minx = max(minx - px - 25, 0)
    maxx = min(maxx + px + 25, w)
    miny = max(miny - py - 25, 0)
    maxy = min(maxy + py + 25, h)
    minz = max(minz - pz - 25, 0)
    maxz = min(maxz + pz + 25, d)

    image = image[minx:maxx, miny:maxy, minz:maxz].astype(np.float32)
    label = label[minx:maxx, miny:maxy, minz:maxz].astype(np.float32)
    return image, label


def window_ct(inputs, low, high):
    data = np.clip(inputs, low, high)
    return (data - data.min()) / (data.max() - data.min())


def main():
    args = parse_args()
    data_root = args.base_dir
    metadata = pd.read_csv(args.meta)
    output_dir = args.output_dir
    os.makedirs(os.path.join(output_dir, 'train_images1'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'val_images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'train_labels1'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'val_labels'), exist_ok=True)

    train_list = metadata['filename'][metadata['split'] == 'train'].values
    val_list = metadata['filename'][metadata['split'] == 'val'].values
    roots = data_root+'/Pancreas'
    filenames = get_filenames_in_folder(roots)

    for file in filenames:
        image = sitk.ReadImage(os.path.join(data_root, 'Pancreas', file))
        label = sitk.ReadImage(os.path.join(data_root, 'label', 'label00{}.nii.gz'.format(file[-9:-7])))
        current_size = image.GetSize()
        current_spacing = image.GetSpacing()
        new_spacing = (1, 1, 1)
        new_size = [int(current_size[i] * current_spacing[i] / new_spacing[i]) for i in range(len(current_spacing))]
        resampler = sitk.ResampleImageFilter()
        resampler.SetOutputDirection(label.GetDirection())
        resampler.SetOutputSpacing(new_spacing)
        resampler.SetOutputOrigin(label.GetOrigin())
        resampler.SetInterpolator(sitk.sitkLinear)
        resampler.SetSize(new_size)
        image_t = resampler.Execute(image)
        label_t_linear = resampler.Execute(label)
        label_t_data = sitk.GetArrayFromImage(label_t_linear)
        thr = 0.5
        label_t_data = (label_t_data >= thr).astype(np.float32)
        label_t = sitk.GetImageFromArray(label_t_data)
        label_t.SetDirection(image_t.GetDirection())
        label_t.SetSpacing(image_t.GetSpacing())

        image_t_data = sitk.GetArrayFromImage(image_t)
        image_data = window_ct(image_t_data, -150, 300)
        fg_image_data, fg_label_data = crop_roi(image_data, label_t_data)
        fg_image = sitk.GetImageFromArray(fg_image_data)
        fg_label = sitk.GetImageFromArray(fg_label_data)
        fg_image.SetDirection(image_t.GetDirection())
        fg_image.SetSpacing(image_t.GetSpacing())
        sitk.WriteImage(fg_image, os.path.join(output_dir, 'train_images1', file ))
        fg_label.SetDirection(label_t.GetDirection())
        fg_label.SetSpacing(label_t.GetSpacing())
        sitk.WriteImage(fg_label, os.path.join(output_dir, 'train_labels1', file ))



if __name__ == '__main__':
    main()
