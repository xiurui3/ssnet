import os
import shutil

def move_dcm_files(source_folder, target_folder):
    # 遍历源文件夹下的子文件夹
    for subfolder in os.listdir(source_folder):
        subfolder_path = os.path.join(source_folder, subfolder)
        # 检查是否为文件夹
        if os.path.isdir(subfolder_path):
            # 遍历子文件夹下的两个子文件夹
            for sub_subfolder in os.listdir(subfolder_path):
                sub_subfolder_path = os.path.join(subfolder_path, sub_subfolder)
                # 检查是否为文件夹
                if os.path.isdir(sub_subfolder_path):
                    # 遍历子文件夹下的所有dcm文件
                    for file in os.listdir(sub_subfolder_path):
                        # 检查文件是否为dcm文件
                        if file.endswith('.dcm'):
                            # 构建源文件的路径
                            source_file_path = os.path.join(sub_subfolder_path, file)
                            # 构建目标文件的路径
                            target_file_path = os.path.join(target_folder, file)
                            # 移动文件
                            shutil.move(source_file_path, target_file_path)
            # 删除空的子文件夹
            shutil.rmtree(subfolder_path)

# 定义根文件夹的路径
root_folder = './Pancreas-CT'

# 遍历根文件夹下的所有子文件夹
for folder in os.listdir(root_folder):
    folder_path = os.path.join(root_folder, folder)
    # 检查是否为文件夹
    if os.path.isdir(folder_path):
        # 调用函数移动dcm文件并删除子文件夹
        move_dcm_files(folder_path, folder_path)
