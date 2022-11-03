# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 16:29:28 2022

@author: 18178
"""


import sys
import os
import csv
import pandas as pd
import numpy as np     
import shutil
import math

import pandas as pd
sys.path.append('C:\\22_summer_exp\\DataPreparation\\') # the project path on Windows

from result_extraction import raw_result_extraction
from utils import helper


#*********************************************************************
# Parameter setting
#*********************************************************************

#=======================================================
# count the number of contracts that do not have timeoutget data from collected results for timeout 1800s and 900s

#======================================================
parent_dir='C:\\22_summer_exp\\exp_mythril_smartExecutor\\'
base_dirs=[
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_1800s\\1st\\',
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_1800s\\2nd\\',
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_1800s\\3rd\\',    
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_900s\\1st\\',
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_900s\\2nd\\',
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_900s\\3rd\\'
]

mark='mythril_vs_smartExecutor_phase1_'
targets=['1800s_1st','1800s_2nd','1800s_3rd','900s_1st','900s_2nd','900s_3rd'] 
timeouts=[1800,1800,1800,900,900,900] 
tools=['mythril','smartExecutor','smartExecutor_phase1']








#*********************************************************************
#  code area
#*********************************************************************
def convert_integer(x:str,solidity:str):
    if x not in ['False']:
        return int(x)
    else:        
        print(f'no valid {x} number:{solidity}')
        return 0

def convert_coverage_float(x:str,solidity:str):
    if '%' in x:
        return float(str(x).strip('%'))
    elif x in [0,-1,'0','-1']:
        return float(x)
    else:
        print(f'no valid coverage in :{solidity}')
        return 0

def count_num_of_contracts_regarding_timeout(tool:str,base_dir:str,timeout):
    total_contracts=0
    num_before_timeout=0

   
    results_csv=tool+"_results.csv"
    df_results=pd.read_csv(base_dir+results_csv)
    total_contracts=df_results.shape[0]
    
    
    df_results['time']=df_results.apply(lambda x: float(x.time), axis=1)
    
    num_before_timeout=df_results[df_results.time<=timeout].shape[0]
    return [num_before_timeout,total_contracts-num_before_timeout]
    
 
def get_data_from_same_contracts(tool1:str,tool2:str,base_dir:str):
    total_contracts=0
    total_time_1=0
    total_time_2=0
    total_bugs_1=0
    total_bugs_2=0
    total_state_1=0
    total_state_2=0
    ave_cov_1=0
    ave_cov_2=0

    df_results1=pd.read_csv(base_dir+tool1+"_left.csv")
    df_results1['time']=df_results1['time'].map(lambda x: float(x))
    df_results1['num_states']=df_results1['num_states'].map(lambda x: int(x)) 
    df_results1['cov_2']=df_results1['cov_2'].map(lambda x: float(x))
    df_results1['vulnerability']=df_results1['vulnerability'].map(lambda x: float(x))

    
    df_results2=pd.read_csv(base_dir+tool2+"_left.csv")
    df_results2['time']=df_results2['time'].map(lambda x: float(x))
    df_results2['num_states']=df_results2['num_states'].map(lambda x: int(x))   
    df_results2['cov_2']=df_results2['cov_2'].map(lambda x: float(x))
    df_results2['vulnerability']=df_results2['vulnerability'].map(lambda x: float(x))

    
    df_results1.columns=['solidity','solc','contract','time_x','num_states_x','cov_2_x','vulnerability_x']
    df_results2.columns=['solidity','solc','contract','time_y','num_states_y','cov_2_y','vulnerability_y']    
    df_combined=df_results1.merge(df_results2,on=['solidity','solc','contract']) 
    
    total_contracts=df_combined.shape[0]
    total_time_1=df_combined['time_x'].sum()/3600
    total_time_2=df_combined['time_y'].sum()/3600
    total_bugs_1=df_combined['vulnerability_x'].sum()
    total_bugs_2=df_combined['vulnerability_y'].sum()
    total_state_1=df_combined['num_states_x'].sum()
    total_state_2=df_combined['num_states_y'].sum()

    ave_cov_1=df_combined['cov_2_x'].mean()
    ave_cov_2=df_combined['cov_2_y'].mean()
    time_diff_series=df_combined.apply(lambda x: x.time_x -x.time_y, axis=1).astype(float)
    bug_diff_series=df_combined.apply(lambda x: x.vulnerability_x -x.vulnerability_y, axis=1).astype(int)    
    cov_diff_series=df_combined.apply(lambda x: x.cov_2_x -x.cov_2_y, axis=1).astype(float)
    
    return [total_contracts,total_time_1,total_bugs_1,total_state_1,ave_cov_1,total_time_2,total_bugs_2,total_state_2,ave_cov_2],time_diff_series,bug_diff_series,cov_diff_series
    





#=======================================================
# count the number of contracts that are finished before timeout and after timeout
#======================================================

num_data=[]
for i, base_dir in enumerate(base_dirs):
    target=targets[i]
    for index, tool in enumerate(tools):
        re=count_num_of_contracts_regarding_timeout(tool,base_dir,timeouts[i])
        num_data.append([target+"_"+tool]+re)

df_num_data=pd.DataFrame(num_data)
columns=['name','num_before_timeout','num_after_timeout']
df_num_data.columns=columns

df_num_data.to_csv(parent_dir+"count_timeouts_900s_1800s.csv")





