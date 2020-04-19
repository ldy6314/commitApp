from tkinter import *
from tkinter.ttk import *


class CommitUi:
    def __init__(self):
        self.win = Tk()
        self.win.title('信息学试卷提交')
        self.lb1 = Label(text='收卷主机号')
        self.lb2 = Label(text='准考证号')
        self.lb3 = Label(text='上机号')
        self.ent1 = Entry(width=25)
        self.ent2 = Entry(width=25)
        self.ent3 = Entry(width=25)
        self.precesbar = Label()
        self.btn = Button(text='提交', width=10, command=self.commit)
        self.bt2 = Button(text='退出', width=10, command=self.win.quit)
        self.lb1.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.ent1.grid(row=0, column=1)
        self.lb2.grid(row=1, column=0, padx=10, sticky=W)
        self.ent2.grid(row=1, column=1)
        self.bt3 = Button(text='...', command=self.change_dir, width=2)
        self.bt3.grid(row=1, column=2)
        self.lb3.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.ent3.grid(row=2, column=1)
        # self.lb4.grid(row=3,column=0, padx=10,  sticky=W)
        self.precesbar.grid(row=3, column=0,columnspan=3, sticky=W+E)
        self.btn.grid(row=4, column=1, padx=10, sticky=W)
        self.bt2.grid(row=4, column=1, sticky=E)

    def commit(self):
        pass

    def change_dir(self):
        pass

    def mainloop(self):
        self.win.mainloop()


if __name__ == '__main__':
    app = CommitUi()
    app.mainloop()
