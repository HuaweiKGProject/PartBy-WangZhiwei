from pathlib import Path
data_root=r'/home/wangoldfei/Desktop/dataset/EKG参考'
data_config={
    'data_root':data_root,
    'kg_sheets':r'三元组',
    'kg_jsons':r'三元组_json',
    'new_kg_sheets':Path('新数据','三元组'),
    'new_kg_jsons':Path('新数据','三元组_json'),
    'document_dir':Path(data_root,r'UPCF_2100_infoCenter_hwics_cn_for_EKG/resources'),
    'navi':r'navi.xml',

    'mml_root_topic':'zh-cn_topic_0266315970.html',
    # 'contain_relation_url':'zh-cn_topic_0250727577.html',
    'contain_relation_url':['zh-cn_topic_0250727578.html','zh-cn_topic_0250727577.html'],
    'contain_relation_json':'contain_relation.json',
    'contain_relation':'contain_relation.json',

    'mml_json':'mml.json',
    'mml2mml_relation':'mml2mml_relation.json',
}
