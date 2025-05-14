import os
import shutil
import win32com.client

def remove_shortcuts(directory):
    """
    遍历给定目录及其所有子目录，删除所有扩展名为 .lnk 的文件（快捷方式）。
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 判断文件扩展名是否为 .lnk（忽略大小写）
            if file.lower().endswith('.lnk'):
                shortcut_path = os.path.join(root, file)
                try:
                    os.remove(shortcut_path)
                    print(f"已删除快捷方式：{shortcut_path}")
                except Exception as e:
                    print(f"删除 {shortcut_path} 时出错：{e}")

def create_shortcut(target, shortcut_path, description=""):
    """
    创建一个指向 target 文件夹的快捷方式，并保存到 shortcut_path。
    """
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.Description = description
    shortcut.save()

def collect_shortcut(source_dir, shortcut_dir):

    # 如果目标目录不存在则创建
    if not os.path.exists(shortcut_dir):
        os.makedirs(shortcut_dir)

    # 遍历源目录下的一级目录
    for first_level in os.listdir(source_dir):
        first_level_path = os.path.join(source_dir, first_level)
        if os.path.isdir(first_level_path):
            # 遍历一级目录中的二级目录
            for second_level in os.listdir(first_level_path):
                second_level_path = os.path.join(first_level_path, second_level)
                if os.path.isdir(second_level_path):
                    # 为二级目录创建快捷方式（可根据需要自定义命名规则）
                    shortcut_name = f"{second_level}_{first_level}.lnk"
                    shortcut_path = os.path.join(shortcut_dir, shortcut_name)
                    create_shortcut(second_level_path, shortcut_path, description=second_level_path)
                    print(f"已创建快捷方式: {shortcut_path}")




def create_task_folders(base_path, folder_names_vec):
    # 遍历列表，在指定路径下创建空文件夹
    for folder in folder_names_vec:
        folder_path = os.path.join(base_path, folder)
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"已创建或已存在文件夹：{folder_path}")
        except Exception as e:
            print(f"创建文件夹 {folder_path} 时发生错误：{e}")


def move_shortcuts_into_dirs(shortcut_source, target_folder):

    # 遍历快捷方式文件夹内的所有文件
    for file in os.listdir(shortcut_source):
        if file.lower().endswith('.lnk'):
            # 获取不含扩展名的文件名
            base_name = os.path.splitext(file)[0]
            # 去掉后15个字符，如果长度不足15则取全部
            compare_name = base_name[:-10] if len(base_name) > 10 else base_name

            # 标记是否已匹配到对应的二级目录
            found = False

            # 遍历目标文件夹下的一级目录
            for first_level in os.listdir(target_folder):
                first_level_path = os.path.join(target_folder, first_level)
                if os.path.isdir(first_level_path):
                    # 遍历一级目录下的二级目录
                    for second_level in os.listdir(first_level_path):
                        second_level_path = os.path.join(first_level_path, second_level)
                        if os.path.isdir(second_level_path):
                            # 如果二级目录的名称与处理后的快捷方式名称相同，则移动该快捷方式文件
                            if second_level == compare_name:
                                src_path = os.path.join(shortcut_source, file)
                                dst_path = os.path.join(second_level_path, file)
                                shutil.move(src_path, dst_path)
                                print(f"已将 {file} 移动到 {second_level_path}")
                                found = True
                                break
                    if found:
                        break
            if not found:
                print(f"未找到匹配的二级目录，快捷方式 {file} 未移动。")


def update_shortcut_folders(disk_char: str):
    # disk_char = "D:"

    # 清除失效的旧有快捷方式
    folder_path = r"D:\Alpha"
    folder_path = folder_path.replace("D:", disk_char)
    remove_shortcuts(folder_path)

    # 读取所有的二级目录并创建为快捷方式
    source_dir = r"D:\Alpha\StoreLatestYears"
    shortcut_dir = r"D:\temp"
    source_dir = source_dir.replace("D:", disk_char)
    shortcut_dir = shortcut_dir.replace("D:", disk_char)
    collect_shortcut(source_dir, shortcut_dir)


    # 移动所有快捷方式至相应位置
    shortcut_source = r"D:\temp"
    target_folder = r"D:\Alpha"
    shortcut_source = shortcut_source.replace("D:", disk_char)
    target_folder = target_folder.replace("D:", disk_char)
    move_shortcuts_into_dirs(shortcut_source, target_folder)

    # 确保日常事务文件夹的目录齐全
    base_directory = r"D:\Alpha\M02广医事务性工作"
    base_directory = base_directory.replace("D:", disk_char)
    folder_names_vec = [
        "产学研_产业化工作",
        "产学研_社科科普",
        "产学研_科研工作",
        "人事工作_人才帽子",
        "人事工作_人才补贴政策",
        "人事工作_出境公开",
        "人事工作_提拔调动升职称",
        "人事工作_教师招聘或教师培训",
        "人事工作_职称评审",
        "外界公司",
        "学校党政行政_红头文件",
        "学院党政行政_红头文件",
        "工会后勤宣传保卫等工作",
        "年终绩效总结",
        "教学人才培养_教学学生竞赛",
        "教学人才培养_教改项目论文",
        "教学人才培养_本科教学",
        "教学人才培养_研究生教学",
        "日常整治与安全检查",
        "评审委员_校内校外",
        "财务_经费提醒"
    ]
    create_task_folders(base_directory, folder_names_vec)


    # 确保日常事务文件夹的目录齐全
    base_directory = r"D:\Alpha\StoreLatestYears\Store2024"
    base_directory = base_directory.replace("D:", disk_char)
    folder_names_vec = [
        "A项目_科研与教改项目_A01_科研项目申请评议",
        "A项目_科研与教改项目_A01_科研项目申请评议_A01_申请书讲座",
        "A项目_科研与教改项目_A01_科研项目申请评议_A02_往年基金范本",
        "A项目_科研与教改项目_A02_教改项目申请评议",
        "A项目_科研与教改项目_A03_产业化创新创业赛项目",
        "A项目_科研与教改项目_A04_评奖申请评议",
        "B教学_教学与人才培养_A01_教学培训参加",
        "B教学_教学与人才培养_A02_教学竞赛",
        "B教学_教学与人才培养_A03_学生竞赛",
        "B教学_教学与人才培养_A04_教改社科论文",
        "B教学_教学与人才培养_B01_本科生课程",
        "B教学_教学与人才培养_B01_本科生课程_Z01_一流课程建设",
        "B教学_教学与人才培养_B02_本科生教材",
        "B教学_教学与人才培养_B03_本科生毕设",
        "B教学_教学与人才培养_B05_本科生评审",
        "B教学_教学与人才培养_B06_本科生招生",
        "B教学_教学与人才培养_B10_本科班主任",
        "B教学_教学与人才培养_B11_本科生导师",
        "B教学_教学与人才培养_B21_教学会议参与",
        "B教学_教学与人才培养_B22_教学经验推广",
        "B教学_教学与人才培养_B80_课程录像",
        "B教学_教学与人才培养_B90_监考统计",
        "B教学_教学与人才培养_C00_研究生导师",
        "B教学_教学与人才培养_C01_研究生课程",
        "B教学_教学与人才培养_C02_研究生培养",
        "B教学_教学与人才培养_C02_研究生评审",
        "B教学_教学与人才培养_C03_研究生命题",
        "B教学_教学与人才培养_D01_思政素材",
        "B教学_教学与人才培养_E01_督导_学院",
        "B教学_教学与人才培养_M01_学生推荐信",
        "C科研_科研学术成果_C01学术论文",
        "C科研_科研学术成果_C02知识产权_01专利",
        "C科研_科研学术成果_C02知识产权_02软件著作权",
        "C科研_科研学术成果_C02知识产权_03科普",
        "C科研_科研学术成果_C02知识产权_04专著",
        "C科研_科研学术成果_C10本人会议报告",
        "D服务_评审专家会员担任_A01论文审稿",
        "D服务_评审专家会员担任_A02期刊编辑",
        "D服务_评审专家会员担任_A03审稿编辑证书",
        "D服务_评审专家会员担任_B01科研项目评审",
        "D服务_评审专家会员担任_B02教学项目评审",
        "D服务_评审专家会员担任_B03本科专业评审",
        "D服务_评审专家会员担任_B04产业转化评审",
        "D服务_评审专家会员担任_B05命题审题专家担任",
        "D服务_评审专家会员担任_B06职称评审",
        "D服务_评审专家会员担任_C01教学学会会员",
        "D服务_评审专家会员担任_C02科研学会会员",
        "E建设_学科专业与平台建设_A01_会议举办与专家邀请",
        "E建设_学科专业与平台建设_A02_学校学术会议照片",
        "E建设_学科专业与平台建设_A03_学院学术会议照片",
        "E建设_学科专业与平台建设_B01_学术会议照片",
        "E建设_学科专业与平台建设_B02_附属医院学科共建",
        "E建设_学科专业与平台建设_B03_学院服务",
        "H照片汇总",
        "M02广医事务性工作"
    ]
    create_task_folders(base_directory, folder_names_vec)
