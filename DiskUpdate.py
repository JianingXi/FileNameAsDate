from DiskUpdateDict.FileNameAsDate import rename_date
from DiskUpdateDict.UpdateShortcut import update_shortcut_folders
from DiskUpdateDict.DiskUpdateFunc import update_commercial2rar_files

disk_char = "D:"




basedir = r'C:\Users\xijia\Desktop\ToDoList\D20_Done'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\ToDoList\D20_Z_ToEvernote'
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

basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_比赛\24硕黄思敏_中国国际'
rename_date(basedir)

basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_毕设\敖济民'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_毕设\严颖轩'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_毕设\林煌'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_毕设\张姚琪'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20_毕设\李丹'
rename_date(basedir)

# 专业评估材料
basedir = r'C:\Users\xijia\Desktop\ToDoList\D20250212_专业评估材料'
rename_date(basedir)

basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A01通知'
rename_date(basedir)
basedir = r'C:\Users\xijia\Desktop\DoingPlatform\D20250428_教创赛省赛决赛答辩\A03决赛打磨'
rename_date(basedir)

basedir = r'D:\Alpha\J机智\工作业务\Y2025'
rename_date(basedir)



# 硬盘位置确定与硬盘快捷方式更新
# update_shortcut_folders(disk_char)

# 商业报告参考模板备份
# update_commercial2rar_files(disk_char)