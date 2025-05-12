import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import pyperclip
import re
import traceback
import sys

# 尝试导入latex2mathml
try:
    from latex2mathml.converter import convert as latex2mathml_convert
except ImportError as e:
    # 创建一个简单的错误窗口
    def show_error():
        root = tk.Tk()
        root.title("错误")
        root.geometry("600x400")
        
        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="无法加载latex2mathml库，请确保它已正确安装").pack(pady=10)
        ttk.Label(frame, text=f"错误信息: {str(e)}").pack(pady=5)
        ttk.Label(frame, text="请运行以下命令安装:").pack(pady=5)
        ttk.Label(frame, text="pip install latex2mathml").pack(pady=5)
        
        btn = ttk.Button(frame, text="退出", command=root.destroy)
        btn.pack(pady=20)
        
        root.mainloop()
        sys.exit(1)
    
    show_error()

class LatexToMathTypeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("LaTeX to MathType Converter")
        self.root.geometry("800x600")
        
        # 配置主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # LaTeX输入区域
        ttk.Label(main_frame, text="LaTeX 输入:").pack(anchor=tk.W, pady=(5, 0))
        self.latex_input = scrolledtext.ScrolledText(main_frame, height=10, width=80, wrap=tk.WORD)
        self.latex_input.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # 转换按钮
        convert_button = ttk.Button(button_frame, text="转换", command=self.convert_latex)
        convert_button.pack(side=tk.LEFT, padx=5)
        
        # 复制按钮
        copy_button = ttk.Button(button_frame, text="复制结果", command=self.copy_result)
        copy_button.pack(side=tk.LEFT, padx=5)
        
        # 清除按钮
        clear_button = ttk.Button(button_frame, text="清除", command=self.clear_all)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 示例按钮
        example_button = ttk.Button(button_frame, text="插入示例", command=self.insert_example)
        example_button.pack(side=tk.LEFT, padx=5)
        
        # 显示错误按钮
        show_error_button = ttk.Button(button_frame, text="显示详细错误", command=self.show_error_dialog)
        show_error_button.pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        ttk.Label(main_frame, text="转换结果 (MathML格式):").pack(anchor=tk.W, pady=(5, 0))
        self.result_output = scrolledtext.ScrolledText(main_frame, height=10, width=80, wrap=tk.WORD)
        self.result_output.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.pack(anchor=tk.W, pady=5)
        
        # 保存最后的错误
        self.last_error = None
        
    def convert_latex(self):
        """将LaTeX公式转换为MathML格式 (MathType可用)"""
        try:
            latex_text = self.latex_input.get("1.0", tk.END).strip()
            
            if not latex_text:
                self.status_label.config(text="请输入LaTeX公式")
                return
            
            # 清除LaTeX环境标记
            latex_text = re.sub(r'\\begin\{equation\}|\\\(', '', latex_text)
            latex_text = re.sub(r'\\end\{equation\}|\\\)', '', latex_text)
            
            # 移除可能包含的$符号
            latex_text = latex_text.replace('$', '')
            latex_text = latex_text.strip()
            
            # 转换为MathML格式
            mathml = latex2mathml_convert(latex_text)
            
            # 显示结果
            self.result_output.delete("1.0", tk.END)
            self.result_output.insert("1.0", mathml)
            
            self.status_label.config(text="转换成功！复制结果后可直接粘贴到MathType中")
            self.last_error = None
        
        except Exception as e:
            self.last_error = traceback.format_exc()
            self.status_label.config(text=f"转换失败: {str(e)}")
    
    def copy_result(self):
        """复制结果到剪贴板"""
        result = self.result_output.get("1.0", tk.END).strip()
        
        if result:
            pyperclip.copy(result)
            self.status_label.config(text="已复制到剪贴板！现在可以在MathType中粘贴")
        else:
            self.status_label.config(text="没有可复制的内容")
    
    def clear_all(self):
        """清除输入和输出内容"""
        self.latex_input.delete("1.0", tk.END)
        self.result_output.delete("1.0", tk.END)
        self.status_label.config(text="")
        self.last_error = None
    
    def insert_example(self):
        """插入示例公式"""
        examples = [
            r"s_0 = \frac{(s_{-3} + s_{3}) + 2(s_{-2} + s_{2}) - (s_{-1} + s_{1}) - 4s_0}{16h^2}",
            r"\int_{a}^{b} f(x) dx",
            r"\sum_{i=1}^{n} x_i",
            r"\lim_{x \to \infty} f(x)"
        ]
        self.latex_input.delete("1.0", tk.END)
        self.latex_input.insert("1.0", examples[0])
    
    def show_error_dialog(self):
        """显示详细错误信息的对话框"""
        error_window = tk.Toplevel(self.root)
        error_window.title("详细错误信息")
        error_window.geometry("600x400")
        
        error_frame = ttk.Frame(error_window, padding="10")
        error_frame.pack(fill=tk.BOTH, expand=True)
        
        if self.last_error:
            ttk.Label(error_frame, text="发生了以下错误:").pack(anchor=tk.W, pady=5)
            
            error_text = scrolledtext.ScrolledText(error_frame, height=15, width=70)
            error_text.pack(fill=tk.BOTH, expand=True, pady=5)
            error_text.insert("1.0", self.last_error)
            error_text.config(state="disabled")
            
            copy_btn = ttk.Button(error_frame, text="复制错误信息", 
                                  command=lambda: pyperclip.copy(self.last_error))
            copy_btn.pack(pady=10)
        else:
            ttk.Label(error_frame, text="目前没有错误信息").pack(pady=20)
        
        close_btn = ttk.Button(error_frame, text="关闭", command=error_window.destroy)
        close_btn.pack(pady=10)
        
        # 系统信息
        ttk.Separator(error_frame, orient="horizontal").pack(fill=tk.X, pady=10)
        ttk.Label(error_frame, text="系统信息:").pack(anchor=tk.W)
        
        system_info = f"Python版本: {sys.version}\n"
        system_info += f"运行模式: {'打包EXE' if getattr(sys, 'frozen', False) else '脚本'}\n"
        
        ttk.Label(error_frame, text=system_info).pack(anchor=tk.W)

def main():
    try:
        root = tk.Tk()
        app = LatexToMathTypeConverter(root)
        root.mainloop()
    except Exception as e:
        # 如果整个应用程序崩溃，显示错误
        error_text = f"应用程序发生严重错误:\n{str(e)}\n\n"
        error_text += traceback.format_exc()
        
        error_root = tk.Tk()
        error_root.title("应用程序错误")
        error_root.geometry("600x400")
        
        frame = ttk.Frame(error_root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="应用程序发生严重错误，无法继续运行").pack(pady=10)
        
        error_box = scrolledtext.ScrolledText(frame, height=15, width=70)
        error_box.pack(fill=tk.BOTH, expand=True, pady=10)
        error_box.insert("1.0", error_text)
        
        ttk.Button(frame, text="退出", command=error_root.destroy).pack(pady=10)
        
        error_root.mainloop()

if __name__ == "__main__":
    main() 