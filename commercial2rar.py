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


if __name__ == "__main__":
    base_path = r'C:\Users\xijia\Desktop\ToDoList\D20_ToHardDisk'
    find_and_compress_folders(base_path, rar_exe_path)
    delete_matching_folders(base_path)
