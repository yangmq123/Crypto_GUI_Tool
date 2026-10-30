from tkinter import filedialog, messagebox
import tkinter as tk
import crypto
from ui import Win



class Controller:
    ui: Win

    def __init__(self):
        self.public_key_path = ""
        self.private_key_path = ""

    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui

    def _get_input(self):
        """读取上方输入框文本。"""
        return self.ui.tk_text_mv84fk4d.get("1.0", "end-1c")

    def _set_output(self, text):
        """将文本写入下方结果框。"""
        self.ui.tk_text_mv849eat.delete("1.0", "end")
        self.ui.tk_text_mv849eat.insert("1.0", text)

    def _refresh_labels(self):
        """更新公钥/私钥文件位置标签。"""
        self.ui.tk_label_mv84a2au.config(
            text="公钥文件位置\n" + (self.public_key_path or "未选择"))
        self.ui.tk_label_mv84a9c5.config(
            text="私钥文件位置\n" + (self.private_key_path or "未选择"))

    def _show_randomart_dialog(self, art_text):
        """
        弹出一个带等宽字体的 Toplevel 窗口，用于展示公钥图样。
        点击“确定”后关闭。
        """
        # 1. 创建 Toplevel 弹窗，依附于主窗口
        dialog = tk.Toplevel(self.ui)
        dialog.title("警告")
        dialog.resizable(False, False)

        # 居中显示在主窗口上方
        self.ui.update_idletasks()
        x = self.ui.winfo_x() + (self.ui.winfo_width() // 2) - 150
        y = self.ui.winfo_y() + (self.ui.winfo_height() // 2) - 200
        dialog.geometry(f"+{x}+{y}")

        # 2. 图标和说明文字

        tk.Label(dialog, text="当前公钥文件图样如下：", justify="center").pack(padx=20, pady=5)

        # 3. 关键：等宽字体显示图样
        # 使用 Text 控件，去除边框，看起来像普通文本，且设置只读
        art_text_widget = tk.Text(dialog, font=("Consolas", 11), bg=dialog.cget('bg'),
                                  bd=0, highlightthickness=0, wrap="none", height=12, width=25)
        art_text_widget.insert("1.0", art_text)
        art_text_widget.config(state="disabled")  # 只读
        art_text_widget.pack(padx=20, pady=10)

        # 4. 确定按钮
        tk.Button(dialog, text="确定", width=10, command=dialog.destroy).pack(pady=(5, 15))

        # 5. 窗口居中、模态设置与聚焦
        dialog.transient(self.ui)  # 让弹窗始终浮在主窗口上方
        dialog.grab_set()  # 拦截所有发往主窗口的事件（模态）
        dialog.focus_set()  # 弹窗获取焦点

        # 6. 阻塞等待用户点击“确定”或关闭窗口
        self.ui.wait_window(dialog)

    def start_en(self, evt):
        """加密：读取上方文本，用公钥加密，结果(Base64)写入下方结果框。"""
        try:
            if not self.public_key_path:
                messagebox.showwarning("提示", "请先选择或生成公钥文件")
                return
            plaintext = self._get_input()
            if not plaintext:
                messagebox.showwarning("提示", "请输入要加密的文本")
                return
            with open(self.public_key_path, "rb") as f:
                public_key = f.read()

            result = crypto.encrypt(plaintext, public_key)
            self._set_output(result)
        except Exception as e:
            messagebox.showerror("加密失败", str(e))

    def start_de(self, evt):
        """解密：读取上方Base64密文，用私钥解密，结果(文本)写入下方结果框。"""
        try:
            if not self.private_key_path:
                messagebox.showwarning("提示", "请先选择或生成私钥文件")
                return
            ciphertext = self._get_input().strip()
            if not ciphertext:
                messagebox.showwarning("提示", "请输入要解密的Base64密文")
                return
            with open(self.private_key_path, "rb") as f:
                private_key = f.read()
            result = crypto.decrypt(ciphertext, private_key)
            self._set_output(result)
        except Exception as e:
            messagebox.showerror("解密失败", str(e))

    def get_file1_path(self, evt):
        """选择公钥文件。"""
        path = filedialog.askopenfilename(
            title="选择公钥文件",
            filetypes=[("PEM 文件", "*.pem"), ("所有文件", "*.*")],
        )
        if path:
            self.public_key_path = path
            self._refresh_labels()
            try:
                with open(path, "rb") as f:
                    public_key = f.read()
                    # 假设 crypto.verify_public_key 返回的是随机图样字符串
                    art = crypto.verify_public_key(public_key)

                    # 调用自定义的图样弹窗，阻塞直到用户点击“确定”
                    self._show_randomart_dialog(art)
            except Exception as e:
                messagebox.showerror("错误", f"无法读取公钥或生成图样：\n{str(e)}")
                # 可选：如果出错，是否要回退路径
                # self.public_key_path = ""
                # self._refresh_labels()

    def get_file2_path(self, evt):
        """选择私钥文件。"""
        path = filedialog.askopenfilename(
            title="选择私钥文件",
            filetypes=[("PEM 文件", "*.pem"), ("所有文件", "*.*")],
        )
        if path:
            self.private_key_path = path
            self._refresh_labels()

    def gen_keys(self, evt):
        """生成密钥对并保存为 PEM 文件。"""
        try:
            public_path = filedialog.asksaveasfilename(
                title="保存公钥",
                initialfile="public_key.pem",
                defaultextension=".pem",
                filetypes=[("PEM 文件", "*.pem"), ("所有文件", "*.*")],
            )
            if not public_path:
                return
            private_path = filedialog.asksaveasfilename(
                title="保存私钥",
                initialfile="private_key.pem",
                defaultextension=".pem",
                filetypes=[("PEM 文件", "*.pem"), ("所有文件", "*.*")],
            )
            if not private_path:
                return

            public_pem, private_pem = crypto.generate_key_pair()
            with open(public_path, "wb") as f:
                f.write(public_pem)
            with open(private_path, "wb") as f:
                f.write(private_pem)

            self.public_key_path = public_path
            self.private_key_path = private_path
            self._refresh_labels()
            messagebox.showinfo("成功", "密钥对生成成功")
        except Exception as e:
            messagebox.showerror("生成密钥失败", str(e))