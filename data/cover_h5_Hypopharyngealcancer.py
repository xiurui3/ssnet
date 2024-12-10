# -*- coding: utf-8 -*-
import os
import numpy as np
import nibabel as nib
import h5py

# 设置输出的h5文件夹路径
output_folder = 'posshypopharyBIG'

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# # 提取第一个文件夹中文件的通用部分
# file1_base = "R01-001.nii_extracted_slice_232_area_60.nii"
#
# # 构建第二个文件的文件名
# file2_base = file1_base.replace("extracted_slice", "extracted_roi_slice")


# 循环遍历pan-C文件夹中的文件
ima_c_folder = 'hypopharyBIG/image'
label_folder = 'hypopharyBIG/label'
for filename in os.listdir(ima_c_folder):
    if filename.endswith('.nii.gz'):
        file1_base = filename
        file1_num = file1_base[:-7]
        file2_base = file1_base.replace("extracted_slice", "extracted_roi_slice")
        # file_number = filename.split('_')[-1].split('.')[0]  # 获取文件编号
        # label_filename = os.path.join(label_folder, filename)

        # 读取图像和标签
        image_data = nib.load(os.path.join(ima_c_folder, file1_base)).get_fdata()
        label_data = nib.load(os.path.join(label_folder, file2_base)).get_fdata()



        # 保存为h5文件
        output_filename = os.path.join(output_folder, file1_num + '.h5')
        with h5py.File(output_filename, 'w') as f:
            f.create_dataset('image', data=image_data, compression="gzip")
            f.create_dataset('label', data=label_data, compression="gzip")

        print(f"Processed file {filename} and saved as {output_filename}")
