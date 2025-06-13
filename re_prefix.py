import os
import threading
from queue import Queue
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor

def load_file_info(directory_path, pbar):
    """多线程加载文件信息"""
    def is_file(file_name):
        full_path = os.path.join(directory_path, file_name)
        result = os.path.isfile(full_path)
        pbar.update(1)
        return result

    # 获取目录中的所有项目
    all_items = os.listdir(directory_path)
    
    # 创建进度条
    with tqdm(total=len(all_items), desc="加载文件信息") as pbar:
        # 使用线程池处理文件检查
        with ThreadPoolExecutor(max_workers=min(8, len(all_items))) as executor:
            # 使用map处理所有项目
            results = list(executor.map(is_file, all_items))
            
        # 过滤出文件
        files = [item for item, is_file in zip(all_items, results) if is_file]
    
    return files

def rename_worker(queue, pbar):
    while True:
        task = queue.get()
        if task is None:
            break
            
        old_path, new_path = task
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            print(f"\n重命名出错: {str(e)}")
        finally:
            pbar.update(1)
            queue.task_done()

def rename_files_with_prefix(directory_path):
    # 检查目录是否存在
    if not os.path.exists(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在")
        return

    # 多线程加载文件信息
    files = load_file_info(directory_path, tqdm)
    
    if not files:
        print("该目录下没有文件")
        return

    # 询问用户是否需要修改前缀
    current_prefix = input("请输入当前文件的前缀（如果不需要修改前缀，直接按回车）：").strip()
    
    if current_prefix:
        # 修改前缀的情况
        new_prefix = input("请输入新的前缀（直接按回车则删除旧前缀）：").strip()
        
        # 创建任务队列
        task_queue = Queue()
        # 创建进度条
        pbar = tqdm(total=len(files), desc="重命名进度")
        
        # 创建并启动工作线程
        num_threads = min(8, len(files))  # 最多8个线程
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=rename_worker, args=(task_queue, pbar))
            t.start()
            threads.append(t)
        
        # 添加任务到队列
        for file in files:
            if file.startswith(current_prefix):
                new_name = file.replace(current_prefix, new_prefix, 1)
                old_path = os.path.join(directory_path, file)
                new_path = os.path.join(directory_path, new_name)
                task_queue.put((old_path, new_path))
        
        # 添加结束标记
        for _ in range(num_threads):
            task_queue.put(None)
        
        # 等待所有任务完成
        task_queue.join()
        # 等待所有线程结束
        for t in threads:
            t.join()
        
        pbar.close()
            
    else:
        # 询问是否需要新增前缀
        add_prefix = input("是否需要为文件添加新前缀？(y/n): ").strip().lower()
        if add_prefix == 'y':
            new_prefix = input("请输入要添加的前缀：").strip()
            if not new_prefix:
                print("错误：新前缀不能为空")
                return
            
            # 创建任务队列
            task_queue = Queue()
            # 创建进度条
            pbar = tqdm(total=len(files), desc="重命名进度")
            
            # 创建并启动工作线程
            num_threads = min(8, len(files))  # 最多8个线程
            threads = []
            for _ in range(num_threads):
                t = threading.Thread(target=rename_worker, args=(task_queue, pbar))
                t.start()
                threads.append(t)
            
            # 添加任务到队列
            for file in files:
                new_name = new_prefix + file
                old_path = os.path.join(directory_path, file)
                new_path = os.path.join(directory_path, new_name)
                task_queue.put((old_path, new_path))
            
            # 添加结束标记
            for _ in range(num_threads):
                task_queue.put(None)
            
            # 等待所有任务完成
            task_queue.join()
            # 等待所有线程结束
            for t in threads:
                t.join()
            
            pbar.close()
        else:
            print("操作已取消")

def main():
    print("欢迎使用文件重命名程序！")
    directory_path = input("请输入要处理的目录路径：").strip()
    rename_files_with_prefix(directory_path)

if __name__ == "__main__":
    main() 