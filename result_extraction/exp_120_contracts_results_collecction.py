# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 09:48:08 2022

@author: 18178
"""

import sys
import os
import ast
import pandas as pd
sys.path.append('C:\\22_summer_exp\\DataPreparation\\') # the project path on Windows

from result_extraction import raw_result_extraction
from utils import helper

#=======================================================
# collect results from randomly selected 120 contracts
#======================================================


# base_dirs=[
#     'C:\\22_summer_exp\\exp_120_contracts\\',
#     ]
# tools=['dubaser','smartExecutor']
# result_folder_prefix=['dubaser_group','smartExecutor_group']



# base_dirs=[
#     'C:\\22_summer_exp\\exp_120_contracts\\dubaser_alld\\7200s_results\\',
#     ]
# tools=['dubaser_alld','mythril_tx3']
# result_folder_prefix=['dubaser_group','mythril_group']



# base_dirs=[
#     'C:\\22_summer_exp\\exp_120_contracts\\dubaser_alld\\1800s_results\\',
#     ]
# tools=['dubaser_alld']
# result_folder_prefix=['dubaser_group']



# base_dirs=[
#     'C:\\22_summer_exp\\exp_120_contracts\\dubaser_alld_cov\\1800s_results\\',
#     ]
# tools=['dubaser_alld_cov']
# result_folder_prefix=['dubaser_group']




# base_dirs=[
#     'C:\\22_summer_exp\\exp_120_contracts\\dubaser_alld_cov1\\1800s_results\\',
#     ]
# tools=['dubaser_alld_cov1']
# result_folder_prefix=['dubaser_group']




base_dirs=[
    'C:\\22_fall_exp\\test_120_contracts\\1800s_results\\',
    ]
tools=['mythril_tx2','smartExecutor','smartExecutor_3.0']
result_folder_prefix=['mythril_group','smartExecutor_group','smartExecutor_group']




# base_dirs=[
#     'C:\\22_fall_exp\\test_120_contracts\\7200s_results\\',
#     ]
# tools=['mythril_tx3','smartExecutor_phase2','smartExecutor_3.0']
# result_folder_prefix=['mythril_group','smartExecutor_group','smartExecutor_group']




group_start_index=1
group_end_index=30
group_size=4

group_name_prefix='contracts_4_group'
flag_ftn=True  


for i, base_dir in enumerate(base_dirs):
    for index,tool in enumerate(tools):
        if os.path.exists(base_dir+tool+"_results.csv"):
            continue
        df_data=raw_result_extraction.extract_raw_results(group_start_index,
                                                          group_end_index,
                                                          group_size,
                                                          base_dir,
                                                          group_name_prefix,
                                                          result_folder_prefix[index],
                                                          tool,
                                                          flag_ftn)



