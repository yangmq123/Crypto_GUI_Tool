
import random
from tkinter import *
from tkinter.ttk import *
class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_button_mv848z6f = self.__tk_button_mv848z6f(self)
        self.tk_button_mv8492b3 = self.__tk_button_mv8492b3(self)
        self.tk_text_mv849eat = self.__tk_text_mv849eat(self)
        self.tk_text_mv84fk4d = self.__tk_text_mv84fk4d(self)
        self.tk_text_mv86hf87 = self.__tk_text_mv86hf87(self)
        self.tk_button_mv86hwv6 = self.__tk_button_mv86hwv6(self)
    def __win(self):
        self.title("AES_GCM加解密")
        # 设置窗口大小、居中
        width = 527
        height = 632
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.resizable(width=False, height=False)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_button_mv848z6f(self,parent):
        btn = Button(parent, text="加密", takefocus=False,)
        btn.place(x=399, y=241, width=108, height=30)
        return btn
    def __tk_button_mv8492b3(self,parent):
        btn = Button(parent, text="解密", takefocus=False,)
        btn.place(x=399, y=347, width=108, height=30)
        return btn
    def __tk_text_mv849eat(self,parent):
        text = Text(parent)
        text.place(x=0, y=431, width=526, height=197)
        return text
    def __tk_text_mv84fk4d(self,parent):
        text = Text(parent)
        text.place(x=0, y=0, width=526, height=197)
        return text
    def __tk_text_mv86hf87(self,parent):
        text = Text(parent)
        text.place(x=35, y=228, width=150, height=100)
        return text
    def __tk_button_mv86hwv6(self,parent):
        btn = Button(parent, text="随机密钥", takefocus=False,)
        btn.place(x=55, y=340, width=108, height=30)
        return btn
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_button_mv848z6f.bind('<Button-1>',self.ctl.start_en)
        self.tk_button_mv8492b3.bind('<Button-1>',self.ctl.start_de)
        self.tk_button_mv86hwv6.bind('<Button-1>',self.ctl.random_key)
        pass
    def __style_config(self):
        pass
if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()