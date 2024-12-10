import os
import SimpleITK as sitk

# 定义函数，将 DICOM 文件夹转换为 NIfTI 文件
def convert_dicom_to_nifti(dicom_dir, output_path):
    # 读取 DICOM 文件并创建 SimpleITK 图像对象
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dicom_dir)
    reader.SetFileNames(dicom_names)
    dicom_image = reader.Execute()

    # 合并图像对象
    nifti_image = sitk.JoinSeries(dicom_image)

    # 保存为 NIfTI 文件
    sitk.WriteImage(nifti_image, output_path)


# 定义函数，遍历文件夹 A 中的每个子文件夹并进行转换
def convert_folders_in_A(input_folder_A, output_folder):
    # 遍历文件夹 A 中的每个子文件夹
    for folder_name in os.listdir(input_folder_A):
        folder_path = os.path.join(input_folder_A, folder_name)

        # 忽略非文件夹
        if not os.path.isdir(folder_path):
            continue

        # 生成输出文件路径
        output_path = os.path.join(output_folder, folder_name + ".nii.gz")

        # 调用转换函数将 DICOM 文件夹转换为 NIfTI 文件
        convert_dicom_to_nifti(folder_path, output_path)

        # 删除原始的 DICOM 文件夹
        # shutil.rmtree(folder_path)


# 定义输入文件夹 A 的路径和输出文件夹的路径
input_folder_A = "./Pancreas-CT"
output_folder = "./pan-Cl"

# 执行转换
convert_folders_in_A(input_folder_A, output_folder)
