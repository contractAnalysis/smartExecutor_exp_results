# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 09:48:08 2022

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

#=======================================================
# collect results from randomly selected 120 contracts
#======================================================


base_dirs=[
    'C:\\22_summer_exp\\exp_phase2\\test_phase2_120_contracts\\results_7200s\\1st\\',
     'C:\\22_summer_exp\\exp_phase2\\test_phase2_120_contracts\\results_7200s\\2nd\\',
         'C:\\22_summer_exp\\exp_phase2\\test_phase2_120_contracts\\results_7200s\\3rd\\'
    ]


group_start_index=1
group_end_index=30
group_size=4
base_dir='C:\\22_summer_exp\\exp_phase2\\test_phase2\\test_1\\results_7200s\\'   
group_name_prefix='contracts_4_group'
flag_ftn=True  

tools=['mythril_tx3','smartExecutor_phase2']
result_folder_prefix=['mythril_group','smartExecutor_group']


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



