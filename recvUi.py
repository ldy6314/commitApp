from tkinter import *
from tkinter.ttk import *


class RecvUi(Tk):
    def __init__(self):
        super().__init__()
        style1 = Style()
        style1.configure("BW.Label",  anchor=E, background='#708090')
        self.top_label = Label(text='本机\n地址', font=('', 15))
        self.ip_ent = Label(text='192.168.0.1', font=('', 30))

        self.sort_button = Button(text='排序')
        self.dump_button = Button(text='导出')
        self.sever_start_button = Button(text='开始')
        self.dir_choose_button = Button(text='...', width=3)

        self.columns = ('上机号', '准考证号', 'IP地址')
        self.tree = Treeview(show='headings', height=15, columns=self.columns, selectmode=BROWSE)
        self.bar = Scrollbar()
        
        self.status = StringVar() 
        self.status_bar = Button(textvar=self.status, style='BW.Label', command=self.open_recvdir, cursor='hand2')
        self.set_ui()

    def set_ui(self):
        self.title('文件夹接收服务器')
        self.resizable(False, False)
        self.top_label.grid(row=0, rowspan=2, column=0, padx=20, pady=20, sticky=N+S)
        self.ip_ent.grid(row=0, rowspan=2, column=1, sticky=N+S+W+E)

        self.sort_button.grid(row=2, column=0, padx=20)
        self.dump_button.grid(row=2, column=1)
        self.sever_start_button.grid(row=2, column=2,sticky=W)
        self.dir_choose_button.grid(row=2, column=2, sticky=E, padx=20)

        for column in self.columns:
            self.tree.column(column, anchor='center')
            self.tree.heading(column, text=column)
        self.bar.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.bar.set)
        self.tree.grid(row=3, columnspan=3, padx=20, pady=10)
        self.bar.grid(row=3, columnspan=3, sticky=E+N+S, padx=20, pady=10)
        
        self.status.set('状态:  未接收   ')
        self.status_bar.grid(row=4, columnspan=3, sticky=W+E)


if __name__ == '__main__':
    app = RecvUi()
    app.mainloop()
