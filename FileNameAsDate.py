import os
import shutil
from datetime import datetime

MAX_PATH_LENGTH = 260  # Maximum path length for Windows
MAX_FILENAME_LENGTH = 100  # Maximum length for filenames to avoid path length issues

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
        '（': '_', '）': '_', '(': '_', ')': '_', ',': '_', ';': '_'
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


def shorten_filename(filename, max_length=MAX_FILENAME_LENGTH):
    """
    将文件名缩短到指定长度。
    """
    if len(filename) > max_length:
        base, ext = os.path.splitext(filename)
        filename = base[:max_length - len(ext)] + ext
    return filename


def ensure_path_length(path, max_length=MAX_PATH_LENGTH):
    """
    确保路径长度不超过指定的最大长度。
    """
    if len(path) > max_length:
        directory, filename = os.path.split(path)
        filename = shorten_filename(filename, max_length - len(directory) - 1)
        path = os.path.join(directory, filename)
    return path


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
        new_filename = shorten_filename(new_filename)

        dst_path = os.path.join(dst_dir, new_filename)
        dst_path = ensure_path_length(dst_path)

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
        new_dirname = shorten_filename(new_dirname)

        dst_path = os.path.join(dst_dir, new_dirname)
        dst_path = ensure_path_length(dst_path)

        if src_path != dst_path:
            print(f"rename directory {new_dirname}")
            shutil.move(src_path, dst_path)


def rename_date(basedir):
    if not basedir.endswith('/'):
        basedir += '/'

    temp_dir = create_temp_dir(basedir)

    move_files_with_new_names(basedir, temp_dir)
    move_directories_with_new_names(basedir, temp_dir)

    print('     ----     ')

    move_files_with_new_names(temp_dir, basedir)
    move_directories_with_new_names(temp_dir, basedir)

    os.rmdir(temp_dir)


basedir = r'C:\Users\xijia\Desktop\ToDoList\D20_Done'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\ToDoList\D20_ToEvernote'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\ToDoList\D20_ToHardDisk'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\ToDoList\D20_ToDailyNotice'
rename_date(basedir)



# Paper
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_论文\D20241115_冯景辉论文'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_论文\D20241214_黄思敏论文'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_论文\D20241219_余宇论文'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_论文\D20250114_孔元元'
rename_date(basedir)


basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_比赛\23级孙波_BME全国赛'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_比赛\23级王玉儿_BME全国赛'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_比赛\23级黄颂_BME全国赛'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_比赛\24级李旭翔_BME全国赛'
rename_date(basedir)

basedir = r'C:\Users\xijia\Desktop\DoingPlatform\教创赛省赛提交\E01_报告素材R1'
rename_date(basedir)


basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_毕设\林煌'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_毕设\张姚琪'
rename_date(basedir)


# 专业评估材料
basedir = r'C:\Users\xijia\Desktop\ToDoList\D20250212_专业评估材料'
rename_date(basedir)

basedir = r'C:\Users\xijia\Desktop\DoingPlatform\教创赛省赛提交\A01_学校通知'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\教创赛省赛提交\E02_申报表'
rename_date(basedir)


basedir = r'C:\MyDocument\教材撰写\E03_原稿二审修改\BK'
rename_date(basedir)





print('--------------all done----------------')
print('   ')
print('--------------all done----------------')

