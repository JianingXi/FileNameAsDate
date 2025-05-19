# ----- 硬盘局部区域目录备份 ----- #
import os
from datetime import datetime
import shutil


def scan_directory(base_dir, output_file):
    """
    扫描 base_dir 目录下的所有文件，包括子目录中的文件，
    严格跳过 $RECYCLE.BIN 及其内部所有文件，并排除 desktop.ini 文件
    """
    # 排除目录前缀，注意：路径分隔符需标准化
    EXCLUDE_PREFIX = os.path.join(base_dir, "$RECYCLE.BIN").lower()
    # 排除文件名，不区分大小写
    EXCLUDE_FILES = {"desktop.ini"}

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for root, _, files in os.walk(base_dir):

                # 标准化路径并转换为小写
                normalized_root = os.path.normpath(root).lower()

                # 如果当前路径是 $RECYCLE.BIN 或其子路径，则跳过
                if normalized_root.startswith(EXCLUDE_PREFIX):
                    continue

                for filename in files:
                    # 排除 desktop.ini 文件（忽略大小写）
                    if filename.lower() in EXCLUDE_FILES:
                        continue

                    # 获取完整路径，并生成相对路径
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, base_dir)

                    # 写入文件路径
                    file.write(relative_path + '\n')

        # print(f"扫描完成，文件路径已保存到 {output_file}")
    except Exception as e:
        print(f"发生错误：{e}")


def get_file_info(file_path):
    """ 获取文件的元数据信息，包括 modified_time """
    try:
        stat_info = os.stat(file_path)
        return {
            "name": os.path.basename(file_path),
            "size": stat_info.st_size,
            "modified_time": stat_info.st_mtime
        }
    except FileNotFoundError:
        print(f"[Error] File not found: {file_path}")
        return None
    except PermissionError:
        print(f"[Error] Permission denied: {file_path}")
        return None


def format_timestamp(timestamp):
    """ 将时间戳格式化为可读时间 """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def compare_files(file1, file2):
    """
    比较两个文件的元数据信息，并返回：
    - all_equal_except_create: 布尔值，仅比较 name 和 size 是否一致，不考虑 modified_time
    - modified_times: 两个文件的 modified_time 格式化输出
    """
    info1 = get_file_info(file1)
    info2 = get_file_info(file2)

    # 文件不存在或权限错误，直接返回
    if not info1 or not info2:
        return False, ["N/A", "N/A"]

    # 获取 modified_time（用于输出，不用于比较 all_equal_except_create）
    modified_times = [format_timestamp(info1["modified_time"]), format_timestamp(info2["modified_time"])]

    # 比较 `name` 和 `size`，不考虑 `modified_time`
    all_equal_except_create = (info1["name"] == info2["name"]) and (info1["size"] == info2["size"])

    print(f"\nComparing Files:\n  - File 1: {file1}\n  - File 2: {file2}")
    print(f"All Equal Except Create Time: {all_equal_except_create}")
    return all_equal_except_create, modified_times


def copy_and_overwrite(src, dst):
    """ 复制并覆盖文件 """
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print(f"[Copied] {src} -> {dst}")


def sanitize_path(path):
    """ 处理路径中的非法字符并标准化路径结构，同时避免转义字符干扰 """
    # 去除首尾空格并处理引号
    path = path.strip().strip('"').strip("'")
    # 处理反斜杠，确保不会被识别为转义字符，同时保留空格和连字符
    path = path.replace('\\', os.sep).replace('/', os.sep)
    # 规范路径结构
    path = os.path.normpath(path)
    # 调试信息：输出处理后的路径
    return path


def compare_files_from_txt(base_directory_1, base_directory_2, file1_path, file2_path):
    """
    遍历第一个文件中的每个路径，并逐一与第二个文件中的路径进行文件名比较。
    如果文件名匹配，则比较 modified_time，并更新时间较新的文件到另一个目录。
    如果文件名不匹配，则直接复制文件到目标目录。
    兼容文件名中的空格、点号以及特殊字符。
    """
    try:
        # 读取第二个文件列表并生成完整路径列表
        with open(file2_path, 'r', encoding='utf-8') as f2:
            file2_list = [sanitize_path(os.path.join(base_directory_2, line)) for line in f2 if line.strip()]

        if not file2_list:
            print("[Warning] 第二个文件列表为空")
            return

        # 逐行读取第一个文件
        with open(file1_path, 'r', encoding='utf-8') as f1:
            for line1 in f1:
                relative_path_1 = sanitize_path(line1)
                if not relative_path_1:
                    continue

                file1_full_path = os.path.join(base_directory_1, relative_path_1)
                file1_full_path = sanitize_path(file1_full_path)
                file1_name = os.path.basename(file1_full_path)

                if not os.path.exists(file1_full_path):
                    print(f"[Warning] File not found: {file1_full_path}")
                    continue

                file1_modified_time = os.path.getmtime(file1_full_path)
                found_match = False

                for file2_full_path in file2_list:
                    file2_full_path = sanitize_path(file2_full_path)

                    if not os.path.exists(file2_full_path):
                        continue

                    file2_name = os.path.basename(file2_full_path)

                    if file1_name == file2_name:
                        found_match = True
                        file2_modified_time = os.path.getmtime(file2_full_path)

                        if file1_modified_time > file2_modified_time:
                            copy_and_overwrite(file1_full_path, file2_full_path)
                        elif file2_modified_time > file1_modified_time:
                            copy_and_overwrite(file2_full_path, file1_full_path)

                if not found_match:
                    target_path_in_2 = os.path.join(base_directory_2, relative_path_1)
                    target_path_in_2 = sanitize_path(target_path_in_2)
                    copy_and_overwrite(file1_full_path, target_path_in_2)

        # 遍历第二个文件
        with open(file2_path, 'r', encoding='utf-8') as f2:
            for line2 in f2:
                relative_path_2 = sanitize_path(line2)
                if not relative_path_2:
                    continue

                file2_full_path = os.path.join(base_directory_2, relative_path_2)
                file2_full_path = sanitize_path(file2_full_path)
                file2_name = os.path.basename(file2_full_path)

                if not os.path.exists(file2_full_path):
                    continue

                match_found = False

                with open(file1_path, 'r', encoding='utf-8') as f1:
                    for line1 in f1:
                        relative_path_1 = sanitize_path(line1)
                        file1_name = os.path.basename(relative_path_1)

                        if file2_name == file1_name:
                            match_found = True
                            break

                if not match_found:
                    target_path_in_1 = os.path.join(base_directory_1, relative_path_2)
                    target_path_in_1 = sanitize_path(target_path_in_1)
                    copy_and_overwrite(file2_full_path, target_path_in_1)

    except Exception as e:
        print(f"[Error] {e}")



def backup_between_dir(base_directory_1: str, base_directory_2: str, temp_txt_file_1: str, temp_txt_file_2: str):
    """
    先对两个文件夹扫描，在根据所生产的txt文件列表，进行相互备份
    :param base_directory_1:
    :param base_directory_2:
    :param temp_txt_file_1:
    :param temp_txt_file_2:
    :return:
    """
    # 执行扫描并写入文件
    scan_directory(base_directory_1, temp_txt_file_1)
    scan_directory(base_directory_2, temp_txt_file_2)

    # 执行比较与同步
    compare_files_from_txt(base_directory_1, base_directory_2, temp_txt_file_1, temp_txt_file_2)


# ----- 对目录里的文件夹，读取深度为三层的文件夹/文件的地址 ----- #

def get_files_within_depth(base_dir, output_file, max_depth=3):
    """
    遍历目录，并将深度为三层以内的文件路径（从基目录开始的相对路径）存储到指定文件中，
    同时保存第三级别的文件夹名字（前提是该文件夹中的文件没有被展示）。

    Args:
        base_dir (str): 起始目录路径。
        output_file (str): 输出文件路径。
        max_depth (int): 最大深度，默认为 3 层。
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            # 用于记录第三级别文件夹是否已展示文件
            displayed_folders = set()

            # 遍历起始目录
            for root, dirs, files in os.walk(base_dir):
                # 计算当前路径的深度（基于分隔符数量）
                depth = root[len(base_dir):].count(os.sep)

                # 处理符合深度要求的文件
                if depth <= max_depth:
                    for file_name in files:
                        # 获取完整路径
                        file_path = os.path.join(root, file_name)
                        # 生成相对路径
                        relative_path = os.path.relpath(file_path, base_dir)

                        # 第三级别的文件路径
                        if depth == max_depth:
                            # 标记该文件所在的文件夹为已展示文件
                            displayed_folders.add(root)
                            # 写入文件路径
                            file.write(relative_path + '\n')

                        # 第二级及以下的文件路径，直接展示
                        elif depth < max_depth:
                            file.write(relative_path + '\n')

                # 对于第三级别文件夹，如果未展示任何内部文件，则展示文件夹路径
                if depth == max_depth:
                    for dir_name in dirs:
                        dir_path = os.path.join(root, dir_name)

                        # 如果该文件夹未展示任何文件，则展示文件夹路径
                        if dir_path not in displayed_folders:
                            relative_dir_path = os.path.relpath(dir_path, base_dir)
                            file.write(f"{relative_dir_path}/\n")

    except Exception as e:
        print(f"[Error] {e}")


def split_txt_by_type(input_txt_path: str, base_directory: str):
    """
    把txt列表中的文件和文件夹进行拆分
    :param input_txt_path: 要拆分文件夹和文件的txt列表
    :param base_directory: 要解析文件的目录地址
    :return: 拆分后的txt名称
    """
    input_path = Path(input_txt_path)
    base_dir = Path(base_directory)

    # 输入文件与基准路径检查
    if not input_path.is_file():
        print(f"输入文件无效：{input_txt_path}")
        return
    if not base_dir.is_dir():
        print(f"基准目录无效：{base_directory}")
        return

    # 输出文件路径：存储在输入文件所在目录中
    output_dir = input_path.parent
    dir_output_path = output_dir / f"{input_path.stem}_dir.txt"
    file_output_path = output_dir / f"{input_path.stem}_file.txt"

    # 清空现有文件内容，避免追加模式
    open(dir_output_path, 'w').close()
    open(file_output_path, 'w').close()

    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(dir_output_path, 'a', encoding='utf-8') as dir_outfile, \
         open(file_output_path, 'a', encoding='utf-8') as file_outfile:

        for line in infile:
            line = line.strip()
            if not line:
                continue

            # 拼接路径
            full_path = base_dir / line
            # print(f"解析路径：{line} -> {full_path}")

            if full_path.exists():
                resolved_path = full_path.resolve()
                # print(f"路径有效：{resolved_path}")

                if resolved_path.is_dir():
                    dir_outfile.write(f"{resolved_path}\n")
                    # print(f"写入目录：{resolved_path}")
                elif resolved_path.is_file():
                    file_outfile.write(f"{resolved_path}\n")
                    # print(f"写入文件：{resolved_path}")
            else:
                print(f"路径无效或不存在：{full_path}")
    return dir_output_path, file_output_path

import os
from pathlib import Path
import re

def sanitize_name(name):
    """
    规范化文件名：
    - 去除首尾空格；
    - 合并多个空格为一个；
    - 空格和短横线统一替换为下划线。
    """
    # 去除首尾空格并合并多个空格为一个
    name = re.sub(r'\s+', ' ', name.strip())
    # 将空格和短横线统一替换为下划线
    name = re.sub(r'[\s-]+', '_', name)
    return name


def refine_file_paths(input_file_path, base_dir):
    """
    对无效临时文件的文件名进行剔除，对文件路径进行统一规范化处理，
    将空格和短横线替换为下划线。

    Args:
        input_file_path (str): 文件名称列表txt文件路径，每行一个文件路径。
        base_dir (str): 要解析文件的基目录地址。

    Returns:
        str: output_file_path 规范后的文件名组成的txt列表路径。
    """

    # 规范化 base_dir，确保末尾不带路径分隔符
    base_dir = os.path.normpath(base_dir)

    # 生成输出文件路径
    input_path = Path(input_file_path)
    output_file_path = input_path.with_name(f"{input_path.stem}_refine.txt")

    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w',
                                                                      encoding='utf-8') as outfile:
        for line in infile:
            # 去除首尾空白符
            line = line.strip()

            # 跳过无效行和临时文件
            if not line or '~WRL' in line or line.endswith('.tmp'):
                continue

            # 规范化路径，不更改路径内部的空格
            abs_path = os.path.normpath(line)

            # 路径有效性检查
            if os.path.exists(abs_path):
                try:
                    # 获取相对路径
                    relative_path = os.path.relpath(abs_path, base_dir)

                    # 处理路径中的每个部分
                    path_parts = relative_path.split(os.sep)
                    normalized_parts = [sanitize_name(part) for part in path_parts]

                    # 合并路径并输出
                    normalized_path = os.sep.join(normalized_parts)
                    outfile.write(normalized_path + '\n')

                except ValueError:
                    # 如果路径不在 base_dir 中，则跳过
                    print(f"Skipped: {abs_path}")

    return str(output_file_path)



def print_directories(input_file_path):
    """
    读取 txt 文件中的目录路径，并逐行打印每个路径作为变量。

    Args:
        input_file_path (str): txt 文件路径，每行一个文件夹路径。
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                directory = line.strip()
                if directory:
                    print(f"Directory Path: {directory}")

    except FileNotFoundError:
        print(f"文件未找到: {input_file_path}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    # 示例输入文件路径
    input_file_path = r'C:\Users\xijia\Desktop\新建文件夹\directories.txt'
    print_directories(input_file_path)





# ----- 商业报告参考模板 专属备份 ----- #
import subprocess
from pathlib import Path
import shutil


def compress_folder_to_rar(folder_path, rar_exe_path):
    folder_path = Path(folder_path)
    rar_name = folder_path.parent / f"{folder_path.name}.rar"
    cmd = [rar_exe_path, 'a', str(rar_name), f"{folder_path.name}"]
    try:
        subprocess.run(cmd, check=True, cwd=folder_path.parent)
    except subprocess.CalledProcessError as e:
        print(f"Compression failed for {folder_path}: {e}")



rar_exe_path = r'C:\Program Files\WinRAR\rar.exe'
def find_and_compress_folders(base_path, rar_exe_path):
    base_path = Path(base_path)
    for folder in base_path.iterdir():
        if folder.is_dir() and folder.name.endswith("商业报告参考模板"):
            try:
                compress_folder_to_rar(folder, rar_exe_path)
                print(f"Compressed: {folder}")
            except Exception as e:
                print(f"Error compressing {folder}: {e}")


def delete_matching_folders(base_path):
    base_path = Path(base_path)

    # 获取所有一级目录中的文件夹和RAR压缩包
    folders = [folder for folder in base_path.iterdir() if folder.is_dir() and folder.name.endswith("商业报告参考模板")]
    rar_files = [rar.stem for rar in base_path.iterdir() if
                 rar.suffix == '.rar' and rar.name.endswith("商业报告参考模板.rar")]

    # 检查匹配并删除文件夹
    for folder in folders:
        if folder.name in rar_files:
            try:
                shutil.rmtree(folder)
                print(f"Deleted folder: {folder}")
            except Exception as e:
                print(f"Failed to delete {folder}: {e}")


import os
import shutil
from pathlib import Path


def move_commercial2rar_files(source_path, target_path):
    source_path = Path(source_path)
    target_path = Path(target_path)

    # 创建目标路径（如果不存在）
    target_path.mkdir(parents=True, exist_ok=True)

    # 遍历源目录中的文件，查找结尾为“商业报告参考模板.rar”的压缩包
    for rar_file in source_path.iterdir():
        if rar_file.suffix == ".rar" and rar_file.name.endswith("商业报告参考模板.rar"):
            try:
                destination = target_path / rar_file.name
                shutil.move(str(rar_file), str(destination))
                print(f"Moved: {rar_file} to {destination}")
            except Exception as e:
                print(f"Failed to move {rar_file}: {e}")


def update_commercial2rar_files(disk_char: str):
    # disk_char = "D:"

    source_path = r'C:\Users\xijia\Desktop\ToDoList\D20_ToHardDisk'
    target_path = r'D:\Alpha\StoreLatestYears\Store2025\B教学_教学与人才培养_A03_学生竞赛\创业计划书外界参考模板'
    target_path = target_path.replace("D:", disk_char)

    find_and_compress_folders(source_path, rar_exe_path)
    delete_matching_folders(source_path)
    move_commercial2rar_files(source_path, target_path)
