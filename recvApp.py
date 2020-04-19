from recvserver import RecvServer
from recvUi import RecvUi
import socket
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
import os
import sqlite3 as sq3


class RecvApp(RecvUi, RecvServer):
    def __init__(self):
        RecvUi.__init__(self)
        RecvServer.__init__(self)
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.ip_ent['text'] = self.ip_address
        self.db_name = 'commit_info.db'
        try:
            conn = sq3.connect(self.db_name)
            cur = conn.cursor()
            cur.execute("""CREATE TABLE commit_info(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_number TEXT ,
            machine_number INTEGER,
            ip_address TEXT
            )
            """)
            conn.commit()
            conn.close()
        except sq3.OperationalError:
            self.load()
        
        self.sort_button.configure(command=self.sort_info)
        self.sever_start_button.configure(command=self.start_server)
        self.dump_button.configure(command=self.dump_info)
        self.dir_choose_button.configure(command=self.get_recvdir)
    
    def load(self):
        conn = sq3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute('SELECT machine_number, id_number, ip_address from commit_info')
        lists = cur.fetchall()
        for item in lists:
            self.tree.insert('', 'end', values=item)
                     
    def start_server(self):
        if not self.recvdir:
            messagebox.showerror('错误', '没有设置接收文件夹')
            return
        status_info = f"{self.recvdir} 正在接收中...{' '*5}"
        self.status.set(status_info)
        thread = Thread(target=RecvServer.sever_for_ever, args=[self, self.ip_address, 8888, self.recvdir ])
        thread.start()
        self.sever_start_button.configure(state='disable')
        self.dir_choose_button.configure(state='disable')

    def logout(self, machine_number, id, ip_address):
        self.tree.insert('', 'end', values=(machine_number, id, ip_address))
        conn = sq3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute('SELECT id_number from commit_info')
        res = cur.fetchall()
        if (id,) not in res:
            cur.execute('INSERT INTO commit_info(id_number, machine_number, ip_address) VALUES(?,?,?)',
                        (id, int(machine_number), ip_address))
        conn.commit()
        conn.close()

    def get_recvdir(self):
        res = filedialog.askdirectory()

        if res:
            self.recvdir = res
        else:
            messagebox.showerror('错误', '接收文件夹未设置')

    def open_recvdir(self):
        if self.recvdir:
            os.startfile(self.recvdir)

    def dump_info(self):
        conn = sq3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute('SELECT machine_number, id_number, ip_address from commit_info')
        lists = cur.fetchall()
        lists.sort(key=lambda item: item[0])
        lists = list(map(lambda x: str(x)[1:-1], lists))
        lists.insert(0, 'machine_number,id,ip_address')
        with open('提交信息.csv', 'w', encoding='utf-8') as fo:
            fo.writelines('\n'.join(lists))
        conn.close()
        messagebox.showinfo('提示', '交卷信息已经保存')

    def sort_info(self):
        values = []
        children = self.tree.get_children()
        for child in children:
            values.append(tuple(self.tree.item(child)['values']))
        values.sort(key=lambda x: x[0])
        for child in children:
            self.tree.delete(child)

        for val in values:
            self.tree.insert('', 'end', values=val)


if __name__ == '__main__':
    app = RecvApp()
    app.mainloop()
