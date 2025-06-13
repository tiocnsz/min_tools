import os

def rename_files_with_prefix(directory_path):
    # 检查目录是否存在
    if not os.path.exists(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在")
        return

    # 获取目录中的所有文件
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    if not files:
        print("该目录下没有文件")
        return

    # 询问用户是否需要修改前缀
    current_prefix = input("请输入当前文件的前缀（如果不需要修改前缀，直接按回车）：").strip()
    
    if current_prefix:
        # 修改前缀的情况
        new_prefix = input("请输入新的前缀（直接按回车则删除旧前缀）：").strip()
            
        for file in files:
            if file.startswith(current_prefix):
                new_name = file.replace(current_prefix, new_prefix, 1)
                old_path = os.path.join(directory_path, file)
                new_path = os.path.join(directory_path, new_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"已重命名: {file} -> {new_name}")
                except Exception as e:
                    print(f"重命名 {file} 时出错: {str(e)}")
    else:
        # 询问是否需要新增前缀
        add_prefix = input("是否需要为文件添加新前缀？(y/n): ").strip().lower()
        if add_prefix == 'y':
            new_prefix = input("请输入要添加的前缀：").strip()
            if not new_prefix:
                print("错误：新前缀不能为空")
                return
                
            for file in files:
                new_name = new_prefix + file
                old_path = os.path.join(directory_path, file)
                new_path = os.path.join(directory_path, new_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"已重命名: {file} -> {new_name}")
                except Exception as e:
                    print(f"重命名 {file} 时出错: {str(e)}")
        else:
            print("操作已取消")

def main():
    print("欢迎使用文件重命名程序！")
    directory_path = input("请输入要处理的目录路径：").strip()
    rename_files_with_prefix(directory_path)

if __name__ == "__main__":
    main() 