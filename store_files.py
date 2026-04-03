import os
import shutil

# 要整理的目标文件夹
# os.path.expanduser("~") 会自动展开成当前用户的家目录
folder_path = os.path.expanduser("~/store_folder")

# 定义“文件类型 -> 对应扩展名”的映射
# 后面程序会根据文件后缀，把文件移动到对应分类里
file_types = {
    "Images": [".jpg", ".png", ".jpeg", "heic"],
    "Videos": [".mp4", ".mov", "mkv"],
    "Documents": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
    "Installers": [ ".dmg", "pkg", "apkg"]
}

# 先创建每个分类文件夹
# exist_ok=True 表示：如果文件夹已经存在，也不要报错
for category in file_types:
    os.makedirs(os.path.join(folder_path, category), exist_ok=True)

# 遍历 store_folder 里的所有内容
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)

    # 先确认当前项目是“普通文件”，不是文件夹
    if os.path.isfile(file_path):

        # 如果这个文件的后缀不在我们定义的所有类型里，就跳过
        if not any(file.lower().endswith(ext) for exts in file_types.values() for ext in exts):
            continue

        # 逐个分类检查，找到匹配的类别后就移动进去
        for category, extensions in file_types.items():
            if any(file.lower().endswith(ext) for ext in extensions):
                shutil.move(file_path, os.path.join(folder_path, category, file))
                print(f"Moved {file} to {category}")

print("整理完成 ✅")
