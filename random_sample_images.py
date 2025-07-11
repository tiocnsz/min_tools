import os
import shutil
import random
from pathlib import Path
from datetime import datetime

def sample_images(source_dir, dest_dir, sample_count):
    """
    从每个子文件夹中随机取样指定数量的图片
    
    Args:
        source_dir (str): 源文件夹路径
        dest_dir (str): 目标文件夹路径
        sample_count (int): 每个子文件夹需要取样的图片数量
    """
    # 将源路径和目标路径转换为Path对象
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    # 创建目标文件夹
    dest_path.mkdir(exist_ok=True)
    
    # 获取所有子文件夹
    subdirs = [d for d in source_path.iterdir() if d.is_dir()]
    
    # 遍历每个子文件夹
    for subdir in subdirs:
        # 获取子文件夹中的所有图片文件
        image_files = [f for f in subdir.glob("*") if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}]
        
        if not image_files:
            print(f"警告: {subdir.name} 中没有找到图片文件")
            continue
            
        # 如果图片数量少于要求的取样数量，则使用所有图片
        actual_sample_count = min(sample_count, len(image_files))
        
        # 随机选择图片
        selected_images = random.sample(image_files, actual_sample_count)
        
        # 复制选中的图片到目标文件夹
        for img in selected_images:
            # 创建新的文件名
            new_name = f"{img.name}"
            dest_file = dest_path / new_name
            shutil.copy2(img, dest_file)
            
        print(f"已从 {subdir.name} 中取样 {actual_sample_count} 张图片")

def main():
    # 获取用户输入
    source_dir = input("请输入源文件夹路径: ").strip()
    dest_dir = input("请输入目标文件夹路径: ").strip()
    sample_count = int(input("请输入每个子文件夹需要取样的图片数量: "))
    
    # 检查源文件夹是否存在
    if not os.path.exists(source_dir):
        print("错误：指定的源文件夹不存在！")
        return
        
    # 执行取样
    sample_images(source_dir, dest_dir, sample_count)
    print("\n取样完成！")

if __name__ == "__main__":
    main() 