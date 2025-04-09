import os
import shutil
import math
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def split_files_into_folders(source_folder, max_files=50):
    """
    将 source_folder 中的所有文件（不递归子目录）分批移动到多个新文件夹中，
    每个新文件夹内的文件数不超过 max_files。新文件夹名称保留原文件夹名称，
    在末尾添加下划线和编号。

    返回所有新创建的子文件夹路径列表。
    """
    # 获取当前目录下所有文件（不包括子文件夹）
    files = [os.path.join(source_folder, f) for f in os.listdir(source_folder) if
             os.path.isfile(os.path.join(source_folder, f))]
    num_files = len(files)
    if num_files == 0:
        return []

    num_splits = math.ceil(num_files / max_files)
    print(f"源文件夹 '{source_folder}' 中共有 {num_files} 个文件，需要分成 {num_splits} 个子文件夹。")

    # 创建分批文件夹，名称格式为 原文件夹名称_序号
    original_name = os.path.basename(source_folder)
    parent_dir = os.path.dirname(source_folder)
    batch_folders = []
    for i in range(1, num_splits + 1):
        new_folder = os.path.join(parent_dir, f"{original_name}_{i}")
        os.makedirs(new_folder, exist_ok=True)
        batch_folders.append(new_folder)

    # 按序号将文件移动到各个子文件夹中
    for index, file_path in enumerate(files):
        target_folder = batch_folders[index // max_files]
        dst = os.path.join(target_folder, os.path.basename(file_path))
        shutil.move(file_path, dst)
        print(f"移动文件：{file_path} -> {dst}")

    return batch_folders


def upload_folder(driver, folder_path):
    """
    利用 Selenium 模拟操作，将一个文件夹上传到超星学习通网盘。
    假定页面中存在点击上传的按钮及支持文件夹上传的 <input type="file" webkitdirectory> 控件。
    """
    try:
        # 点击上传按钮，打开上传窗口
        upload_button = driver.find_element(By.ID, "uploadBtn")
        upload_button.click()

        # 等待上传控件出现（此处假定支持文件夹上传，且控件有 webkitdirectory 属性）
        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @webkitdirectory]"))
        )

        # 直接发送文件夹路径进行上传
        file_input.send_keys(folder_path)
        print(f"开始上传文件夹：{folder_path}")

        # 根据实际情况等待上传完成
        time.sleep(5)
    except Exception as e:
        print(f"上传文件夹 {folder_path} 时出错：{e}")


def batch_upload_folders(driver, folders):
    """
    依次将列表中的每个文件夹上传到网盘。每次上传一个文件夹。
    """
    for folder in folders:
        upload_folder(driver, folder)
        # 每次上传后等待一段时间（根据实际情况调整）
        time.sleep(5)


if __name__ == "__main__":
    # 待上传的源文件夹（其中所有文件将会被分批移动到多个子文件夹中）
    source_folder = r"C:\Users\xijia\Desktop\待上传文件夹"  # 请根据实际情况修改

    # 先对源文件夹中的文件进行分批（每批不超过50个文件），生成多个子文件夹
    batch_folders = split_files_into_folders(source_folder, max_files=50)
    if not batch_folders:
        print("没有需要上传的文件。")
        exit()

    # 初始化 Selenium 浏览器驱动（确保已安装 chromedriver）
    driver = webdriver.Chrome()

    # 访问超星学习通登录页面（URL 请根据实际情况修改）
    driver.get("https://passport2.chaoxing.com/login?fid=1743926720924")
    print("请在打开的浏览器中完成登录操作，登录成功后在终端按回车继续...")
    input()

    # 登录后，跳转到网盘上传页面（URL 请根据实际情况修改）
    driver.get("https://mooc1-2.chaoxing.com/mycourse/studentstudymain?courseId=xxxx")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "uploadBtn")))

    # 分批上传所有文件夹
    batch_upload_folders(driver, batch_folders)

    print("所有文件夹上传完成。")
    driver.quit()
