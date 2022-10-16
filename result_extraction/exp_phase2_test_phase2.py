# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 16:13:30 2022

@author: 18178
"""

root='C:\\22_summer_exp\\SmartExecutor_experiment_data\\'
import sys
import ast
import pandas as pd
sys.path.append(root) # the project path on Windows

from result_extraction import raw_result_extraction
from utils import helper



# #=======================================================
# # test_1  results
# #======================================================
# target='test_1'
# group_start_index=1
# group_end_index=30
# group_size=1
# base_dir='C:\\22_summer_exp\\exp_phase2\\test_phase2\\test_1\\results_7200s\\'   
# group_name_prefix='contracts_1_group'
# flag_ftn=True  

# #=======================================================
# # test_2  results
# #======================================================
# target='test_2'
# group_start_index=1
# group_end_index=30
# group_size=1
# base_dir='C:\\22_summer_exp\\exp_phase2\\test_phase2\\test_2\\results_7200s\\'   
# group_name_prefix='contracts_1_group'
# flag_ftn=True  
  


# #=======================================================
# # the code to collect results 
# #======================================================
# columns_needed=['solidity','solc','contract','time','cov_2','vulnerability','function_cov', '#_covered_deep_func','#_total_deep_func']

# # tools=['mythril','smartExecutor1.0','smartExecutor1.0.1','smartExecutor1.0.2','smartExecutor1.0.3','smartExecutor1.0.4','smartExecutor1.0.5','smartExecutor1.0.6','smartExecutor1.0.7']
# tools=['mythril','smartExecutor','smartExecutor1','smartExecutor2','smartExecutor3','smartExecutor4','smartExecutor5','smartExecutor6','smartExecutor7']


# # get raw results save output to csv files
# for tool in tools:
#     if tool.startswith("smartExecutor"):
#         result_folder_prefix='smartExecutor_group'
#     else:
#         result_folder_prefix='mythril_group'
#     df_data=raw_result_extraction.extract_raw_results(group_start_index, group_end_index,group_size,base_dir,group_name_prefix,result_folder_prefix,tool, flag_ftn)

 

# # get data from csv files and needed data   
# df_data_combined=pd.DataFrame()
# for tool in tools:
#     csv_results=base_dir+tool+"_results.csv"
#     df_data=pd.read_csv(csv_results)
#     df_data=df_data[columns_needed]
#     df_data["#_bugs"]=df_data["vulnerability"].map(lambda x: helper.get_num_vul(x))
#     if "mythril" in tool:
#         df_data['#_total_deep_func']=df_data['function_cov'].map(lambda x: helper.count_deep_functions(x))
#         df_data_combined=df_data  
#     else:
#         df_data_combined=df_data_combined.merge(df_data,on=['solidity','solc','contract'])
# df_data_combined.to_csv(base_dir+target+"_combined_results.csv")    


    
#=======================================================================================================================
# #=======================================================
# # test_1  results
# #======================================================
# target='test_1'
# group_start_index=1
# group_end_index=30
# group_size=1
# base_dir='C:\\22_summer_exp\\exp_phase2\\test_phase2\\test_1\\results_7200s\\'   
# group_name_prefix='contracts_1_group'
# flag_ftn=True  


#=======================================================
# test_2  results
#======================================================
target='test_2'
group_start_index=1
group_end_index=30
group_size=1
base_dir='C:\\22_summer_exp\\exp_phase2\\test_phase2\\test_2\\results_7200s\\'   
group_name_prefix='contracts_1_group'
flag_ftn=True  




#--------------------------------------
# mythril (tx=3) vs smartExecutor
csv_mythril='mythril_results.csv'
df_mythril=pd.read_csv(base_dir+csv_mythril)
columns_needed=['solidity','solc','contract','time','cov_2','vulnerability','function_cov']
df_mythril=df_mythril[columns_needed]
df_mythril.columns=['solidity','solc','contract','time_x','cov_2_x','vulnerability_x','function_cov_x']

csv_smartExecutor='smartExecutor_results.csv'
df_smartExecutor=pd.read_csv(base_dir+csv_smartExecutor)
columns_needed=['solidity','solc','contract','time','cov_2','vulnerability','function_cov','#_total_deep_func']
df_smartExecutor=df_smartExecutor[columns_needed]
df_smartExecutor.columns=['solidity','solc','contract','time_y','cov_2_y','vulnerability_y','function_cov_y','#_total_deep_func_y']

df_combine=df_mythril.merge(df_smartExecutor,on=['solidity','solc','contract'])

# compute the number of detected bugs
df_combine['#_vul_x']=df_combine['vulnerability_x'].map(lambda x: helper.get_num_vul(x))
df_combine['#_vul_y']=df_combine['vulnerability_y'].map(lambda x: helper.get_num_vul(x))

# compute the function coverage difference
for i in range(len(df_combine)):
    ftn_cov_x=df_combine.loc[i,'function_cov_x']
    ftn_cov_y=df_combine.loc[i,'function_cov_y']
    cov_diff=helper.function_coverage_difference(ftn_cov_y,ftn_cov_x)
    df_combine.loc[i,'#_function_high_cov']=len(cov_diff)
    df_combine.loc[i,'function_y_x']=str(cov_diff)
df_combine.to_csv(base_dir+"mythril_tx3_smartExecutor_7200s_results.csv")

#--------------------------------------
# mythril (tx=2) mythril (tx=3)
csv_mythril='selected_contracts.csv'
df_mythril=pd.read_csv(base_dir+csv_mythril, header=None)
columns_needed=[0,1,2,3,6,7,10]
df_mythril=df_mythril[columns_needed]
df_mythril.columns=['solidity','solc','contract','time_x','cov_2_x','vulnerability_x','function_cov_x']

csv_mythril_1='mythril_results.csv'
df_mythril_1=pd.read_csv(base_dir+csv_mythril_1)
columns_needed=['solidity','solc','contract','time','cov_2','vulnerability','function_cov']
df_mythril_1=df_mythril_1[columns_needed]
df_mythril_1.columns=['solidity','solc','contract','time_y','cov_2_y','vulnerability_y','function_cov_y']

df_combine=df_mythril.merge(df_mythril_1,on=['solidity','solc','contract'])

# compute the number of detected bugs
df_combine['#_vul_x']=df_combine['vulnerability_x'].map(lambda x: helper.get_num_vul(x))
df_combine['#_vul_y']=df_combine['vulnerability_y'].map(lambda x: helper.get_num_vul(x))

# compute the function coverage difference
for i in range(len(df_combine)):
    ftn_cov_x=df_combine.loc[i,'function_cov_x']
    ftn_cov_y=df_combine.loc[i,'function_cov_y']
    cov_diff=helper.function_coverage_difference(ftn_cov_y,ftn_cov_x)
    df_combine.loc[i,'#_function_high_cov']=len(cov_diff)
    df_combine.loc[i,'function_y_x']=str(cov_diff)
df_combine.to_csv(base_dir+"mythril_tx2_tx3_7200s_results.csv")


#--------------------------------------
# mythril (tx=2) vs smartExecutor
csv_mythril='selected_contracts.csv'
df_mythril=pd.read_csv(base_dir+csv_mythril,header=None)
columns_needed=[0,1,2,3,6,7,10]
df_mythril=df_mythril[columns_needed]
df_mythril.columns=['solidity','solc','contract','time_x','cov_2_x','vulnerability_x','function_cov_x']

csv_smartExecutor='smartExecutor_results.csv'
df_smartExecutor=pd.read_csv(base_dir+csv_smartExecutor)
columns_needed=['solidity','solc','contract','time','cov_2','vulnerability','function_cov','#_total_deep_func']
df_smartExecutor=df_smartExecutor[columns_needed]
df_smartExecutor.columns=['solidity','solc','contract','time_y','cov_2_y','vulnerability_y','function_cov_y','#_total_deep_func_y']

df_combine=df_mythril.merge(df_smartExecutor,on=['solidity','solc','contract'])

# compute the number of detected bugs
df_combine['#_vul_x']=df_combine['vulnerability_x'].map(lambda x: helper.get_num_vul(x))
df_combine['#_vul_y']=df_combine['vulnerability_y'].map(lambda x: helper.get_num_vul(x))

# compute the function coverage difference
for i in range(len(df_combine)):
    ftn_cov_x=df_combine.loc[i,'function_cov_x']
    ftn_cov_y=df_combine.loc[i,'function_cov_y']
    cov_diff=helper.function_coverage_difference(ftn_cov_y,ftn_cov_x)
    df_combine.loc[i,'#_function_high_cov']=len(cov_diff)
    df_combine.loc[i,'function_y_x']=str(cov_diff)
df_combine.to_csv(base_dir+"mythril_tx2_smartExecutor_7200s_results.csv")
