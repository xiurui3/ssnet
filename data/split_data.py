# -*- coding: utf-8 -*-
import os
import random

# 定义文件夹路径和文件名列表
folder_path = 'posshypopharyBIG'  # 替换成你的文件夹路径
train_file = 'train.list'
val_file = 'val.list'
test_file = 'test.list'

# 获取文件名列表
file_names = os.listdir(folder_path)
random.shuffle(file_names)  # 随机打乱文件名顺序

# 计算划分数据集的索引
total_files = len(file_names)
train_size = int(total_files * 0.7)
val_size = int(total_files * 0.1)
test_size = total_files - train_size - val_size

# 分割文件名列表
train_set = file_names[:train_size]
val_set = file_names[train_size:train_size + val_size]
test_set = file_names[train_size + val_size:]

# 写入文件列表
def write_file(file_path, data):
    with open(file_path, 'w') as f:
        for item in data:
            f.write(item + '\n')

write_file(train_file, train_set)
write_file(val_file, val_set)
write_file(test_file, test_set)

print(f"Dataset split: Train {len(train_set)}, Validation {len(val_set)}, Test {len(test_set)}")
