import os


def rename_files_in_directory(directory, old_str, new_str):
    """
    递归遍历目录，重命名包含特定字符串的文件
    :param directory: 要遍历的目录路径
    :param old_str: 要替换的旧字符串
    :param new_str: 要替换成的新字符串
    """
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if old_str in filename:
                # 构造旧文件路径和新文件路径
                old_path = os.path.join(root, filename)
                new_filename = filename.replace(old_str, new_str)
                new_path = os.path.join(root, new_filename)

                try:
                    # 重命名文件
                    os.rename(old_path, new_path)
                    print(f"重命名成功: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"重命名失败 {old_path}: {e}")

        # 同样处理目录名（如果需要）
        for dirname in dirs[:]:  # 使用副本遍历，因为我们可能修改dirs
            if old_str in dirname:
                old_dirpath = os.path.join(root, dirname)
                new_dirname = dirname.replace(old_str, new_str)
                new_dirpath = os.path.join(root, new_dirname)

                try:
                    os.rename(old_dirpath, new_dirpath)
                    print(f"重命名目录成功: {old_dirpath} -> {new_dirpath}")
                    # 更新遍历列表，因为目录名已更改
                    dirs[dirs.index(dirname)] = new_dirname
                except Exception as e:
                    print(f"重命名目录失败 {old_dirpath}: {e}")


if __name__ == "__main__":
    # 设置要处理的目录路径
    target_directory = r"C:\迅雷下载"

    # 检查路径是否存在
    if not os.path.isdir(target_directory):
        print("错误: 指定的路径不是一个有效的目录!")
        exit(1)


    """
    需替换的字符串候选：
    
    """


    # 定义要替换的字符串
    old_string = "--鹿鹿文化"
    new_string = ""

    print(f"开始处理目录: {target_directory}")
    print(f"将把文件名中的 '{old_string}' 替换为 '{new_string}'")

    # 执行重命名
    rename_files_in_directory(target_directory, old_string, new_string)

    print("处理完成!")