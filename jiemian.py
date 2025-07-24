import os
import zipfile
import shutil
from tqdm import tqdm
import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class ZipSplitMergeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZIP 文件拆分与合并工具")
        self.root.geometry("600x400")
        
        self.create_widgets()
    
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="ZIP 文件拆分与合并工具", font=('Arial', 14))
        title_label.pack(pady=10)
        
        # 创建选项卡
        tab_control = ttk.Notebook(main_frame)
        
        # 拆分按大小选项卡
        tab_size = ttk.Frame(tab_control)
        self.create_split_by_size_tab(tab_size)
        
        # 拆分按数量选项卡
        tab_parts = ttk.Frame(tab_control)
        self.create_split_by_parts_tab(tab_parts)
        
        # 合并选项卡
        tab_merge = ttk.Frame(tab_control)
        self.create_merge_tab(tab_merge)
        
        tab_control.add(tab_size, text='按大小拆分')
        tab_control.add(tab_parts, text='按数量拆分')
        tab_control.add(tab_merge, text='合并文件')
        tab_control.pack(expand=1, fill="both")
    
    def create_split_by_size_tab(self, parent):
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入文件
        ttk.Label(frame, text="输入 ZIP 文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_file_size = tk.StringVar()
        ttk.Entry(frame, textvariable=self.input_file_size, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="浏览...", command=lambda: self.browse_file(self.input_file_size)).grid(row=0, column=2)
        
        # 输出前缀
        ttk.Label(frame, text="输出文件前缀:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_prefix_size = tk.StringVar()
        ttk.Entry(frame, textvariable=self.output_prefix_size, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="浏览...", command=lambda: self.browse_output(self.output_prefix_size)).grid(row=1, column=2)
        
        # 部分大小
        ttk.Label(frame, text="每个部分大小(MB):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.part_size = tk.StringVar(value="100")
        ttk.Entry(frame, textvariable=self.part_size, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # 进度条
        self.progress_size = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_size.grid(row=3, column=0, columnspan=3, pady=10)
        
        # 执行按钮
        ttk.Button(frame, text="开始拆分", command=self.split_by_size).grid(row=4, column=1, pady=10)
    
    def create_split_by_parts_tab(self, parent):
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入文件
        ttk.Label(frame, text="输入 ZIP 文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_file_parts = tk.StringVar()
        ttk.Entry(frame, textvariable=self.input_file_parts, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="浏览...", command=lambda: self.browse_file(self.input_file_parts)).grid(row=0, column=2)
        
        # 输出前缀
        ttk.Label(frame, text="输出文件前缀:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_prefix_parts = tk.StringVar()
        ttk.Entry(frame, textvariable=self.output_prefix_parts, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="浏览...", command=lambda: self.browse_output(self.output_prefix_parts)).grid(row=1, column=2)
        
        # 部分数量
        ttk.Label(frame, text="要拆分的部分数量:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.num_parts = tk.StringVar(value="5")
        ttk.Entry(frame, textvariable=self.num_parts, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # 进度条
        self.progress_parts = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_parts.grid(row=3, column=0, columnspan=3, pady=10)
        
        # 执行按钮
        ttk.Button(frame, text="开始拆分", command=self.split_by_parts).grid(row=4, column=1, pady=10)
    
    def create_merge_tab(self, parent):
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入前缀
        ttk.Label(frame, text="输入部分文件前缀:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_prefix_merge = tk.StringVar()
        ttk.Entry(frame, textvariable=self.input_prefix_merge, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="浏览...", command=lambda: self.browse_file(self.input_prefix_merge)).grid(row=0, column=2)
        
        # 输出文件
        ttk.Label(frame, text="输出 ZIP 文件:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_file_merge = tk.StringVar()
        ttk.Entry(frame, textvariable=self.output_file_merge, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="浏览...", command=lambda: self.browse_output(self.output_file_merge, is_file=True)).grid(row=1, column=2)
        
        # 进度条
        self.progress_merge = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_merge.grid(row=2, column=0, columnspan=3, pady=10)
        
        # 执行按钮
        ttk.Button(frame, text="开始合并", command=self.merge_zips).grid(row=3, column=1, pady=10)
    
    def browse_file(self, target_var):
        filename = filedialog.askopenfilename(filetypes=[("ZIP 文件", "*.zip")])
        if filename:
            target_var.set(filename)
    
    def browse_output(self, target_var, is_file=False):
        if is_file:
            filename = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP 文件", "*.zip")])
            if filename:
                target_var.set(filename)
        else:
            directory = filedialog.askdirectory()
            if directory:
                target_var.set(directory)
    
    def split_by_size(self):
        input_zip = self.input_file_size.get()
        output_prefix = self.output_prefix_parts.get()
        part_size_mb = float(self.part_size.get())
        
        if not input_zip or not output_prefix:
            messagebox.showerror("错误", "请输入所有必要信息！")
            return
        
        try:
            part_size = part_size_mb * 1024 * 1024  # 转换为字节
            file_size = os.path.getsize(input_zip)
            num_parts = math.ceil(file_size / part_size)
            
            self.progress_size["maximum"] = file_size
            self.progress_size["value"] = 0
            
            with open(input_zip, 'rb') as f:
                for i in range(num_parts):
                    part_num = i + 1
                    part_name = f"{output_prefix}.part{part_num:03d}.zip"
                    
                    with open(part_name, 'wb') as part_file:
                        bytes_written = 0
                        while bytes_written < part_size:
                            chunk = min(1024 * 1024, part_size - bytes_written)
                            data = f.read(chunk)
                            if not data:
                                break
                            part_file.write(data)
                            bytes_written += len(data)
                            self.progress_size["value"] += len(data)
                            self.root.update()
            
            messagebox.showinfo("完成", f"拆分完成！共生成 {num_parts} 个部分，每个约 {part_size_mb}MB")
            self.progress_size["value"] = 0
        
        except Exception as e:
            messagebox.showerror("错误", f"拆分过程中出错: {str(e)}")
    
    def split_by_parts(self):
        input_zip = self.input_file_parts.get()
        output_prefix = self.output_prefix_parts.get()
        num_parts = int(self.num_parts.get())
        
        if not input_zip or not output_prefix:
            messagebox.showerror("错误", "请输入所有必要信息！")
            return
        
        try:
            file_size = os.path.getsize(input_zip)
            part_size = math.ceil(file_size / num_parts)
            
            self.progress_parts["maximum"] = file_size
            self.progress_parts["value"] = 0
            
            with open(input_zip, 'rb') as f:
                for i in range(num_parts):
                    part_num = i + 1
                    part_name = f"{output_prefix}.part{part_num:03d}.zip"
                    
                    with open(part_name, 'wb') as part_file:
                        bytes_written = 0
                        while bytes_written < part_size:
                            chunk = min(1024 * 1024, part_size - bytes_written)
                            data = f.read(chunk)
                            if not data:
                                break
                            part_file.write(data)
                            bytes_written += len(data)
                            self.progress_parts["value"] += len(data)
                            self.root.update()
            
            messagebox.showinfo("完成", f"拆分完成！共生成 {num_parts} 个部分")
            self.progress_parts["value"] = 0
        
        except Exception as e:
            messagebox.showerror("错误", f"拆分过程中出错: {str(e)}")
    
    def merge_zips(self):
        input_prefix = self.input_prefix_merge.get()
        output_zip = self.output_file_merge.get()
        
        if not input_prefix or not output_zip:
            messagebox.showerror("错误", "请输入所有必要信息！")
            return
        
        try:
            # 找到所有部分文件
            parts = []
            dir_name = os.path.dirname(input_prefix) or '.'
            base_name = os.path.basename(input_prefix)
            
            for f in os.listdir(dir_name):
                if f.startswith(base_name) and f.endswith('.zip'):
                    parts.append(os.path.join(dir_name, f))
            
            if not parts:
                messagebox.showerror("错误", "未找到匹配的部分文件！")
                return
            
            parts.sort()
            total_size = sum(os.path.getsize(p) for p in parts)
            
            self.progress_merge["maximum"] = total_size
            self.progress_merge["value"] = 0
            
            with open(output_zip, 'wb') as out_file:
                for part in parts:
                    with open(part, 'rb') as in_file:
                        while True:
                            data = in_file.read(1024 * 1024)
                            if not data:
                                break
                            out_file.write(data)
                            self.progress_merge["value"] += len(data)
                            self.root.update()
            
            messagebox.showinfo("完成", f"合并完成！输出文件: {output_zip}")
            self.progress_merge["value"] = 0
        
        except Exception as e:
            messagebox.showerror("错误", f"合并过程中出错: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(r"D:\FFOutput\高木.ico")  # 或者使用完整路径
    app = ZipSplitMergeApp(root)
    root.mainloop()