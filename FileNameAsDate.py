import os
import shutil
from datetime import datetime


def create_temp_dir(directory):
    """
    创建临时目录。
    """
    temp_dir = os.path.join(directory, 'TempDirForDeleteJustTemp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def sanitize_filename(filename):
    """
    根据特定规则清理文件名。
    """
    replacements = {
        ' ': '_', '-': '_', '—': '_', '。': '_', '：': '_', ':': '_',
        '（': '_', '）': '_', '(': '_', ')': '_'
    }
    for old, new in replacements.items():
        filename = filename.replace(old, new)

    # 处理多个点的情况
    parts = filename.split('.')
    if len(parts) > 2:
        filename = '_'.join(parts[:-1]) + '.' + parts[-1]

    # 删除重复的下划线
    while '__' in filename:
        filename = filename.replace('__', '_')

    # 将 _. 替换为 .
    filename = filename.replace('_.', '.')

    return filename


def prepend_date_to_filename(filename, date):
    """
    在文件名前添加日期信息。
    """
    date_str = date.strftime('D%Y%m%d_')
    if not filename.startswith('D20'):
        filename = date_str + filename
    return filename


def move_files_with_new_names(src_dir, dst_dir):
    """
    将文件从 src_dir 移动到 dst_dir，并更新文件名。
    """
    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)

        if not os.path.isfile(src_path) or filename in ['..', '.']:
            continue

        file_mod_time = datetime.fromtimestamp(os.path.getmtime(src_path))
        new_filename = sanitize_filename(filename)
        new_filename = prepend_date_to_filename(new_filename, file_mod_time)

        dst_path = os.path.join(dst_dir, new_filename)

        if src_path != dst_path:
            print(f"rename {new_filename}")
            shutil.move(src_path, dst_path)


def move_directories_with_new_names(src_dir, dst_dir):
    """
    将目录从 src_dir 移动到 dst_dir，并更新目录名。
    """
    for dirname in os.listdir(src_dir):
        src_path = os.path.join(src_dir, dirname)

        if not os.path.isdir(src_path) or dirname in ['..', '.', 'TempDirForDeleteJustTemp']:
            continue

        dir_mod_time = datetime.fromtimestamp(os.path.getmtime(src_path))
        new_dirname = sanitize_filename(dirname)
        new_dirname = prepend_date_to_filename(new_dirname, dir_mod_time)

        dst_path = os.path.join(dst_dir, new_dirname)

        if src_path != dst_path:
            print(f"rename directory {new_dirname}")
            shutil.move(src_path, dst_path)


def main():
    basedir = r'C:\Users\DELL\Desktop\ToDo'
    if not basedir.endswith('/'):
        basedir += '/'

    temp_dir = create_temp_dir(basedir)

    move_files_with_new_names(basedir, temp_dir)
    move_directories_with_new_names(basedir, temp_dir)

    print('     ----     ')

    move_files_with_new_names(temp_dir, basedir)
    move_directories_with_new_names(temp_dir, basedir)

    os.rmdir(temp_dir)


if __name__ == "__main__":
    main()
