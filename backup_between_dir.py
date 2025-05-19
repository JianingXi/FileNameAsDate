import os
from DiskUpdateDict.DiskUpdateFunc import get_files_within_depth, split_txt_by_type, refine_file_paths
from DiskUpdateDict.DiskUpdateFunc import backup_between_dir

base_directory_1 = r'C:\Users\xijia\Desktop\A项目_科研与教改项目_A01_科研项目申请评议'
file_list_txt_1 = r'C:\Users\xijia\Desktop\新建文件夹\text1.txt'

# 执行路径扫描并保存
get_files_within_depth(base_directory_1, file_list_txt_1)

base_directory_2 = r'C:\Users\xijia\Desktop\A项目_科研与教改项目_A01_科研项目申请评议1'
file_list_txt_2 = r'C:\Users\xijia\Desktop\新建文件夹\text2.txt'

# 执行路径扫描并保存
get_files_within_depth(base_directory_2, file_list_txt_2)

# 文件列表的文件夹和文件拆分
dir_output_path_1, file_output_path_1 = split_txt_by_type(file_list_txt_1, base_directory_1)
dir_output_path_2, file_output_path_2 = split_txt_by_type(file_list_txt_2, base_directory_2)

# 规范文件名列表，删除无效文件名
file_output_path_1t = refine_file_paths(file_output_path_1, base_directory_1)
file_output_path_2t = refine_file_paths(file_output_path_2, base_directory_2)

# 同步前三层的文件
backup_between_dir(base_directory_1, base_directory_2, file_output_path_1t, file_output_path_2t)

# 同步三层后的文件夹
#print_directories