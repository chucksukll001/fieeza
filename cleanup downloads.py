import os
import shutil
import time

# 要整理的下载文件夹
downloads_folder = os.path.expanduser("~/Downloads")

# 清理箱文件夹
# 用来存放“暂时不想删，但也不想继续留在 Downloads 里”的旧压缩包
cleanup_folder = os.path.expanduser("~/store_folder/cleanup_bin")

# 直接删除的临时文件类型
delete_file_types = [".tmp", ".log"]

# 超过 30 天未修改，才移动走的压缩文件类型
archive_file_types = [".zip", ".rar", ".7z"]

# 30 天对应的秒数
# 因为文件时间通常是用“秒”来计算，所以先把 30 天换算好
days_30_in_seconds = 30 * 24 * 60 * 60

# 创建 cleanup_bin 文件夹
os.makedirs(cleanup_folder, exist_ok=True)

# 记录“现在”的时间，后面用它和文件最后修改时间比较
current_time = time.time()

# 遍历 Downloads 里的所有内容
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
        # 取出文件的“最后修改时间”
        last_modified_time = os.path.getmtime(file_path)

        # 文件年龄 = 当前时间 - 最后修改时间
        file_age = current_time - last_modified_time

        if file_age > days_30_in_seconds:
            target_path = os.path.join(cleanup_folder, file)

            # 如果清理箱里已经有同名文件，就跳过，避免覆盖
            if os.path.exists(target_path):
                print(f"Skipped (already exists in cleanup_bin): {file}")
            else:
                shutil.move(file_path, target_path)
                print(f"Moved old archive: {file}")

print("清理完成 ✅")
