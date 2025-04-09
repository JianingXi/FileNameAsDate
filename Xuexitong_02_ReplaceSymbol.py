import os
import re

# 要替换的特殊符号列表
SPECIAL_CHARS = r'~!@#$%^&*+<>?:"{},\\;\[\]/ '

# 构造正则表达式：匹配上述任意一个字符
pattern = re.compile(f"[{re.escape(SPECIAL_CHARS)}]")

def clean_name(name):
    """
    将名称中的特殊字符替换为下划线，并合并多个下划线为一个
    """
    # 替换所有特殊字符为下划线
    new_name = pattern.sub("_", name)
    # 合并连续的下划线
    new_name = re.sub(r'_+', '_', new_name)
    return new_name

def get_unique_name(directory, new_name):
    """
    检查目标目录中是否已存在相同名称的文件/文件夹，如果存在，则在结尾加 _数字 直到不冲突
    """
    base, ext = os.path.splitext(new_name)
    candidate = new_name
    counter = 1
    while os.path.exists(os.path.join(directory, candidate)):
        candidate = f"{base}_{counter}{ext}"
        counter += 1
    return candidate

def rename_recursively(root_dir):
    """
    递归遍历目录（从最深层开始），对所有文件和文件夹进行重命名
    """
    # 使用topdown=False确保先处理子文件夹，再处理父文件夹
    for current_root, dirs, files in os.walk(root_dir, topdown=False):
        # 先处理文件
        for filename in files:
            old_path = os.path.join(current_root, filename)
            new_filename = clean_name(filename)
            # 如果名称未改变则跳过
            if new_filename == filename:
                continue
            # 检查是否存在重名
            new_filename = get_unique_name(current_root, new_filename)
            new_path = os.path.join(current_root, new_filename)
            try:
                os.rename(old_path, new_path)
                print(f"重命名文件: {old_path} -> {new_path}")
            except Exception as e:
                print(f"重命名文件 {old_path} 时出错: {e}")

        # 再处理目录
        for dirname in dirs:
            old_dir_path = os.path.join(current_root, dirname)
            new_dirname = clean_name(dirname)
            if new_dirname == dirname:
                continue
            new_dirname = get_unique_name(current_root, new_dirname)
            new_dir_path = os.path.join(current_root, new_dirname)
            try:
                os.rename(old_dir_path, new_dir_path)
                print(f"重命名文件夹: {old_dir_path} -> {new_dir_path}")
            except Exception as e:
                print(f"重命名文件夹 {old_dir_path} 时出错: {e}")

if __name__ == "__main__":
    # 指定要处理的目录，修改为你需要操作的目录路径
    target_directory = r"D:\Alpha\StoreLatestYears\Store2025\B教学_教学与人才培养_A03_学生竞赛"
    if not os.path.isdir(target_directory):
        print("错误: 指定的路径不是一个有效的目录!")
        exit(1)
    rename_recursively(target_directory)
    print("处理完成!")
