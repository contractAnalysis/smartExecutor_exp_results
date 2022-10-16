

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



# # #=======================================================
# # # SB_all  results
# # #======================================================
# base_dirs_SB_all=[
#             # 'C:\\22_summer_exp\\exp_benchmark\\SB\\all\\results_1800s\\1st\\',           
#           'C:\\22_summer_exp\\exp_benchmark\\SB\\all\\results_1800s\\2nd\\', 
#           # 'C:\\22_summer_exp\\exp_benchmark\\SB\\all\\results_1800s\\3rd\\',
# ]
# base_dirs=base_dirs_SB_all
# # shared parameters
# group_start_index=1
# group_end_index=28
# group_size=7
# group_name_prefix='contracts_7_group'
# flag_ftn=False  




# # #=======================================================
# # # B2  results
# # #======================================================
# base_dirs_B2=[
#           'C:\\22_summer_exp\\exp_benchmark\\B2\\results_1800s\\1st\\', 
#           'C:\\22_summer_exp\\exp_benchmark\\B2\\results_1800s\\2nd\\',           
#           'C:\\22_summer_exp\\exp_benchmark\\B2\\results_1800s\\3rd\\'
#             ]
# base_dirs=base_dirs_B2
# # shared parameters
# group_start_index=1
# group_end_index=27
# group_size=3
# group_name_prefix='contracts_3_group'
# flag_ftn=False    



# #=======================================================
# # SB_all  results
# #======================================================
base_dirs_SB_IB_RE_ULC=[
        'C:\\22_summer_exp\\exp_benchmark\\SB\IB_RE_ULC\\1800s_results\\1st\\',           
        'C:\\22_summer_exp\\exp_benchmark\\SB\IB_RE_ULC\\1800s_results\\2nd\\',  
        'C:\\22_summer_exp\\exp_benchmark\\SB\IB_RE_ULC\\1800s_results\\3rd\\',  
]
base_dirs=base_dirs_SB_IB_RE_ULC
# shared parameters
group_start_index=1
group_end_index=26
group_size=4
group_name_prefix='contracts_4_group'
flag_ftn=False  


# #=======================================================
# # the code to collect results
# #======================================================
result_folder_prefix=['mythril_group','smartExecutor_group','smartian_group']
tools=['mythril','smartExecutor','smartian']

for base_dir in base_dirs:
    # get raw results and save to csv files
    for idx, tool in enumerate(tools):
        df_data=raw_result_extraction.extract_raw_results(group_start_index,
                                                          group_end_index,
                                                          group_size,
                                                          base_dir,
                                                          group_name_prefix,
                                                          result_folder_prefix[idx],
                                                          tool,
                                                          flag_ftn)
    
    








