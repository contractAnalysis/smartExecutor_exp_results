
import sys
import os
import csv
# import pandas as pd
import numpy as np
import json
import ast

def random_select(data:list, seed:int, num:int):
    if len(data)<num:
        return data
    np.random.seed(seed)
    selected = np.random.choice(data, size=num, replace=False)
    return list(selected)

def remove_B_from_A(A:list, B:list):
    """
    remove the elements in B from A
    """
    for b in B:
        if b in A:
            A.remove(b)
    return A

def find_all_file(dir:str,extension:str):
    """
    Given a parent directory, find all files with extension of extension
    Args:
        dir: parent directory, e.g. "/usr/admin/HoloToken/"

    Returns:
        list of file directories. e.g. ["/usr/admin/HoloToken/user0001.extension"......]
    """
    res = []
    for file in os.listdir(dir):
        if file.endswith("."+extension):
            res.append(os.path.join(dir, file))
    return res

def get_num_vul(data:str):
    res = ast.literal_eval(data)
    if isinstance(res,dict):
        return len( res.keys())
    else: return 0 
    
def count_deep_functions(data:str):
    count=0
    data=str(data)      
    if '[]' in data: return 0
    mylist = ast.literal_eval(data)
    for item in mylist:
        cov=str(item[0]).strip('%')
        if float(cov)<100:
            if not str(item[1]) in ['name', 'symbol', 'safeSub', 'safeMul','safeAdd','safeDiv']:
                count+=1
    return count

def function_coverage_difference(dataA:str,dataB:str):
    results=[]
    if '[]' in dataA or '[]' in dataB: return []
    a=ast.literal_eval(dataA)
    a_dict={}
    b=ast.literal_eval(dataB)
    b_dict={}
    for item in a:
        cov=float(str(item[0]).strip('%'))
        ftn=str(item[1]).strip()
        a_dict[ftn]=cov
    for item in b:
        cov=float(str(item[0]).strip('%'))
        ftn=str(item[1]).strip()
        b_dict[ftn]=cov
    assert len(a_dict)==len(b_dict)
    for ftn,cov_a in a_dict.items():
        cov_b=b_dict[ftn]
        # print(f'ftn:{ftn} ')
        # print(f'cov_x:{cov_x} ')
        # print(f'cov_y:{cov_y} ')
        # assert cov_x>=cov_y
        if cov_a>cov_b:
            cov_diff=cov_a-cov_b
            results.append([ftn,cov_diff])
    return results

def average(data:list):
    valid_items=[]
    sum=0
    for item in data:
        if item!=0:
            valid_items.append(item)
    length= len(valid_items) 
    if len(valid_items)==0.0:
        return 0
    
    for item in valid_items:
        sum+=item
    return sum/length

# df = df[~df['date'].isin(a)]

        
# # parse a string
# aa="[['a',2],['a','b']]"
# mylist = ast.literal_eval(aa)
# mylist

# df['c'] = df.apply(lambda row: row.a + row.b, axis=1)
# # df = df.apply(lambda x: np.square(x) if x.name == 'd' else x, axis=1)
# # df = df.assign(Percentage = lambda x: (x['Total_Marks'] /500 * 100))


# # iterate rows
# for i in range(len(df_data_combined_temp)):
#     print(df_data_combined_temp.loc[i, "contract"], df_data_combined_temp.loc[i, "time"])


# # 'Name' and 'Stream' column respectively.
# for ind in df.index:
#     print(df['Name'][ind], df['Stream'][ind])

# remove the digits and '.' in a string
# tool_column_key=re.sub(r'[0-9|.]+', '', tool)

# df_data_combined_temp['mythril']=df_data_combined_temp.apply(lambda row: "no results" if row.m_cov_2 in ["-1",'0',0,-1] else 'x', axis=1)
# df_data_combined_temp['smartExecutor']=df_data_combined_temp.apply(lambda row: "no results" if row.se_cov_2 in ["-1",'0',0,-1] else 'x', axis=1)
# df_data_combined_temp['smartian']=df_data_combined_temp.apply(lambda row: "no results" if row['#_edge'] in ['0',0] else 'x', axis=1)
    
# # filtered out contracts
#     mythril_data_filter_out=mythril_data[(mythril_data.m_cov2 =='-1') | (mythril_data.m_cov2 =='0')]