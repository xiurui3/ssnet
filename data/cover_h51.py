# -*- coding: utf-8 -*-
import os
import numpy as np
import nibabel as nib
import h5py

# 设置输出的h5文件夹路径
output_folder = 'data1'

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 设置输出图像的大小
# output_size = (256, 256, 64)

# 循环遍历pan-C文件夹中的文件
pan_c_folder = 'R01-001/iamge'
label_folder = 'R01-001/label'
for filename in os.listdir(pan_c_folder):
    if filename.endswith('.nii.gz'):
        file_number = filename.split('_')[-1].split('.')[0]  # 获取文件编号
        label_filename = os.path.join(label_folder, filename)

        # 读取图像和标签
        image_data = nib.load(os.path.join(pan_c_folder, filename)).get_fdata()
        label_data = nib.load(label_filename).get_fdata()

        # # 处理标签
        # label_data = (label_data == 255).astype(np.uint8)
        # w, h, d = label_data.shape
        # tempL = np.nonzero(label_data)
        # minx, maxx = np.min(tempL[0]), np.max(tempL[0])
        # miny, maxy = np.min(tempL[1]), np.max(tempL[1])
        # minz, maxz = np.min(tempL[2]), np.max(tempL[2])
        # px = max(output_size[0] - (maxx - minx), 0) // 2
        # py = max(output_size[1] - (maxy - miny), 0) // 2
        # pz = max(output_size[2] - (maxz - minz), 0) // 2
        # minx = max(minx - np.random.randint(10, 20) - px, 0)
        # maxx = min(maxx + np.random.randint(10, 20) + px, w)
        # miny = max(miny - np.random.randint(10, 20) - py, 0)
        # maxy = min(maxy + np.random.randint(10, 20) + py, h)
        # minz = max(minz - np.random.randint(5, 10) - pz, 0)
        # maxz = min(maxz + np.random.randint(5, 10) + pz, d)
        #
        # # 对图像进行标准化处理
        # image_data = (image_data - np.mean(image_data)) / np.std(image_data)
        # image_data = image_data.astype(np.float32)
        # image_data = image_data[minx:maxx, miny:maxy]
        #
        # # 裁剪标签
        # label_data = label_data[minx:maxx, miny:maxy]

        # 保存为h5文件
        output_filename = os.path.join(output_folder, 'PANCREAS_' + file_number + '.h5')
        with h5py.File(output_filename, 'w') as f:
            f.create_dataset('image', data=image_data, compression="gzip")
            f.create_dataset('label', data=label_data, compression="gzip")

        print(f"Processed file {filename} and saved as {output_filename}")
