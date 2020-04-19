from commitUi import CommitUi
from sendfolder import SendFolder
import socket
import struct
import json
from tkinter import messagebox
import re
import os
from tkinter import filedialog
from threading import  Thread
import time

class CommitApp(CommitUi, SendFolder):
    def __init__(self):
        CommitUi.__init__(self)
        SendFolder.__init__(self)
        self.skt = None
        self.dir_name = "H:/Users/Desktop/"

    def commit(self):
        self.skt = socket.socket()
        address = self.ent1.get()
        id = self.ent2.get()
        machine_number = self.ent3.get()
        patten = re.compile('[0-5]?[0-9]$')
        ippatten = re.compile(r'^192\.168\.\d{1,3}\.\d{1,3}$')

        if not patten.match(machine_number):
            messagebox.showerror('错误提示', '输入正确的机器号01-50  ！')
            return

        if not ippatten.match(address):
            messagebox.showerror('错误提示', '请输入正确的ip地址！')
            return

        dirname = (self.dir_name+id).strip('\u202a')
        if not os.path.exists(dirname):
            messagebox.showerror('错误提示', '没有考生文件夹！')
            return

        port = 8888
        try:
            self.connect(address, port)
            head_info = [id, machine_number]
            head_info_byte = json.dumps(head_info)
            head_len = len(head_info_byte)
            len_bytes = struct.pack('q', head_len)
            self.skt.send(len_bytes)
            self.skt.send(head_info_byte.encode())
            thread = Thread(target=self.send_all, args=[dirname])
            thread.start()
        except TimeoutError:
            messagebox.showerror('错误提示', '连接超时')
        except ConnectionRefusedError:
            messagebox.showerror('错误提示', '无法连接交卷主机')

    def change_dir(self):
        self.dir_name = filedialog.askdirectory()+'/'

    @staticmethod
    def show_has_exist():
        messagebox.showinfo("提示", "服务器已经存在同名文件夹")
    
    def show_progress(self):
        pct = self.has_send/self.totsize
        self.precesbar['text']=('\r|'+int(pct*30)*'▇' + f'{pct:.0%}')
        if pct == 1.:
            time.sleep(0.1)
            self.precesbar['text']= '传输完成!'


if __name__ == '__main__':
    app = CommitApp()
    app.mainloop()
