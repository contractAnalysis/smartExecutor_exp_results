# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 10:11:43 2022

@author: 18178
"""
root='C:\\22_summer_exp\\SmartExecutor_experiment_data\\'
import sys
import os
import ast
import pandas as pd
sys.path.append(root) # the project path on Windows

from result_extraction import raw_result_extraction
from utils import helper

parent_dir='C:\\22_summer_exp\\exp_phase2\\test_phase2_120_contracts\\results_7200s\\'
mythril_tx2_csv='selected_120_contracts_have_DF.csv'


base_dirs=[
    'C:\\22_summer_exp\\exp_phase2\\test_phase2_120_contracts\\results_7200s\\1st\\',
     'C:\\22_summer_exp\\exp_phase2\\test_phase2_120_contracts\\results_7200s\\2nd\\',
         'C:\\22_summer_exp\\exp_phase2\\test_phase2_120_contracts\\results_7200s\\3rd\\'
    ]

tools=['mythril_tx3','smartExecutor_phase2']



#--------------------------------------
# mythril (tx=3) vs smartExecutor

def compare_two_tools(tool1:str, base_dir1:str,tool2:str,base_dir2:str,parent_dir:str):
    csv_tool1=tool1+'_results.csv'
    df_tool1=pd.read_csv(base_dir1+csv_tool1)
    columns_needed=['solidity','solc','contract','time','cov_2','vulnerability','function_cov']
    df_tool1=df_tool1[columns_needed]
    df_tool1['vulnerability']=df_tool1['vulnerability'].map(lambda x: helper.get_num_vul(x))
    df_tool1['time']=df_tool1['time'].map(lambda x: float(x))
    df_tool1['cov_2']=df_tool1['cov_2'].map(lambda x: float(str(x).strip('%')))

    df_tool1.columns=['solidity','solc','contract','time_x','cov_2_x','vulnerability_x','function_cov_x']
    
    csv_tool2=tool2+'_results.csv'
    df_tool2=pd.read_csv(base_dir2+csv_tool2)
    columns_needed=['solidity','solc','contract','time','cov_2','vulnerability','function_cov']
    df_tool2=df_tool2[columns_needed]
    df_tool2['vulnerability']=df_tool2['vulnerability'].map(lambda x: helper.get_num_vul(x))
    df_tool2['time']=df_tool2['time'].map(lambda x: float(x))
    df_tool2['cov_2']=df_tool2['cov_2'].map(lambda x: float(str(x).strip('%')))
    df_tool2.columns=['solidity','solc','contract','time_y','cov_2_y','vulnerability_y','function_cov_y']
    
    df_combine=df_tool1.merge(df_tool2,on=['solidity','solc','contract'])
    
    
    # compute the function coverage difference
    for i in range(len(df_combine)):
        ftn_cov_x=df_combine.loc[i,'function_cov_x']
        ftn_cov_y=df_combine.loc[i,'function_cov_y']
        cov_diff=helper.function_coverage_difference(ftn_cov_x,ftn_cov_y)
        df_combine.loc[i,'#_function_high_cov']=len(cov_diff)
        df_combine.loc[i,'function_x_m_y']=str(cov_diff)
    df_combine.to_csv(parent_dir+tool1+"_vs_"+tool2+"_7200s_results.csv")
    
    return get_general_data_statistics(df_combine), df_combine
    

def get_general_data_statistics(df_data:pd.DataFrame):
    total_contracts=df_data.shape[0]
    total_time_1=df_data['time_x'].sum()
    total_time_2=df_data['time_y'].sum()
    total_bugs_1=df_data['vulnerability_x'].sum()
    total_bugs_2=df_data['vulnerability_y'].sum()
    ave_time_1=df_data['time_x'].mean()
    ave_time_2=df_data['time_y'].mean()

    ave_cov_1=df_data['cov_2_x'].mean()
    ave_cov_2=df_data['cov_2_y'].mean()
    total_ftn_high_cov=df_data['#_function_high_cov'].sum()

    
    general_data=[total_contracts,total_time_1,total_bugs_1,ave_time_1,ave_cov_1,total_ftn_high_cov]+\
    [total_time_2,total_bugs_2,ave_time_2,ave_cov_2]
    return general_data
    
def collect_ftn_increased_coverage(df_data:pd.DataFrame)->dict:
    results={}
    for idx in range(len(df_data)):
        ftns_with_increased_cov=df_data.loc[idx,'function_x_m_y']
        ftns_with_increased_cov=ast.literal_eval(ftns_with_increased_cov)
        if len(ftns_with_increased_cov)>0:
            key=df_data.loc[idx,'solidity']+"_"+df_data.loc[idx,'contract']
            results[key]=ftns_with_increased_cov        
    return results
            



targets=['1st_7200s_','2nd_7200s_','3rd_7200s_'] 
results=[['results','total_contracts','total_time_1','total_bugs_1','ave_time_1','ave_cov_1','total_ftn_high_cov']+\
         ['total_time_2','total_bugs_2','ave_time_2','ave_cov_2']
         ] 
ftn_results={}

for i,base_dir in enumerate(base_dirs):
    for tool in tools:
        target=targets[i]+tool+"_vs_"+"mythril_tx2"
        general_data,df_combined=compare_two_tools( tool,base_dir,'mythril_tx2', parent_dir,base_dir)
        results.append([target]+general_data)
        
        ftn_with_increased_cov=collect_ftn_increased_coverage(df_combined)
        ftn_results[target]=ftn_with_increased_cov
        
df_results=pd.DataFrame(results)
df_results=df_results.T
df_results.to_csv(parent_dir+"general_statistics.csv",index=False) 


ftn_results_list=[]
for target, ftn_with_coverage_increased in ftn_results.items():
    result=[target]
    
    for key, ftn_cov_list in ftn_with_coverage_increased.items():        
        for ftn_cov in ftn_cov_list:
            re=[key]+ftn_cov
            result.append(re)
       
    ftn_results_list.append(result)


df_ftn_results=pd.DataFrame(ftn_results_list)
df_ftn_results.to_csv(parent_dir+"function_with_increased_coverage.csv",index=False)




    