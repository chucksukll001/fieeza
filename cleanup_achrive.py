import os
import shutil
import time

# 源文件夹：下载目录
# 程序会从这里开始扫描文件
downloads_folder = os.path.expanduser("~/Downloads")

# 目标总目录：store_folder
# 整理后的文件会被移动到这里
store_folder = os.path.expanduser("~/store_folder")

# cleanup_bin：放超过 30 天的压缩包
# 可以理解成“归档区”或“暂存区”
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

# 30 天对应的秒数
days_30_in_seconds = 30 * 24 * 60 * 60

# 创建目标文件夹
# 如果文件夹已经存在，不会报错
os.makedirs(store_folder, exist_ok=True)
os.makedirs(cleanup_folder, exist_ok=True)
for category in file_types:
    os.makedirs(os.path.join(store_folder, category), exist_ok=True)

# 先询问用户是否确认执行
# 因为这个脚本会删除文件，所以多一步确认更安全
confirm = input("确认开始整理 Downloads 吗？(y/n): ")
if confirm.lower() != "y":
    print("已取消")
    exit()

# 记录当前时间，后面用来判断压缩包是否“太旧”
current_time = time.time()

# 计数器：用于最后输出统计信息
deleted_count = 0
moved_archive_count = 0
classified_count = 0
skipped_count = 0

# 遍历 Downloads 里的所有内容
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
        # 获取文件最后修改时间
        last_modified_time = os.path.getmtime(file_path)

        # 文件已经放了多久
        file_age = current_time - last_modified_time

        if file_age > days_30_in_seconds:
            target_path = os.path.join(cleanup_folder, file)

            # 如果目标位置已经有同名文件，就先跳过，避免覆盖
            if os.path.exists(target_path):
                print(f"Skipped (already exists in cleanup_bin): {file}")
                skipped_count += 1
            else:
                shutil.move(file_path, target_path)
                print(f"Moved old archive: {file}")
                moved_archive_count += 1
            continue

    # 3. 其他常见文件分类到 store_folder
    # moved 用来记录：这个文件有没有被成功分类移动
    moved = False
    for category, extensions in file_types.items():
        if any(file_lower.endswith(ext) for ext in extensions):
            target_folder = os.path.join(store_folder, category)
            target_path = os.path.join(target_folder, file)

            # 已有同名文件时不覆盖，直接跳过
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
    # 这样可以避免误删或误移动未知类型的文件
    if not moved:
        print(f"Skipped (unsupported type): {file}")
        skipped_count += 1

# 输出最终统计结果，方便知道这次整理做了什么
print("\n整理完成 ✅")
print(f"Deleted temp files: {deleted_count}")
print(f"Moved old archives: {moved_archive_count}")
print(f"Classified files: {classified_count}")
print(f"Skipped files: {skipped_count}")
