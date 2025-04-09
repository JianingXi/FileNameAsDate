import os
import shutil
import math


def split_folder_if_needed(folder, max_files=50):
    """
    检查指定文件夹下的文件数量（不含子文件夹），如果超过 max_files，则拆分为多个子文件夹，
    拆分后的子文件夹名称为原文件夹名称 + 下划线 + 编号。
    """
    # 获取当前目录下所有文件（不包括子目录）
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    num_files = len(files)

    if num_files > max_files:
        # 获取当前文件夹名称
        original_folder_name = os.path.basename(folder)
        # 计算需要拆分的子文件夹数量
        num_splits = math.ceil(num_files / max_files)
        print(f"目录 {folder} 中有 {num_files} 个文件，需要拆分为 {num_splits} 个子文件夹。")

        # 创建拆分用的子文件夹
        split_folders = []
        for i in range(1, num_splits + 1):
            # 子文件夹名称为 原文件夹名称 + 下划线 + 序号
            new_folder = os.path.join(folder, f"{original_folder_name}_{i}")
            os.makedirs(new_folder, exist_ok=True)
            split_folders.append(new_folder)

        # 将文件依次分配到各个拆分子文件夹中，每个子文件夹内文件数量不超过 max_files
        for index, filename in enumerate(files):
            src = os.path.join(folder, filename)
            # 根据文件的序号计算目标子文件夹的索引
            target_index = index // max_files
            dst = os.path.join(split_folders[target_index], filename)
            shutil.move(src, dst)
            print(f"移动文件 {src} -> {dst}")


def process_directory(root_dir):
    """
    递归遍历目录，对每个目录调用 split_folder_if_needed 函数，
    使用 topdown=False 以确保先处理深层目录，再处理父目录。
    """
    for current_dir, subdirs, files in os.walk(root_dir, topdown=False):
        split_folder_if_needed(current_dir)


if __name__ == "__main__":
    # 指定目标目录（路径前加 r 避免转义问题）
    target_directory = r"C:\迅雷下载\【赠送】10000套大学生创新创业计划书word成品互联网+大赛ppt模板商业策划书撰写"

    process_directory(target_directory)

    print("处理完成。")
