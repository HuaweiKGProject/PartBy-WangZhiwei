from bs4 import BeautifulSoup
from pathlib import Path
import re
from config import data_config
import json
from util import isMatch
pages = [BeautifulSoup(open(Path(data_config['document_dir'],url),encoding='GBK'),'html.parser') for url in data_config['contain_relation_url']]
# html = BeautifulSoup(open(Path(data_config['document_dir'],data_config['contain_relation_url']),encoding='GBK'),'html.parser')
# <a name="zh-cn_topic_0172858983_table1847424713469"></a>
Total_VM = []

for html in pages:
    a = html.find('a',attrs={'name':'zh-cn_topic_0172858983_table1847424713469'})
    while a.name != 'div':
        a = a.parent
    table = a.find('table')
    title = html.find('title').text.split('虚拟机')[0]
    rows = table.find_all('tr')
    # # 表格head格式化一下文本
    # table_head = [_.text.replace('\n', '').strip() for _ in rows[0].find_all('th')]
    # # 文档的表格存在一些叫法不统一,这里做一些重映射
    # table_head = [head_map[_] if _ in head_map else _ for _ in table_head]
    head = rows[0].find_all('th')

    VM_Type = head[0].text.strip()
    POD_Name = head[1].text.strip()
    Container_Name = head[2].text.strip()
    # Module_Name = head[3].text.strip()


    contain_relation = {}
    num_tds_front = len(head)

    for row in rows[1:]:

        # container_module = {}
        pod_container = {}
        tds = row.find_all('td')
        num_tds_present = len(tds)

        VM_temp = tds[0].text.strip()

        num_container = 1
        # num_module = 1
        # 判断第一列是否为空
        if num_tds_present>=num_tds_front:
            nameOfVM = VM_temp
            nameOfPod = tds[1].text.strip()
            # 容器和模块部分可能有多个<li>或者只有一个<p>
            liOfContainer = row.find_all('td')[2].find_all('li')
            # liOfModule = row.find_all('td')[3].find_all('li')

            pOfContainer = row.find_all('td')[2]
            # pOfModule = row.find_all('td')[3]
            if len(liOfContainer)!=0:
                num_container = len(liOfContainer)
            # if len(liOfModule) != 0:
            #     num_module = len(liOfModule)

        else:
            nameOfPod = tds[0].text.strip()

            liOfContainer = row.find_all('td')[1].find_all('li')
            # liOfModule = row.find_all('td')[2].find_all('li')
            pOfContainer = row.find_all('td')[1]
            # pOfModule = row.find_all('td')[2]

            if len(liOfContainer)!=0:
                num_container = len(liOfContainer)

        if num_container > 1:
            for i in range(num_container):
                pod_container.setdefault(nameOfPod,[]).append(liOfContainer[i].text.strip())
        else:
            pod_container.setdefault(nameOfPod,[]).append((pOfContainer.text.strip()))
        contain_relation.setdefault(nameOfVM,[]).append(pod_container)

    with open('/home/wangoldfei/Desktop/New_Contain_relation.json', 'a+') as f:
        json.dump(contain_relation, f, ensure_ascii=False, indent='\t')
        f.write("\n")
