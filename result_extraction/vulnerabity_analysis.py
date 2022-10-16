# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 22:47:55 2022

@author: 18178
"""
root='C:\\22_summer_exp\\SmartExecutor_experiment_data\\'
import sys
import ast
import pandas as pd
sys.path.append(root) # the project path on Windows

from result_extraction import raw_result_extraction

#=======================================================
# B2 -> 1st  results
#======================================================
target='B2_1st'
# shared parameters
group_start_index=1
group_end_index=27
group_size=3
base_dir='C:\\22_summer_exp\\exp_benchmark\\B2\\results_1800s\\1st_1\\'   
group_name_prefix='contracts_3_group'
flag_ftn=False    

benchmark_vul_csv='B2_contract_info.csv'

# get the mapping from byte addresses to line numbers of the source code
batin_dir='C:\\22_summer_exp\\exp_benchmark\\batin\\'
benchmark_batin_csv='B2_batin_results.csv'  




# #=======================================================
# # SB -> 1st  results
# #======================================================
# target='SB_1st'
# # shared parameters
# group_start_index=1
# group_end_index=28
# group_size=7
# base_dir='C:\\22_summer_exp\\exp_benchmark\\SB\\all\\results_1800s\\1st\\'   
# group_name_prefix='contracts_7_group'
# flag_ftn=False    

# benchmark_vul_csv='SB_Curated_all_contract_info.csv' 

# # get the mapping from byte addresses to line numbers of the source code
# batin_dir='C:\\22_summer_exp\\exp_benchmark\\batin\\'
# benchmark_batin_csv='SB_all_batin_results.csv'   




smatian_vulnerability_names=['IntegerBug','Reentrancy','MishandledException','BlockstateDependency']
mythril_vulnerability_SWC_ID=['101','107','104', '120']
target_vulnerability_indices=[0,1,2]


tools=['mythril','smartExecutor','smartian']


#=======================================================================================================================
#---------------------------------------------------------------
# combine the results in csv files
columns_needed=['solidity','solc','contract','time','cov_2','vulnerability']
df_data_combined=pd.read_csv(base_dir+benchmark_vul_csv)

for tool in tools:
    csv_results=base_dir+tool+"_results.csv"
    df_data=pd.read_csv(csv_results)
    # filter some data not needed 
    if tool in 'mythril':
        # select columns        
        df_data=df_data[columns_needed]
        # rename columns
        df_data.columns=['solidity','solc','contract','mt_time','mt_cov_2','mt_vulnerability']
        
    elif tool in 'smartExecutor':        
        df_data=df_data[columns_needed] 
        df_data.columns=['solidity','solc','contract','se_time','se_cov_2','se_vulnerability']
    elif tool in 'smartian':
        columns_needed=['solidity', 'solc', 'contract', 'time', '#_edge', '#_instructioins','vulnerability']
        df_data=df_data[columns_needed]
        df_data.columns=['solidity', 'solc', 'contract', 'st_time', '#_edge', '#_instructioins','st_vulnerability']
      
    else:pass
    
    #merge data
    if df_data_combined.empty:
        df_data_combined=df_data
    else:
        df_data_combined=df_data_combined.merge(df_data,on=['solidity','solc','contract'])        
df_data_combined.to_csv(base_dir+target+"_combined_results.csv")



df_data_combined_temp=df_data_combined
#---------------------------------------------------------------
#  get the mapping from byte addresses to line numbers of the source code
df_benchmark_mapper =pd.read_csv(batin_dir+benchmark_batin_csv)
benchmark_byteAddress_to_lineno={}
benchmark_runtime_offset={}
for index in range(len(df_benchmark_mapper)):
    key=df_benchmark_mapper.loc[index,'solidity']+"_"+df_benchmark_mapper.loc[index,'contract']
    address_to_line=ast.literal_eval(df_benchmark_mapper.loc[index,'address_to_line'])
    benchmark_byteAddress_to_lineno[key]=address_to_line
    benchmark_runtime_offset[key]=int(df_benchmark_mapper.loc[index,'runtime_offset'])
    
    
#---------------------------------------------------------------
# for mythril and smartExecutor
def vul_id_line_pcAddr(vul:str, target_vul_id:str):
    vuls=[]
    res = ast.literal_eval(vul)
    if isinstance(res,dict):
        for bug in res.values():
            # print(bug['SWC_ID'])
            if str(bug['SWC_ID']).strip() in [target_vul_id,int(target_vul_id)]:
                if 'file_point' in bug.keys():
                    vuls.append({'SWC_ID':bug['SWC_ID'],"pcAddr":bug['PC_address'],'line':bug['file_point']})
                else:
                    vuls.append({'SWC_ID':bug['SWC_ID'],"pcAddr":bug['PC_address']})
    if len(vuls)==0:
        return '0'
    return str(vuls)

# for smartian (report vulnerabilities at byte addresses based on creation code while batin produces mapping based on runtime code)
def vul_byteAddr_lineno(solidty_file_name:str, contract_name:str, vul:str, target_vul_name:str):
    vuls=[]
    res=ast.literal_eval(vul)
    if isinstance(res,dict):
        for bug in res.values():
            if str(bug['name']).strip() in  target_vul_name:
                key=solidty_file_name+"_"+contract_name
                point_decimal=int(bug['point'], 16)
                runtime_offset=benchmark_runtime_offset[key]
                # if runtime_offset!=-1:
                #     runtime_point_decimal=point_decimal-runtime_offset
                # else:
                #      runtime_point_decimal=point_decimal
                runtime_point_decimal=point_decimal
                if str(runtime_point_decimal) in benchmark_byteAddress_to_lineno[key].keys():
                    lineno=benchmark_byteAddress_to_lineno[key][str(runtime_point_decimal)]  
                else:
                    lineno='not found'
                vuls.append({'name':bug['name'],'point_hex':bug['point'],'point_decimal':int(bug['point'], 16),'line':lineno})
    if len(vuls)==0:
        return '0'
    return str(vuls)


#---------------------------------------------------------------
# iterate all contracts to identify if the labeled vulnerabilities are reported by each tool or not
m_vul_targets=[mythril_vulnerability_SWC_ID[index] for index in target_vulnerability_indices]
smartian_vul_targets=[smatian_vulnerability_names[index] for index in target_vulnerability_indices]

for i in range(len(df_data_combined_temp)):

    # vul_type=df_data_combined_temp.loc[i, "bugs_x"] #B2
    vul_type=df_data_combined_temp.loc[i, "vul_type"] #SB
    
    # get the labeled vulnerailities
    vul_types=ast.literal_eval(vul_type)
    types=[]
    if isinstance(vul_types,list):
        for item in vul_types:
            if item[0] not in types:
                types.append(item[0].strip())
    if len(types)==0:continue  

    
    # find vulnerabilites that belong to the labeled vulnerabilities
    m_vul=""
    se_vul=""
    if 'UNCHECKED_LL_CALLS'in types and '104' in m_vul_targets :
        m_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "m_vulnerability"],'104')
        se_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "se_vulnerability"],'104')
        
    if 'REENTRANCY' in types  and '107' in m_vul_targets :
        m_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "m_vulnerability"],'107')
        se_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "se_vulnerability"],'107')
        
    if 'BAD_RANDOMNESS' in types and '120' in m_vul_targets :
        m_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "m_vulnerability"],'120')
        se_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "se_vulnerability"],'120')
        
    if 'ARITHMETIC' in types and '101' in m_vul_targets :
        m_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "m_vulnerability"],'101')
        se_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "se_vulnerability"],'101')
    else:
        pass    
    df_data_combined_temp.loc[i, "mythril"]=m_vul
    df_data_combined_temp.loc[i, "smartExecutor"]=se_vul
    
    st_vul=""
    if 'UNCHECKED_LL_CALLS'in types and 'MishandledException' in smartian_vul_targets :
        st_vul+=vul_byteAddr_lineno(df_data_combined_temp.loc[i, "solidity"],df_data_combined_temp.loc[i, "contract"],df_data_combined_temp.loc[i, "st_vulnerability"],'MishandledException')
    
    if 'REENTRANCY' in types  and 'Reentrancy' in smartian_vul_targets :
        st_vul+=vul_byteAddr_lineno(df_data_combined_temp.loc[i, "solidity"],df_data_combined_temp.loc[i, "contract"],df_data_combined_temp.loc[i, "st_vulnerability"],'Reentrancy')
    
    if 'BAD_RANDOMNESS' in types and 'BlockstateDependency' in smartian_vul_targets :
        st_vul+=vul_byteAddr_lineno(df_data_combined_temp.loc[i, "solidity"],df_data_combined_temp.loc[i, "contract"],df_data_combined_temp.loc[i, "st_vulnerability"],'BlockstateDependency')
    
    if 'ARITHMETIC' in types and 'IntegerBug' in smartian_vul_targets : 
        st_vul+=vul_byteAddr_lineno(df_data_combined_temp.loc[i, "solidity"],df_data_combined_temp.loc[i, "contract"],df_data_combined_temp.loc[i, "st_vulnerability"],'IntegerBug')

    df_data_combined_temp.loc[i, "smartian"]= st_vul
    
   
#---------------------------------------------------------------
# mark 'no results' if a tool does not have results collected.
df_data_combined_temp['mythril']=df_data_combined_temp.apply(lambda row: "no results" if row.m_cov_2 in ["-1",'0',0,-1] else row.mythril, axis=1)
df_data_combined_temp['smartExecutor']=df_data_combined_temp.apply(lambda row: "no results" if row.se_cov_2 in ["-1",'0',0,-1] else row.smartExecutor, axis=1)
df_data_combined_temp['smartian']=df_data_combined_temp.apply(lambda row: "no results" if row['#_edge'] in ['0',0] else row.smartian, axis=1)
    


#---------------------------------------------------------------
# select_columns=['solidity','solc','contract','vul_type','bugs_x','mt_time','se_time','time','mythril','smartExecutor','smartian'] #B2
select_columns=['solidity','solc','contract','vul_points','vul_type','mt_time','se_time','st_time','mythril','smartExecutor','smartian']#SB
df_data_combined_temp=df_data_combined_temp[select_columns]
df_data_combined_temp.to_csv(base_dir+target+"_combined_results_my_data.csv")
