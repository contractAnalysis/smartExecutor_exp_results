# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 15:36:09 2022

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


#=======================================================
# collect all results for timeout 1800s and 900s
#======================================================


group_start_index=1
group_end_index=417
group_size=12 
group_name_prefix='contracts_12_group'
flag_ftn=True 


base_dirs=[
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_1800s\\1st\\',
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_1800s\\2nd\\',
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_1800s\\3rd\\',    
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_900s\\1st\\',
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_900s\\2nd\\',
    'C:\\22_summer_exp\\exp_mythril_smartExecutor\\results_900s\\3rd\\'
    ]
 
result_folder_prefix=['mythril_group','smartExecutor_group','smartExecutor_group']
tools=['mythril','smartExecutor','smartExecutor_phase1']
result_folder_prefix=['smartExecutor_group']
tools=['smartExecutor']

for i, base_dir in enumerate(base_dirs):    
    for index, tool in enumerate(tools):
        # if os.path.exists(base_dir+tool+"_results.csv"):  # the results are aready collected
        #     continue
        # get the results
        df_data=raw_result_extraction.extract_raw_results(group_start_index, 
                                                          group_end_index,
                                                          group_size,
                                                          base_dir,
                                                          group_name_prefix,
                                                          result_folder_prefix[index],
                                                          tool,
                                                          flag_ftn)




