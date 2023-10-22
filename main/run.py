# -*- coding:utf-8 -*-
from tkinter import *
from tkinter import ttk
import add_face
import db
import detect
import re
import os
import sqlite3
from datetime import *


class APP:
    def __init__(self):

        self.root = Tk()
        self.root.title('FACE')
        self.root.geometry('%dx%d' % (550, 450))

        # 数据库实例创建
        self.mydb = db.record()

        self.createFirstPage()

        # 新录入的人的姓名
        self.name = StringVar()
        self.name1 = StringVar()


        mainloop()

    def createFirstPage(self):
        self.page1 = Frame(self.root)
        self.page1.grid()
        Label(self.page1, height=4, text='人脸识别系统', font=('microsoft yahei', 26)).grid(columnspan=2)
        #self.usernames 是 用户名字组成的列表
        self.usernames = []
        self.usernames = self.mydb.query_name()


        self.button11 = Button(self.page1, width=18, height=2, text="签到打卡", bg='white', font=("microsoft yahei", 14),
                               relief='raise', command = lambda :detect.check( self.usernames))
        self.button11.grid(row=1, column=0, padx=25, pady=10)
        self.button12 = Button(self.page1, width=18, height=2, text="录入新的人脸", bg='white', font=("microsoft yahei", 14),
                               relief='raise', command = self.createSecondPage)
        self.button12.grid(row=1, column=1, padx=25, pady=10)
        self.button13 = Button(self.page1, width=18, height=2, text="查询签到信息", bg='white', font=("microsoft yahei", 14),
                               relief='raise',command = self.checkDataView)
        self.button13.grid( row=2, column=0,padx=25, pady=10)
        self.button14 = Button(self.page1, width=18, height=2, text="退出系统", bg='gray', font=("microsoft yahei", 14),
                               relief='raise',command = self.quitMain)
        self.button14.grid(row=2, column=1,padx=25, pady=10)

    def createSecondPage(self):
        # self.camera = cv2.VideoCapture(0)
        self.page1.grid_forget()
        self.page2 = Frame(self.root)
        self.page2.pack()
        Label(self.page2, text='欢迎使用人脸识别系统', font=('粗体', 20)).pack()

        # 输入姓名的文本框
        font1 = ('宋',18)
        # self.name = StringVar()
        self.text = Entry(self.page2, textvariable=self.name, width=20, font=font1).pack(side=TOP, padx=0, pady=10)
        self.name.set('请输入英文姓名')

        self.text1 = Entry(self.page2, textvariable=self.name1, width=20, font=font1).pack(side=TOP, padx=0, pady=10)
        self.name1.set('请输入中文姓名')

        # 确认名字的按钮
        self.button21 = Button(self.page2, text='英文名确认', width=13,bg='white', font=("宋", 12),relief='raise', command=lambda :add_face.add_face( self.name,self.usernames))
        self.button21.pack(side=LEFT, padx=5, pady=10)

        # 确认名字的按钮
        self.button21 = Button(self.page2, text='中文名确认',width=13, bg='white', font=("宋", 12),relief='raise', command=self.modifyname)
        self.button21.pack(side=LEFT, padx=10, pady=10)

        # 返回按钮
        self.button22 = Button(self.page2, text="返回", width=13,bg='white', font=("宋", 12),relief='raise',command = self.backFirst)
        self.button22.pack(side=LEFT, padx=15, pady=10)

    def checkDataView(self):
        self.page3 = Frame(self.root)
        self.page1.grid_forget()
        self.root.geometry('700x360')
        self.page3.pack()
        Label(self.page3, text='今日签到信息', bg='white', fg='red', font=('宋体', 25)).pack(side=TOP, fill='x')
        # 签到信息查看视图
        self.checkDate = ttk.Treeview(self.page3, show='headings', column=('sid', 'name', 'check_time'))
        self.checkDate.column('sid', width=100, anchor="center")
        self.checkDate.column('name', width=200, anchor="center")
        self.checkDate.column('check_time', width=300, anchor="center")

        self.checkDate.heading('sid', text='签到序号')
        self.checkDate.heading('name', text='名字')
        self.checkDate.heading('check_time', text='签到时间')

        # 插入数据
        self.records = self.mydb.query_record()
        for i in self.records:
            self.checkDate.insert('', 'end', values=i)

        # y滚动条
        yscrollbar = Scrollbar(self.page3, orient=VERTICAL, command=self.checkDate.yview)
        self.checkDate.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.pack(side=RIGHT, fill=Y)

        self.checkDate.pack(expand=1, fill=BOTH)

        # 返回按钮
        Button(self.page3, width=20, height=2, text="返回", bg='gray', font=("宋", 12),
                               relief='raise',command =self.backMain).pack(padx = 20, pady = 20)

    def backFirst(self):
        self.page2.pack_forget()
        self.root.geometry('550x450')
        self.page1.grid()

    def backMain(self):
        self.root.geometry('550x450')
        self.page3.pack_forget()
        self.page1.grid()

    def quitMain(self):
        sys.exit(0)

    def b(self):
        a=self.name1.get()
        print(a) 

    def modifyname(self):
        a=self.name.get()
        b=self.name1.get()
        path = "FaceData" #输入你要更改文件的目录


        originalname = a #123是要查找文件名里包含123的文件
        replacename = b #321是要被替换的字符串，如果就是删除originalname，那么replacename = ''就可以
        def main1(path1):
            files = os.listdir(path1)  # 得到文件夹下的所有文件名称
            for file in files: #遍历文件夹
                if os.path.isdir(path1 + '/' + file):
                    main1(path1 + '\\' + file)
                else:
                    files2 = os.listdir(path1 + '\\')
                    for file1 in files2:
                        if originalname in file1:
                            #用‘’替换掉 X变量
                            n = str(path1 + '\\' + file1.replace(originalname,replacename))
                            n1 = str(path1 + '\\' + str(file1))
                            try:
                                os.rename(n1, n)
                            except IOError:
                                continue
        main1(path)


        self.conn = sqlite3.connect("recordinfo.db", check_same_thread=False)
        # 创建游标
        self.cursor = self.conn.cursor()


        # 修改数据
        # self.conn.execute("update name_table set name='c' where id = 10")
        self.conn.execute("update name_table set name = '%s' where name = '%s'"%(b,a))
        self.conn.commit()

        self.cursor.close()
        self.conn.close()



if __name__ == '__main__':
    demo = APP()