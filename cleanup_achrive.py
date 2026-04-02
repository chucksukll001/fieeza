import os
import shutil
import time

# 源文件夹：下载目录
downloads_folder = os.path.expanduser("~/Downloads")

# 目标总目录：store_folder
store_folder = os.path.expanduser("~/store_folder")

# cleanup_bin：放超过30天的压缩包
cleanup_folder = os.path.join(store_folder, "cleanup_bin")


# 直接删除的临时文件类型
delete_file_types = [".tmp", ".log"]

# 超过30天才移动到 cleanup_bin 的压缩文件
archive_file_types = [".zip", ".rar", ".7z"]

# 普通分类文件类型
file_types = {
    "Documents": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".txt"],
    "Images": [".jpg", ".jpeg", ".png", ".heic", ".gif", ".webp"],
    "Videos": [".mp4", ".mov", ".mkv", ".avi"],
    "Installers": [".apkg", ".dmg", ".pkg"],
    "Mails": [".msg"]
    }

# 30天秒数
days_30_in_seconds = 30 * 24 * 60 * 60

# 创建目标文件夹
os.makedirs(store_folder, exist_ok=True)
os.makedirs(cleanup_folder, exist_ok=True)
for category in file_types:
    os.makedirs(os.path.join(store_folder, category), exist_ok=True)
#先询问
confirm = input("确认开始整理 Downloads 吗？(y/n): ")
if confirm.lower() != "y":
    print("已取消")
    exit()
# 当前时间
current_time = time.time()

# 计数器
deleted_count = 0
moved_archive_count = 0
classified_count = 0
skipped_count = 0

for file in os.listdir(downloads_folder):
    file_path = os.path.join(downloads_folder, file)

    # 只处理普通文件
    if not os.path.isfile(file_path):
        continue

    file_lower = file.lower()

    # 1. 直接删除临时文件
    if any(file_lower.endswith(ext) for ext in delete_file_types):
        os.remove(file_path)
        print(f"Deleted temp file: {file}")
        deleted_count += 1
        continue

    # 2. 超过30天的压缩文件移到 cleanup_bin
    if any(file_lower.endswith(ext) for ext in archive_file_types):
        last_modified_time = os.path.getmtime(file_path)
        file_age = current_time - last_modified_time

        if file_age > days_30_in_seconds:
            target_path = os.path.join(cleanup_folder, file)

            if os.path.exists(target_path):
                print(f"Skipped (already exists in cleanup_bin): {file}")
                skipped_count += 1
            else:
                shutil.move(file_path, target_path)
                print(f"Moved old archive: {file}")
                moved_archive_count += 1
            continue

    # 3. 其他常见文件分类到 store_folder
    moved = False
    for category, extensions in file_types.items():
        if any(file_lower.endswith(ext) for ext in extensions):
            target_folder = os.path.join(store_folder, category)
            target_path = os.path.join(target_folder, file)

            if os.path.exists(target_path):
                print(f"Skipped (already exists in {category}): {file}")
                skipped_count += 1
            else:
                shutil.move(file_path, target_path)
                print(f"Moved {file} to {category}")
                classified_count += 1

            moved = True
            break

    # 4. 未匹配的文件不动
    if not moved:
        print(f"Skipped (unsupported type): {file}")
        skipped_count += 1

print("\n整理完成 ✅")
print(f"Deleted temp files: {deleted_count}")
print(f"Moved old archives: {moved_archive_count}")
print(f"Classified files: {classified_count}")
print(f"Skipped files: {skipped_count}")