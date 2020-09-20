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
    Module_Name = head[3].text.strip()

    VM_POD = {}
    POD_Container = {}

    num_tds_front = len(head)
    for row in rows[1:]:
        Container_Module = {}
        tds = row.find_all('td')

        num_tds_present = len(tds)
        VM_temp = tds[0].text.strip()
        num_container = 1
        num_module = 1
        if num_tds_present>=num_tds_front:
            VM = VM_temp
            liOfContainer = row.find_all('td')[2].find_all('li')
            liOfModule = row.find_all('td')[3].find_all('li')

            if len(liOfContainer)!=0:
                num_container = len(liOfContainer)
            if len(liOfModule) != 0:
                num_module = len(liOfModule)

            pOfContainer = row.find_all('td')[2]
            pOfModule = row.find_all('td')[3]
            valueOfPod = tds[1].text.strip()
        else:
            valueOfPod = tds[0].text.strip()

            liOfContainer = row.find_all('td')[1].find_all('li')
            liOfModule = row.find_all('td')[2].find_all('li')

            if len(liOfContainer)!=0:
                num_container = len(liOfContainer)
            if len(liOfModule) != 0:
                num_module = len(liOfModule)

            pOfContainer = row.find_all('td')[1]
            pOfModule = row.find_all('td')[2]
        print(num_container,num_module)
        key1 = VM
        key2 = valueOfPod

        # if key not in Total_VM:
        #     Total_VM.append(key)
        VM_POD.setdefault(key1,[]).append(valueOfPod)
        if num_module == num_container:
            if num_container>1:
                for i in range(num_module):
                    Container_Module.setdefault(liOfContainer[i].text.strip(),[]).append(liOfModule[i].text.strip())
            else:
                Container_Module.setdefault(pOfContainer.text.strip(), []).append(pOfModule.text.strip())
        else:
            m = 0
            n = 0
            while m<num_container and n<num_module:
                if isMatch(liOfContainer[m].text.strip(),liOfModule[n].text.strip()):
                    Container_Module.setdefault(liOfContainer[m].text.strip(), []).append(liOfModule[n].text.strip())
                    n += 1
                else:
                    m += 1

        with open('/home/wangoldfei/Desktop/Container_Module.json', 'a+') as f:
            json.dump(Container_Module, f, ensure_ascii=False, indent='\t')
            f.write("\n")