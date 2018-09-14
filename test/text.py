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
    singleCmtFlags = ['#','//']  # 单行注释符号
    multiCmtFlagListone = ['"""',"'''","//*"]
    multiCmtFlagListtwo = ['"""',"'''","*//"] 
    qttnFlagList = ['"',"'"]  # 引号列表
    startPos = 0  # 搜索多行注释符的开始位置
    isCmtRet = True
    # print 'line: ' + line.strip()
    while startPos < len(line):  # 查找注释符号直到行末
        if multiCmtFlagIdx == -1:  # 不在多行注释中
            minStartIdx = len(line)  # 搜索到最靠前的多行注释符
            # 单行注释
            for singleCmtFlag in singleCmtFlags:
                #re.match(pattern, string, flags=0),匹配开头,\s是任意空白字符
                if re.match(r'(\s)*' + singleCmtFlag, line[startPos:]):
                    return isCmtRet
            idx = 0
            preStartIdx = startPos  # 记录搜索多行注释符前的搜索位置
            while idx < len(multiCmtFlagListone):
                # 多行注释开始符号
                startCmtFlag = multiCmtFlagListone[idx]
                try:
                    #re.search(pattern, string, flags=0)找到第一个匹配然后返回,(?<!pattern)
                    startPos = re.search(
                        r'(?<!\\)' + startCmtFlag, line[startPos:]).start() + startPos  # 找到多行注释开始符号
                    if isInQuotation(line[:startPos], startCmtFlag, qttnFlagList):  # 注释开始符在引号中
                        # 找下一个多行注释开始符
                        startPos += len(startCmtFlag.replace('\*', '*'))
                        continue
                    else:  # 注释符号不在引号中
                        startPos += len(startCmtFlag.replace('\*', '*'))
                        if startPos < minStartIdx:
                            multiCmtFlagIdx = idx  # 是多行注释
                            minStartIdx = startPos
                        startPos = preStartIdx  # 找下一个多行注释开始符
                        idx += 1
                except:
                    idx += 1
                    continue  # 没有找到多行注释开始符，继续查找下个类型的符号
            if minStartIdx != len(line):  # 此时搜索到了多行注释开始符
                startCmtFlag = multiCmtFlagListone[multiCmtFlagIdx]
                if not re.match(r'(\s)*' + startCmtFlag, line[preStartIdx:]):
                    isCmtRet = False
            elif line[preStartIdx:] != '\n':
                isCmtRet = False
            startPos = minStartIdx
        elif multiCmtFlagIdx != -1:  # 在多行注释中
            # 多行注释开始符
            endCmtFlag = multiCmtFlagListone[multiCmtFlagIdx]
            if endCmtFlag == '':
                return False, -1  # 注释符号配置有错误
            try:
                startPos \
                    = re.search(endCmtFlag, line[startPos:]).start() \
                    + startPos \
                    + len(endCmtFlag.replace('\*', '*'))  # 查找多汗注释结束符的位置
                multiCmtFlagIdx = -1
            except:
                break
    # print isCmtRet, multiCmtFlagIdx
    return isCmtRet  # 返回是否注释行，以及当前是否在多行注释中


'''
函数名：isInQuotation
功能：根据字符串中引号的奇偶，判断后面的字符是否在引号中
输入：
 line: 一行代码中指定字符前的字符串
 qttnFlagList: 引号列表
输出：
 布尔值：
  True：字符串包含在引号中
  False：字符串不包含在引号中
'''


def isInQuotation(line, cmtFlag, qttnFlagList):
    qttnFlagIdx = len(line)
    flagIdx = len(line)
    rearLine = line
    for i in range(len(qttnFlagList)):
        flag = qttnFlagList[i]
        if flag == cmtFlag[0]:  # 排除引号同时也是注释符号的情况
            continue
        try:
            flagIdx = re.search(r'(?<!\\)' + flag + r'.*',
                                line).start()  # 查找左引号
            rearLine = re.search(r'(?<!\\)' + flag + r'.*',
                                 line).group()[len(flag):]
        except:
            flagIdx = len(line)
        if flagIdx < qttnFlagIdx:  # 根据最早出现的左引号，确认左引号类型
            qttnFlagIdx = flagIdx
            qttnFlag = flag
    if qttnFlagIdx != len(line):
        try:
            # print rearLine
            rearLine = re.search(r'(?<!\\)' + qttnFlag + r'.*',
                                 rearLine).group()[len(qttnFlag):]  # 查找右引号
            # 再次查找下一个左引号
            return isInQuotation(rearLine, cmtFlag[0], qttnFlagList)
        except:
            return True  # 在引号对中
    else:
        return False  # 不在引号对中


def main():
    fd = open('text.py', errors='ignore')
    datas = fd.readlines()
    codelines = 0
    nulllines = 0
    commentlines = 0
    lines = 0
    singleCmtFlags = ['#','//']  # 单行注释符号
    for data in datas:
        # 判断代码行，空行,注释行
        # windows下的编辑器，在只要读到文本最后有'\n'的时候，都会另起一行，显示为空行。其实第二行根本就不存在。
        lines += 1
        if data.strip() == '':
            nulllines += 1
        else:
            if isCmt(data,-1):
                commentlines += 1
            else:
                codelines += 1
    print(commentlines)
    print(nulllines)
    print(codelines)
    print(lines)

if __name__ == '__main__':
    main()
