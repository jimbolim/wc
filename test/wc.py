import os
import re
# https://www.cnblogs.com/captain_jack/archive/2011/01/11/1933366.html
from optparse import OptionParser
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
# StringVar不绑定一个variable不能显示，坑
        self.a = StringVar(self.top)
        self.line = Label(self.top, fg='blue', font=(
            'Helvetica', 12, 'bold'), textvariable=self.a)
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
        lines = data.count('\n')
        self.a.set('行数：%s' % lines)
        self.b.set('字符数：%s' % chars)
        self.c.set('词数：%s' % words)
        self.top.update()


# 使用命令行指令
# options，它是一个对象optpars.Values，保存有命令行参数值。 args，它是一个由 positional arguments 组成的列表。
# short option string: 第一个参数，表示option的缩写;long option string: 第二个参数，表示option的全拼
# 表示此option在经过optionparser解析后的options对象中成员的名字，默认使用long option string
# 使用-h可以查看帮助信息


def opt():
    parser = OptionParser()
    parser.add_option("-c", "--char",
                      dest="chars",
                      action="store_true",
                      default=False,
                      help="only count chars")
    parser.add_option("-w", "--word",
                      dest="words",
                      action="store_true",
                      default=False,
                      help="only count words")
    parser.add_option("-l", "--line",
                      dest="lines",
                      action="store_true",
                      default=False,
                      help="only count lines")
    parser.add_option("-s", "--skim",
                      dest="skim",
                      action="store_true",
                      default=False,
                      help="traverse folder")
    parser.add_option("-x", "--windows",
                      dest="windows",
                      action="store_true",
                      default=False,
                      help="open a window")
    parser.add_option("-a", "--detail",
                      dest="detail",
                      action="store_true",
                      default=False,
                      help="show detail informations,only c")
    options, args = parser.parse_args()
    return options, args


'''
isCmt
功能：判断一行字符串是否为注释
输入：
 line: 字符串行
 isInMultiCmt：前面一行是否在多行注释中
 qttnFlagList: 引号列表
输出：
 isCmt: 当前行是否为注释
 isInMultiCmt：当前行是否在多行注释中
'''


def isCmt(line, multiCmtFlagIdx):
    singleCmtFlag = '//'  # 单行注释符号
    startCmtFlag = "/*"
    endCmtFlag = "*/"
    isCmtRet = True
    # print 'line: ' + line.strip()
    if multiCmtFlagIdx == False:  # 不在多行注释中
        # 单行注释
        # re.match(pattern, string, flags=0),匹配开头,\s是任意空白字符
        if re.match(r'(\s)*' + singleCmtFlag, line):
            return isCmtRet, multiCmtFlagIdx
        # 多行注释开始符号
        if startCmtFlag in line:  # 找到多行注释开始符号
            if endCmtFlag in line:
                multiCmtFlagIdx = False
                return isCmtRet, multiCmtFlagIdx
            return isCmtRet, multiCmtFlagIdx
        else:
             # 没有找到多行注释开始符，继续查找下个类型的符号
            multiCmtFlagIdx = False
            isCmtRet = False
            return isCmtRet, multiCmtFlagIdx
    else:  # 在多行注释中
        # 多行注释开始符
        if endCmtFlag in line:
            multiCmtFlagIdx = False
    # print isCmtRet, multiCmtFlagIdx
    return isCmtRet, multiCmtFlagIdx  # 返回是否注释行，以及当前是否在多行注释中

# 计算文件的信息


def get_count(data):
    chars = len(data)
    words = len(data.split())
    lines = data.count('\n')
    return lines, words, chars

# 输出信息


def print_wc(options, lines, words, chars, fn):
    print('filename:'+fn)
    if options.lines:
        print('lines:%s' % lines)
    if options.words:
        print('words:%s' % words)
    if options.chars:
        print('chars:%s' % chars)


def get_detail_count(fn):
    datas = fn.readlines()
    codelines = 0
    nulllines = 0
    commentlines = 0
    lines = 0
    multiCmtFlagIdx = False
    for data in datas:
        # 判断代码行，空行,注释行
        # windows下的编辑器，在只要读到文本最后有'\n'的时候，都会另起一行，显示为空行。其实第二行根本就不存在。
        if len(data.strip()) < 3 and not multiCmtFlagIdx:
            nulllines += 1
        else:
            isCmtRet, multiCmtFlagIdx = isCmt(data, multiCmtFlagIdx)
            if isCmtRet or multiCmtFlagIdx:
                commentlines += 1
            else:
                codelines += 1
    print('commentlines:%s' % commentlines)
    print('nulllines:%s' % nulllines)
    print('codelines:%s' % codelines)

# 主函数


if __name__ == '__main__':
    options, args = opt()
    if options.windows:
        DirList(os.curdir, 0, 0, 0)
        # os.curdir 是当前目录地址
        mainloop()
    else:
        if not (options.lines or options.words or options.chars or options.detail):
            options.lines, options.words, options.chars, options.detail = True, True, True, True
        if args:
            for fn in args:
                if os.path.isfile(fn):
                    with open(fn, errors='ignore') as fd:
                        data = fd.read()
                    lines, words, chars = get_count(data)
                    print_wc(options, lines, words, chars, fn)
                    if options.detail:
                        fd = open(fn, errors='ignore')
                        get_detail_count(fd)
                # 判断是否文件夹
                elif os.path.isdir(fn):
                    if options.skim:
                        fns = os.listdir(fn)
                        fns.sort()
                        for fd in fns:
                            print(fd)
                            if os.path.isfile(fd):
                                with open(fd, errors='ignore') as folder:
                                    data = folder.read()
                                    lines, words, chars = get_count(data)
                                    print_wc(options, lines, words, chars, fn)
                                folder = open(fd, errors='ignore')
                                get_detail_count(folder)
                    else:
                        print("use -s to traverse %s" % fn)
                else:
                    print("%s: No such file or directory\n" % fn)
        else:
            DirList(os.curdir, 0, 0, 0)
            # os.curdir 是当前目录地址
            mainloop()
