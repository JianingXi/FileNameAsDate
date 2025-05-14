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
    move_commercial2rar_files(source_path, target_path)
