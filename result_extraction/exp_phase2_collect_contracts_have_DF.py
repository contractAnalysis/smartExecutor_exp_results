# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 17:26:37 2022

@author: 18178
"""

root='C:\\22_summer_exp\\SmartExecutor_experiment_data\\'

import sys
import os
import csv
import pandas as pd
import numpy as np     
import shutil
import math
import ast

# add this path as we run this file in Spyder on Windows so that Spyder can find utils.mythril.utils
sys.path.append(root) # the project path on Windows
from utils import helper
from result_extraction import raw_result_extraction
from utils import Constants




#=======================================================================================================================
#===== collect contracts that have deep functions ====
#========================================================
# run smartExecutor without fdg flag (i.e., mythril), timeout<1800s, have results
# collect resullts
group_start_index=1
group_end_index=417
group_size=12
base_dir='C:\\22_summer_exp\\exp_phase2\\find_contracts_DF\\'   
group_name_prefix='contracts_12_group'
result_folder_prefix='smartExecutor_group'
tool='smartExecutor'
flag_ftn=True    

# df_data=raw_result_extraction.extract_raw_results(group_start_index, group_end_index,group_size,base_dir,group_name_prefix,result_folder_prefix,tool, flag_ftn)
   
# compute deep functions
def contracts_have_DF_from_CSV(csv_file_path:str,dir_base:str,output_csv:str)->pd.DataFrame: 
    df_results=pd.read_csv(results_csv_path)
    return contracts_have_DF(df_results,dir_base,output_csv)

def contracts_have_DF(df_results:pd.DataFrame,dir_base:str,output_csv:str)->pd.DataFrame:
    df_results['#_total_deep_func']=df_results['function_cov'].map(lambda x: helper.count_deep_functions(x))
    # get contracts that have deep functions
    df_contracts_DF=df_results[df_results['#_total_deep_func']>0] 
    # get contracts that have coverage
    df_contracts_DF=df_contracts_DF[(df_contracts_DF['cov_2'] !='-1') & (df_contracts_DF['cov_2'] !='0')]
   
    df_contracts_DF['time']=df_contracts_DF['time'].map(lambda x: float(x))
    df_contracts_DF=df_contracts_DF[(df_contracts_DF['time'] <1800)]    #  keep contracts that use time less than 1800 seconds
    
    df_contracts_DF.to_csv(dir_base+output_csv,index=False, header=True,sep=',', line_terminator='\n')
    return df_contracts_DF
    

results_csv_path=base_dir+tool+"_results.csv" 
output_csv="contracts_have_DF.csv"
if os.path.exists(results_csv_path):        
    df_contracts_DF=contracts_have_DF_from_CSV(results_csv_path,base_dir,output_csv)
else:    
    df_data=raw_result_extraction.extract_raw_results(group_start_index, group_end_index,group_size,base_dir,group_name_prefix,result_folder_prefix,tool, flag_ftn)
    df_contracts_DF=contracts_have_DF(df_data,base_dir,output_csv)


