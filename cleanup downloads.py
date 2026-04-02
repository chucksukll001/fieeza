import os
import shutil
import time

# 下载文件夹
downloads_folder = os.path.expanduser("~/Downloads")

# 清理箱文件夹
cleanup_folder = os.path.expanduser("~/store_folder/cleanup_bin")

# 直接删除的临时文件类型
delete_file_types = [".tmp", ".log"]

# 超过30天未修改才移动的压缩文件类型
archive_file_types = [".zip", ".rar", ".7z"]

# 30天对应的秒数
days_30_in_seconds = 30 * 24 * 60 * 60

# 创建 cleanup_bin 文件夹
os.makedirs(cleanup_folder, exist_ok=True)

# 当前时间
current_time = time.time()

for file in os.listdir(downloads_folder):
    file_path = os.path.join(downloads_folder, file)

    # 只处理普通文件
    if not os.path.isfile(file_path):
        continue

    file_lower = file.lower()

    # 规则1：直接删除 tmp / log
    if any(file_lower.endswith(ext) for ext in delete_file_types):
        os.remove(file_path)
        print(f"Deleted temp file: {file}")
        continue

    # 规则2：超过30天未修改的压缩包，移动到 cleanup_bin
    if any(file_lower.endswith(ext) for ext in archive_file_types):
        last_modified_time = os.path.getmtime(file_path)
        file_age = current_time - last_modified_time

        if file_age > days_30_in_seconds:
            target_path = os.path.join(cleanup_folder, file)

            if os.path.exists(target_path):
                print(f"Skipped (already exists in cleanup_bin): {file}")
            else:
                shutil.move(file_path, target_path)
                print(f"Moved old archive: {file}")

print("清理完成 ✅")