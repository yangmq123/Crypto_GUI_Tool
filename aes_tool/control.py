from tkinter import messagebox

import crypto
from ui import Win
import os

class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: Win

    def __init__(self):
        pass

    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        self.check_file()
        self.getlastkey()
    def _get_input(self):
        """读取上方输入框文本。"""
        return self.ui.tk_text_mv84fk4d.get("1.0", "end-1c")

    def _set_output(self, text):
        """将文本写入下方结果框。"""
        self.ui.tk_text_mv849eat.delete("1.0", "end")
        self.ui.tk_text_mv849eat.insert("1.0", text)

    def _get_key(self):
        """读取密钥框内容并校验为 32 字节（AES-256）。"""
        key = self.ui.tk_text_mv86hf87.get("1.0", "end-1c").strip()
        if len(key.encode("utf-8")) != crypto.KEY_BYTES:
            raise ValueError("密钥必须为32字节(256位)，请点击“随机密钥”生成")
        return key

    def start_en(self, evt):
        """加密：读取上方文本，用密钥框中的密钥加密，结果(Base64)写入下方结果框。"""
        try:
            
            key = self._get_key()
            with open("./aes.ini","w") as file:
                file.write(f"aes_key={key}")
            file.close()
            plaintext = self._get_input()
            if not plaintext:
                messagebox.showwarning("提示", "请输入要加密的文本")
                return
            result = crypto.encrypt(plaintext, key)
            self._set_output(result)
        except Exception as e:
            messagebox.showerror("加密失败", str(e))

    def start_de(self, evt):
        """解密：读取上方Base64密文，用密钥框中的密钥解密，结果(文本)写入下方结果框。"""
        try:
            key = self._get_key()
            ciphertext = self._get_input().strip()
            key = self._get_key()
            with open("./aes.ini","w") as file:
                file.write(f"aes_key={key}")
            file.close()
            if not ciphertext:
                messagebox.showwarning("提示", "请输入要解密的Base64密文")
                return
            result = crypto.decrypt(ciphertext, key)
            self._set_output(result)
        except ValueError as e:
            msg = str(e)
            if "MAC" in msg:
                msg = "解密失败：密钥错误或密文已损坏"
            messagebox.showerror("解密失败", msg)
        except Exception as e:
            messagebox.showerror("解密失败", str(e))

    def random_key(self, evt):
        """随机生成 AES-256 密钥并填入密钥框。"""
        key = crypto.generate_key()
        self.ui.tk_text_mv86hf87.delete("1.0", "end")
        self.ui.tk_text_mv86hf87.insert("1.0", key)
    def getlastkey(self):
        with open("./aes.ini","r") as file:
            res = file.read().replace("aes_key=","")
        file.close()  
        self.ui.tk_text_mv86hf87.delete("1.0", "end")
        self.ui.tk_text_mv86hf87.insert("1.0", res)
    def check_file(self):
        if not(os.path.isfile("./aes.ini")):
            with open("./aes.ini","w") as file:
                file.write(f"aes_key=")



