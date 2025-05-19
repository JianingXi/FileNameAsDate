import os
import re

def sanitize_name(name):
    """
    去除首尾空格，合并中间多个空格为一个，并将所有空格和短横线替换为下划线。
    """
    # 去除首尾空格，合并中间多个空格为一个
    name = re.sub(r'\s+', ' ', name.strip())
    # 将空格和短横线替换为下划线
    name = re.sub(r'[\s-]+', '_', name)
    return name

def rename_path(path):
    """
    对路径中的每一部分进行名称规范化处理：首尾空格去除，中间空格合并为一个，所有空格和短横线替换为下划线。
    """
    # 拆分路径并逐级替换空格和短横线
    path_parts = path.split(os.sep)
    new_parts = [sanitize_name(part) for part in path_parts]
    new_path = os.sep.join(new_parts)

    # 检查是否需要重命名
    if new_path != path:
        try:
            os.rename(path, new_path)
            print(f"Renamed: {path} -> {new_path}")
        except Exception as e:
            print(f"Error renaming {path}: {e}")
    return new_path

def rename_files_and_folders(directory):
    """
    遍历目录并对所有文件和文件夹进行重命名，按照路径规范化处理。
    """
    # 先处理子文件夹（从深层往浅层遍历，防止路径嵌套问题）
    for root, dirs, files in os.walk(directory, topdown=False):
        # 处理文件
        for filename in files:
            file_path = os.path.join(root, filename)
            rename_path(file_path)

        # 处理文件夹
        for dirname in dirs:
            dir_path = os.path.join(root, dirname)
            rename_path(dir_path)

    # 最后处理根目录
    rename_path(directory)

if __name__ == "__main__":
    target_directory = r'D:'
    rename_files_and_folders(target_directory)
