import os
from time import sleep
from tkinter import *

# http://www.runoob.com/python3/python3-os-file-methods.html
# 一个生成GUI应用的自定义类


class DirList(object):
    # 构造函数
    def __init__(self, initdir=None, lines=None, words=None, chars=None):
        self.top = Tk()  # 顶层窗口
        self.top.title('wc')
        self.label = Label(self.top, text='wordcount')  # 第一个标签控件
        self.label.pack()

        '''
        StringVar，并不是Python内置的数据类型，而是tkinter模块内的对象。
        我们在使用GUI界面编程时，有时候需要跟踪变量的值的变化，以保证值的变化随时可以显示在界面上。而Python无法做到这一点。这里采用了Tcl工具中对象。
        StringVar 、BooleanVar、DoubleVar、IntVar都属于这类情况
        StringVar()保存了一个string类型变量，默认值是''
        get()方法可以得到保存的值
        set()方法设置/更改保存的值
        Variable类，有些控件如Entry（本例中出现）、Radiobutton，可以通过传入特定参数直接和一个程序变量绑定，这些参数包括：variable、textvariable、
        onvalue、offvalue、value
        这种绑定是双向的：如果该变量发生改变，于该变量绑定的控件也会随之更新。
        '''
        self.cwd = StringVar(self.top)
        # 第二个标签控件。用于动态展示一些文本信息
        self.dirl = Label(self.top, fg='blue', font=('Helvetica', 12, 'bold'))
        self.dirl.pack()

        self.dirfm = Frame(self.top)  # 第一个Frame控件，一个包含其他控件的纯容器
        self.dirsb = Scrollbar(self.dirfm)  # 主要是提供滚动功能
        self.dirsb.pack(side=RIGHT, fill=Y)  # 滚动条靠右填充整个剩余空间
        '''
        一个选项列表，指定列表yscrollbar的回调函数为滚动条的set，同时滚动条的command回调的是列表的yview
        可以这么理解二者的关系：当Listbox改变时（比如使用向上、向下方向键改变列表内容时），滚动条调用set方法改变滑块的位置；
        当滚动条的滑块位置发生变化时，列表将调用yview以展示新的项。
        同学们可以将绑定取消，自行观察现象。
        '''
        self.dirs = Listbox(self.dirfm, height=15, width=50,
                            yscrollcommand=self.dirsb.set)
        # 绑定操作。这意味着将一个回调函数与按键、鼠标操作或者其他的一些事件连接起来。这里当双击任意条目时，会调用setDirAndGo函数
        self.dirs.bind('<Double-1>', self.setDirAndGo)
        # 这里同列表控件的yscrollcommand回调结合起来
        self.dirsb.config(command=self.dirs.yview)
        self.dirs.pack(side=LEFT, fill=BOTH)
        self.dirfm.pack()

        # 单行文本框。指定了宽度；同时设置了一个可变类型参数textvariable的值
        self.dirn = Entry(self.top, width=50, textvariable=self.cwd)
        self.dirn.bind('<Return>', self.doLS)  # 绑定操作。这里当敲击回车键时，调用函数doLS
        self.dirn.pack()

        self.bfm = Frame(self.top)  # 第二个Frame控件
        # 定义了三个按钮，每个按钮分别回调不同的函数，并设置了激活前景色、激活后景色
        self.ls = Button(self.bfm, text='选择文件', command=self.doLS,
                         activeforeground='white', activebackground='green')

        self.ls.pack(side=LEFT)
        self.bfm.pack()

        self.a = StringVar(self.top)
        self.line = Label(self.top, fg='blue', font=(
            'Helvetica', 12, 'bold'), textvariable=self.a)  # StringVar不绑定一个variable不能显示，坑
        self.line.pack()
        self.b = StringVar(self.top)
        self.char = Label(self.top, fg='blue', font=(
            'Helvetica', 12, 'bold'), textvariable=self.b)
        self.char.pack()
        self.c = StringVar(self.top)
        self.word = Label(self.top, fg='blue', font=(
            'Helvetica', 12, 'bold'), textvariable=self.c)
        self.word.pack()

        # 构造函数最后一部分，用于初始化GUI程序，以当前工作目录作为起始点。
        if initdir:
            self.cwd.set(os.curdir)
            self.a.set('行数：%s' % lines)
            self.b.set('字符数：%s' % chars)
            self.c.set('词数：%s' % words)
            self.doLS()

    # 设置要遍历的目录；最后又调用doLS函数
    def setDirAndGo(self, ev=None):
        self.last = self.cwd.get()
        self.dirs.config(selectbackground='red')
        # curselection()获取所选中的对象
        check = self.dirs.get(self.dirs.curselection())
        if not check:
            check = os.curdir
        self.cwd.set(check)
        self.doLS()

    # 实现遍历目录的功能，这也是整个GUI程序最关键的部分。
    def doLS(self, ev=None):
        error = ''
        tdir = self.cwd.get()
        # 进行一些安全检查
        if not tdir:
            tdir = os.curdir
        if not os.path.exists(tdir):
            error = tdir + ': 没有这个文件'

        # 如果发生错误，之前的目录就会重设为当前目录
        if error:
            self.cwd.set(error)
            self.top.update()
            sleep(2)
            # hasattr(object, name)如果对象有该属性返回 True，否则返回 False。
            if not (hasattr(self, 'last') and self.last):
                self.last = os.curdir
            self.cwd.set(self.last)
            self.dirs.config(selectbackground='LightSkyBlue')
            self.top.update()
            return

        if os.path.isfile(tdir):
            self.get_count(tdir)
        else:
            # 如果一切正常
            self.cwd.set('正在获取目标文件夹内容……')
            self.top.update()
            if os.path.isdir(tdir):
                dirlist = os.listdir(tdir)  # 获取实际文件列表
                dirlist.sort()
                os.chdir(tdir)  # 改变当前工作目录

            self.dirl.config(text=os.getcwd())  # getcwd()返回当前工作目录
            self.dirs.delete(0, END)
            self.dirs.insert(END, os.curdir)
            self.dirs.insert(END, os.pardir)  # os.pardir上级目录
            try:
                for eachFile in dirlist:  # 替换Listbox中的内容
                    self.dirs.insert(END, eachFile)
            except:
                pass
            self.cwd.set(os.curdir)
            self.dirs.config(selectbackground='LightSkyBlue')

    def get_count(self, fn):
        with open(fn, errors='ignore') as fd:
            data = fd.read()
        chars = len(data)
        words = len(data.split())
        lines = data.count('\n') + 1  # 统计的是换行符的数量，所以要加1
        self.a.set('行数：%s' % lines)
        self.b.set('字符数：%s' % chars)
        self.c.set('词数：%s' % words)
        self.top.update()

# 主函数，应用程序入口。main函数会创建一个GUI应用，，然后调用mainloop函数来启动GUI程序


def main():
    DirList(os.curdir, 0, 0, 0)
    # os.curdir 是当前目录地址
    mainloop()


if __name__ == '__main__':
    main()
