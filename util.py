import string


# 有些容器和模块的名字只有最前面几个字符匹配，认为最前面匹配数量到达4个，就代表匹配成功
def frontSubstr(str1,str2):
    num = 0
    len1 = len(str1)
    len2 = len(str2)
    i = 0
    j = 0
    while i<len1 and j<len2:
        if str1[i] == str2[j]:
            i += 1
            j += 1
            num += 1
            if num>=4:
                return True
        else:
            return False

# 看容器名和模块名是否匹配
def isMatch(str1,str2):
    flag = False
    # 获取str2的缩写
    str2_length = len(str2)
    str2_abbreviation = ''
    for i in range(str2_length):
        if str2[i].isupper():
            str2_abbreviation += str2[i]
    str2_abbreviation = str2_abbreviation.lower()

    # 统一字符的大小写
    str1 = str1.lower()
    str2 = str2.lower()

    str1_element = str1.split('-')
    str1_element_length = len(str1_element)

    # 去除字符中无关的符号
    str1 = str1.translate(str.maketrans('','',string.punctuation))
    str2 = str2.translate(str.maketrans('','',string.punctuation))

    # 要是有相互包含关系的则匹配上
    if str1 in str2 or str2 in str1:
        flag = True
        return flag

    # 如果str1中元素与str2匹配度达到0.5，则算匹配上
    match_num = 0
    for ele in str1_element:
        if ele in str2 or ele in str2_abbreviation:
            match_num += 1
            str2 = str2[len(ele):]
        else:
            if frontSubstr(ele,str2):
                match_num += 1
    if match_num/str1_element_length >0.5 :
        flag = True
        return flag

    # str2最后一位是数字的话，可以认为匹配成功
    if (ord(str2[-1])-ord('0')) in range(10):
        flag = True
        return flag

    return False