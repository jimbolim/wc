import re

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
    singleCmtFlags = ['//']  # 单行注释符号
    multiCmtFlagListone = ["/*"]
    multiCmtFlagListtwo = ["*/"]
    isCmtRet = True
    idx = 0
    # print 'line: ' + line.strip()
    if multiCmtFlagIdx == -1:  # 不在多行注释中
        # 单行注释
        for singleCmtFlag in singleCmtFlags:
            # re.match(pattern, string, flags=0),匹配开头,\s是任意空白字符
            if re.match(r'(\s)*' + singleCmtFlag, line):
                return isCmtRet,multiCmtFlagIdx
        while idx < len(multiCmtFlagListone):
            # 多行注释开始符号
            startCmtFlag = multiCmtFlagListone[idx]
            if startCmtFlag in line:  # 找到多行注释开始符号
                multiCmtFlagIdx = idx
                return isCmtRet,multiCmtFlagIdx
            else:
                idx += 1
                continue  # 没有找到多行注释开始符，继续查找下个类型的符号
        isCmtRet=False
        return isCmtRet,multiCmtFlagIdx
    if multiCmtFlagIdx != -1:  # 在多行注释中
        # 多行注释开始符
        endCmtFlag = multiCmtFlagListtwo[multiCmtFlagIdx]
        if endCmtFlag in line:
            multiCmtFlagIdx = -1
    # print isCmtRet, multiCmtFlagIdx
    return isCmtRet,multiCmtFlagIdx  # 返回是否注释行，以及当前是否在多行注释中


def main():
    fd = open('b.c', errors='ignore')
    datas = fd.readlines()
    codelines = 0
    nulllines = 0
    commentlines = 0
    lines = 0
    multiCmtFlagIdx = -1
    for data in datas:
        # 判断代码行，空行,注释行
        # windows下的编辑器，在只要读到文本最后有'\n'的时候，都会另起一行，显示为空行。其实第二行根本就不存在。
        lines += 1
        data_s = data.replace('\t','')
        data_s = data.replace(' ','')
        if (data.strip() == '' or len(data_s)<3) and multiCmtFlagIdx==-1:
            nulllines += 1
            print(lines)
        else:
            isCmtRet,multiCmtFlagIdx = isCmt(data,multiCmtFlagIdx)
            if isCmtRet or multiCmtFlagIdx!=-1:
                commentlines += 1
            else:
                codelines += 1
    print(commentlines)
    print(nulllines)
    print(codelines)
    print(lines)


if __name__ == '__main__':
    main()
