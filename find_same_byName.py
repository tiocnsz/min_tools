import os
import shutil
from pathlib import Path
from tqdm import tqdm
import time
import concurrent.futures
from queue import Queue
import threading

def process_file(file_path, reference_names, file_extensions):
    """处理单个文件的函数"""
    if file_path.is_file():
        if file_extensions is None or file_path.suffix.lower() in file_extensions:
            if file_path.stem in reference_names:
                return file_path
    return None

def find_and_copy_files(folder_f, folder_a, output_dir, file_extensions=None):
    """
    根据文件夹F中的文件名在文件夹A中查找相同名称的文件并复制
    
    Args:
        folder_f (str): 包含参考文件名的文件夹路径
        folder_a (str): 需要搜索的文件夹路径
        output_dir (str): 输出文件夹路径
        file_extensions (set): 要处理的文件扩展名集合，如 {'.jpg', '.png'}
    """
    start_time = time.time()
    
    # 转换为Path对象
    folder_f_path = Path(folder_f)
    folder_a_path = Path(folder_a)
    output_path = Path(output_dir)
    
    # 创建输出目录（如果不存在）
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("正在收集参考文件夹中的文件名...")
    # 获取文件夹F中的所有文件名（不含后缀）
    reference_names = set()
    for f in tqdm(folder_f_path.glob("*"), desc="处理参考文件夹"):
        if f.is_file():
            if file_extensions is None or f.suffix.lower() in file_extensions:
                reference_names.add(f.stem)
    
    print(f"参考文件夹中共有 {len(reference_names)} 个唯一文件名")
    
    # 在文件夹A中递归搜索文件
    found_files = []
    print("\n开始搜索匹配文件...")
    
    # 获取所有需要处理的文件路径
    all_files = list(folder_a_path.rglob("*"))
    
    # 创建进度条
    pbar = tqdm(total=len(all_files), desc="搜索文件")
    
    # 创建线程安全的队列来存储结果
    result_queue = Queue()
    
    def update_progress(future):
        """更新进度条的回调函数"""
        pbar.update(1)
        result = future.result()
        if result is not None:
            result_queue.put(result)
    
    # 使用线程池执行文件搜索
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(32, os.cpu_count() * 4)) as executor:
        # 提交所有任务
        futures = [
            executor.submit(process_file, file_path, reference_names, file_extensions)
            for file_path in all_files
        ]
        
        # 添加完成回调
        for future in futures:
            future.add_done_callback(update_progress)
        
        # 等待所有任务完成
        concurrent.futures.wait(futures)
    
    pbar.close()
    
    # 从队列中获取所有结果
    while not result_queue.empty():
        found_files.append(result_queue.get())
    
    # 复制找到的文件到输出目录
    if found_files:
        print(f"\n开始复制 {len(found_files)} 个文件...")
        for file_path in tqdm(found_files, desc="复制文件"):
            # 保持原始文件名
            dest_path = output_path / file_path.name
            # 如果目标文件已存在，添加数字后缀
            counter = 1
            while dest_path.exists():
                dest_path = output_path / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1
            shutil.copy2(file_path, dest_path)
    else:
        print("\n未找到匹配的文件")
    
    end_time = time.time()
    print(f"\n处理完成！")
    print(f"总共找到并复制了 {len(found_files)} 个文件")
    print(f"总耗时: {end_time - start_time:.2f} 秒")

def main():
    # 获取用户输入
    folder_f = input("请输入参考文件夹F的路径: ").strip()
    folder_a = input("请输入需要搜索的文件夹A的路径: ").strip()
    output_dir = input("请输入输出文件夹的路径: ").strip()
    
    # 询问是否需要限制文件类型
    use_file_types = input("是否需要限制文件类型？(y/n): ").strip().lower() == 'y'
    file_extensions = None
    if use_file_types:
        extensions = input("请输入文件扩展名（用逗号分隔，例如：.jpg,.png,.gif）: ").strip()
        file_extensions = {ext.strip().lower() for ext in extensions.split(',')}
    
    # 检查输入路径是否存在
    if not os.path.exists(folder_f):
        print("错误：参考文件夹F不存在！")
        return
    if not os.path.exists(folder_a):
        print("错误：搜索文件夹A不存在！")
        return
    
    # 执行查找和复制
    find_and_copy_files(folder_f, folder_a, output_dir, file_extensions)

if __name__ == "__main__":
    main() 