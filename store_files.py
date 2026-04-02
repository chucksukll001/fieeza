import os
import shutil

folder_path = os.path.expanduser("~/store_folder")

file_types = {
    "Images": [".jpg", ".png", ".jpeg", "heic"],
    "Videos": [".mp4", ".mov", "mkv"],
    "Documents": [".pdf", ".docx", ".xlsx", ".pptx", ".txt"],
    "Installers": [ ".dmg", "pkg", "apkg"]
}

for category in file_types:
    os.makedirs(os.path.join(folder_path, category), exist_ok=True)

for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    #先确认是文件
    if os.path.isfile(file_path):
        #在进行过滤，过滤不需要的类型
        if not any(file.lower().endswith(ext) for exts in file_types.values() for ext in exts):
            continue

        for category, extensions in file_types.items():
            if any(file.lower().endswith(ext) for ext in extensions):
                shutil.move(file_path, os.path.join(folder_path, category, file))
                print(f"Moved {file} to {category}")
print("整理完成 ✅")