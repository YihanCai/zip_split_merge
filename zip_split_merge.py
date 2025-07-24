import os
import zipfile
import shutil
from tqdm import tqdm
import math

def split_zip_by_size(input_zip, output_prefix, part_size_mb):
    """
    按指定大小拆分 ZIP 文件
    :param input_zip: 输入 ZIP 文件路径
    :param output_prefix: 输出文件前缀
    :param part_size_mb: 每个部分的大小(MB)
    """
    part_size = part_size_mb * 1024 * 1024  # 转换为字节
    file_size = os.path.getsize(input_zip)
    num_parts = math.ceil(file_size / part_size)
    
    with open(input_zip, 'rb') as f:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="拆分进度") as pbar:
            for i in range(num_parts):
                part_num = i + 1
                part_name = f"{output_prefix}.part{part_num:03d}.zip"
                
                with open(part_name, 'wb') as part_file:
                    bytes_written = 0
                    while bytes_written < part_size:
                        chunk = min(1024 * 1024, part_size - bytes_written)  # 每次最多读取1MB
                        data = f.read(chunk)
                        if not data:
                            break
                        part_file.write(data)
                        bytes_written += len(data)
                        pbar.update(len(data))

    print(f"\n拆分完成！共生成 {num_parts} 个部分，每个约 {part_size_mb}MB")

def split_zip_by_parts(input_zip, output_prefix, num_parts):
    """
    按指定数量拆分 ZIP 文件
    :param input_zip: 输入 ZIP 文件路径
    :param output_prefix: 输出文件前缀
    :param num_parts: 要拆分的部分数
    """
    file_size = os.path.getsize(input_zip)
    part_size = math.ceil(file_size / num_parts)
    
    with open(input_zip, 'rb') as f:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="拆分进度") as pbar:
            for i in range(num_parts):
                part_num = i + 1
                part_name = f"{output_prefix}.part{part_num:03d}.zip"
                
                with open(part_name, 'wb') as part_file:
                    bytes_written = 0
                    while bytes_written < part_size:
                        chunk = min(1024 * 1024, part_size - bytes_written)  # 每次最多读取1MB
                        data = f.read(chunk)
                        if not data:
                            break
                        part_file.write(data)
                        bytes_written += len(data)
                        pbar.update(len(data))

    print(f"\n拆分完成！共生成 {num_parts} 个部分")

def merge_zips(input_prefix, output_zip):
    """
    合并多个 ZIP 部分
    :param input_prefix: 输入文件前缀(如 'archive.part')
    :param output_zip: 输出 ZIP 文件路径
    """
    # 找到所有部分文件
    parts = []
    dir_name = os.path.dirname(input_prefix) or '.'
    base_name = os.path.basename(input_prefix)
    
    for f in os.listdir(dir_name):
        if f.startswith(base_name) and f.endswith('.zip'):
            parts.append(os.path.join(dir_name, f))
    
    if not parts:
        print("未找到匹配的部分文件！")
        return
    
    parts.sort()
    total_size = sum(os.path.getsize(p) for p in parts)
    
    with open(output_zip, 'wb') as out_file:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="合并进度") as pbar:
            for part in parts:
                with open(part, 'rb') as in_file:
                    while True:
                        data = in_file.read(1024 * 1024)  # 每次读取1MB
                        if not data:
                            break
                        out_file.write(data)
                        pbar.update(len(data))

    print(f"\n合并完成！输出文件: {output_zip}")

def main():
    print("ZIP 文件拆分与合并工具")
    print("1. 按大小拆分 ZIP 文件")
    print("2. 按数量拆分 ZIP 文件")
    print("3. 合并 ZIP 文件")
    
    choice = input("请选择操作 (1/2/3): ")
    
    if choice == '1':
        input_file = input("输入 ZIP 文件路径: ")
        output_prefix = input("输出文件前缀 (如 'archive'): ")
        part_size = float(input("每个部分的大小(MB): "))
        split_zip_by_size(input_file, output_prefix, part_size)
    elif choice == '2':
        input_file = input("输入 ZIP 文件路径: ")
        output_prefix = input("输出文件前缀 (如 'archive'): ")
        num_parts = int(input("要拆分的部分数量: "))
        split_zip_by_parts(input_file, output_prefix, num_parts)
    elif choice == '3':
        input_prefix = input("输入部分文件前缀 (如 'archive.part'): ")
        output_file = input("输出 ZIP 文件路径: ")
        merge_zips(input_prefix, output_file)
    else:
        print("无效选择！")

if __name__ == "__main__":
    main()