import os


def remove_empty_folders(path):
    """
    递归删除空文件夹
    :param path: 要清理的目录路径
    :return: 删除的文件夹数量
    """
    deleted_count = 0

    # 遍历目录树（自底向上）
    for root, dirs, files in os.walk(path, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)

            try:
                # 检查文件夹是否为空
                if not os.listdir(folder_path):
                    os.rmdir(folder_path)
                    print(f"已删除空文件夹: {folder_path}")
                    deleted_count += 1
            except Exception as e:
                print(f"无法删除 {folder_path}: {e}")

    return deleted_count


if __name__ == "__main__":
    target_directory = r"D:\\"  # 目标目录

    # 安全确认
    print(f"即将扫描并删除空文件夹: {target_directory}")
    print("警告: 此操作不可逆！")
    confirm = input("确认要继续吗？(y/n): ").strip().lower()

    if confirm == 'y':
        print("开始扫描...")
        count = remove_empty_folders(target_directory)
        print(f"操作完成，共删除 {count} 个空文件夹")
    else:
        print("操作已取消")