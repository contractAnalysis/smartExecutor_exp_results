# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 14:02:13 2022

@author: 18178
"""

root='C:\\22_summer_exp\\SmartExecutor_experiment_data\\'
import sys
import ast
import pandas as pd
sys.path.append(root) # the project path on Windows

from result_extraction import raw_result_extraction

# add two  key-value pairs in columns_dict in raw_result_extraction.py
    # 'SB_all_batin':['solidity','solc','contract','address_to_line'],
    # 'B2_batin':['solidity','solc','contract','address_to_line'],
# add 'batin' as the fourth tool in tools in raw_result_extraction.py

# #=======================================================
# # SB_all batin results
# #======================================================
# target='SB_all_batin'
# # shared parameters
# group_start_index=1
# group_end_index=28
# group_size=7
# base_dir='C:\\22_summer_exp\\exp_benchmark\\batin\\'   
# group_name_prefix='contracts_7_group'
# flag_ftn=False  
# result_folder_prefix='batin_group'
# tool='SB_all_batin'
# df_data=raw_result_extraction.extract_raw_results(group_start_index, group_end_index,group_size,base_dir,group_name_prefix,result_folder_prefix,tool, flag_ftn)


# #=======================================================
# # B2 batin  results
# #======================================================
# target='B2_batin'
# # shared parameters
# group_start_index=1
# group_end_index=27
# group_size=3
# base_dir='C:\\22_summer_exp\\exp_benchmark\\batin\\'   
# group_name_prefix='contracts_3_group'
# flag_ftn=False    
# result_folder_prefix='batin_group'
# tool='B2_batin'
# df_data=raw_result_extraction.extract_raw_results(group_start_index, group_end_index,group_size,base_dir,group_name_prefix,result_folder_prefix,tool, flag_ftn)



#=======================================================
# SB_IR_RE_ULC  results
#======================================================
target='SB_IR_RE_ULC_batin'
# shared parameters
group_start_index=1
group_end_index=26
group_size=4
base_dir='C:\\22_summer_exp\\exp_benchmark\\batin\\'   
group_name_prefix='contracts_4_group'
flag_ftn=False    
result_folder_prefix='batin_group'
tool='SB_IB_RE_ULC_batin'
df_data=raw_result_extraction.extract_raw_results(group_start_index, group_end_index,group_size,base_dir,group_name_prefix,result_folder_prefix,tool, flag_ftn)





