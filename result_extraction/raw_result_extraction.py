# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 17:50:24 2022

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
import re

# add this path as we run this file in Spyder on Windows so that Spyder can find utils.mythril.utils
sys.path.append(root) # the project path on Windows

from utils import helper
from result_extraction import file_extraction

tools=['mythril','smartExecutor','smartian','batin']


# add this dict because a tool name may have a prefix and/or suffix attached
tools_to_column_keys={
    
    "smartExecutor":'smartExecutor',
    'smartexecutor_phase1':'smartexecutor',
    'smartexecutor_phase2':'smartexecutor',
    'smartExecutor_ftn_cov':'smartExecutor_ftn_cov',
    # 'smartExecutor_phase1_ftn_cov':'smartExecutor_ftn_cov',
    'mythril':'mythril',
    "mythril_ftn_cov":'mythril_ftn_cov',
    'smartian':'smartian',
    'batin':'batin',
    'B2_batin':'batin',
    'SB_all_batin':'batin',
    'SB_IR_RE_ULC_batin':'batin',  
    }


columns_dict={
    'smartian': ['solidity', 'solc', 'contract', 'time', '#_edge', '#_instructioins', '#_bugs','vulnerability'],
    
    'mythril':['solidity','solc','contract','time','num_states','cov_1','cov_2','vulnerability','#_total_runtime_instr'],
    'mythril_ftn_cov':['solidity','solc','contract','time','num_states','cov_1','cov_2','vulnerability','phase2','#_total_runtime_instr','function_cov', '#_covered_deep_func','#_total_deep_func'],
    
    'smartExecutor':['solidity','solc','contract','time','num_states','cov_1','cov_2','vulnerability','#_total_runtime_instr'],
    'smartExecutor_ftn_cov':['solidity','solc','contract','time','num_states','cov_1','cov_2','vulnerability','phase2','#_total_runtime_instr','function_cov', '#_covered_deep_func','#_total_deep_func'],
    
    'batin':['solidity','solc','contract','runtime_offset','address_to_line'],
    # 'SB_all_batin':['solidity','solc','contract','runtime_offset','address_to_line'],
    # 'B2_batin':['solidity','solc','contract','runtime_offset','address_to_line'],

    }   




def get_group_path(base_dir:str, group_index:int, group_name_prefix:str, result_folder_prefix:str,tool:str):
    path=base_dir
    if len(tool)>0:
        path+=tool+"_results\\"
    if len(group_name_prefix)>0:
        path+=group_name_prefix+"_"+str(group_index)+"\\"
    if len(result_folder_prefix)>0:
        path+=result_folder_prefix+"_"+str(group_index)+"_results\\" 
    return path
    


# extract results from one group
def extract_raw_results_from_one_group(folder_path:str,tool:str, group_size:int)->dict:

    data_dict={}       
    all_files= helper.find_all_file(folder_path,'txt')  
    if len(all_files)<group_size:
        path=''
        for item in folder_path.split("\\")[0:-2]:
            path+=item+"\\"
        all_files+=helper.find_all_file(path,'txt')
    if len(all_files)<group_size:
        print(f'path: {folder_path}')
        print(f'number of files: {len(all_files)}')
    
    for file in all_files:
        #print(file)
        key=str(file).split("\\")[-1] # get the file name
        
        # select different file reading methods based on tools
        results=[]
        if tools[0] in tool or tools[1] in tool: # tool may have a suffix and/or prefix attached
            results=file_extraction.file_read_include_ftn_coverage(file)
        elif tools[2] in tool:
            results=file_extraction.file_read_smartian(file)
        elif tools[3] in tool:
            results=file_extraction.file_read_batin(file)
        else:
            pass             
        if len(results[0])==0:
            print(f'file no results:{file}')
        if key not in data_dict.keys(): # assume that the solidity file names within a group are different
            data_dict[key]=results
            
    return data_dict



def extract_raw_results(con_index_start:int, con_index_end:int,group_size:int,base_dir:str,group_name_prefix:str,result_folder_prefix:str,tool:str, flag_ftn:bool)->list:
    my_data={}
    all_results=[]
    
    # go through all groups
    for i in range(con_index_start,con_index_end+1,1):
        
        # prepare the folder path
        folder_path= get_group_path(base_dir,i,group_name_prefix,result_folder_prefix,tool)       
  
        # extract raw results from a group
        data_dict=extract_raw_results_from_one_group(folder_path,tool,group_size)
       
        # collect some data from raw results based on different tools
        results=[]
        if tools[0] in tool or tools[1] in tool:
            if flag_ftn:
                results=collect_data_include_ftn_coverage(data_dict)
            else:
                results=collect_data(data_dict)
        elif tools[2]  in tool:
            results=collect_data_smartian(data_dict)
        elif tools[3] in tool :
            results=collect_data_batin(data_dict)        
        
        all_results+=results
    
    # output to a csv file
    csv_file_name=tool+"_results.csv"
    df_data=pd.DataFrame(all_results)

    # select columns based on tools
    if tools[0] in tool:
        if flag_ftn:
            column_key=tools_to_column_keys[tools[0]+"_ftn_cov"]          
        else:
            column_key=tools_to_column_keys[tools[0]]
    elif tools[1] in tool:
        if flag_ftn:
            column_key=tools_to_column_keys[tools[1]+"_ftn_cov"]          
        else:
            column_key=tools_to_column_keys[tools[1]]
    elif tools[2] in tool:
        column_key=tools_to_column_keys[tools[2]]
    elif tools[3] in tool:
         column_key=tools_to_column_keys[tools[3]]
    else:
        column_key='smartExecutor'
    
    column_names=columns_dict[column_key]
    df_data.columns=column_names
    
    df_data.to_csv(base_dir+csv_file_name,index=False, header=True,sep=',', line_terminator='\n')
    return df_data
 
           

def collect_data_smartian(data_dict:dict)->list:
    results=[]
    for value in data_dict.values():
        re=[]
        re += value[0][0:4]
        re+=value[1:]
        results.append(re)
    return results

def collect_data(data_dict:dict)->list:
    results=[]
    for key, value in data_dict.items():  
        re=[]
        # solidity solc contract runtime  
        re+=value[0][0:4]
         
        # states
        if len(value[1])>0:
            re+=[value[1][2]]                
        else:
            re+=[0]       
            
        # coverage
        if len(value[2])>2:
            re+=[-1,-1]  # means there are more than 2 coverage items
        elif len(value[2])==2:
            re+=value[2][0:2] 
        elif len(value[2])==1:
            re+=[value[2][0],0]
        else:
            re+=[0,0]                
            
        # vulnerabilities
        if len(value[3])>0:
            re+=[value[3]]
        else:
            re+=[0]
            
        re.append(value[4]) # total number of instructions( obatined to compute coverage for smartian)       
        results.append(re)        
    return results

def collect_data_include_ftn_coverage(data_dict:dict)->list:
    results=[]
    for key, value in data_dict.items():        
        re=[]
        # solidity solc contract runtime  
        re+=value[0][0:4]
         
        # states
        if len(value[1])>0:
            re+=[value[1][2]]                
        else:
            re+=[0]       
            
        # coverage
        if len(value[2])>2:
            re+=[-1,-1]  # means there are more than 2 coverage items
        elif len(value[2])==2:
            re+=value[2][0:2] 
        elif len(value[2])==1:
            re+=[value[2][0],0]
        else:
            re+=[0,0]                
            
        # vulnerabilities
        if len(value[3])>0:
            re+=[value[3]]
        else:
            re+=[0]
            
        re.append(value[4]) # have phase 2 (only meaningful for smartExecutor)
        re.append(value[5]) # total number of instructions( obatined to compute coverage for smartian)
        re.append(value[6]) # function coverage
        re+=value[7]# deep function related
        
        results.append(re)
        
    return results
 
def collect_data_batin(data_dict:dict)->list:
    results=[]
    for key, value in data_dict.items():        
        re=[]
        # solidity solc contract runtime  
        re+=value[0][0:3]            
        re.append(value[1]) # the offset of the runtime code within the createion code  
        re.append(value[2]) # mapping from addresses to line numbers    
        results.append(re)        
    return results    
 
    
 
if __name__=="__main__":
    import re
    string = 'smartExecutor1.0.3'
    newstring = re.sub(r'[0-9|.]+', '', string)
    print(newstring)
    
    # group_start_index=1
    # group_end_index=417
    # group_size=12
    # base_dir='C:\\22_summer_exp\\exp_phase2\\find_contracts_DF\\'   
    # group_name_prefix='contracts_12_group'
    # result_folder_prefix='smartExecutor_group'
    # tool='smartExecutor'
    # flag_ftn=True    
    # df_data=extract_raw_results(group_start_index, group_end_index,group_size,base_dir,group_name_prefix,result_folder_prefix,tool, flag_ftn)
    
