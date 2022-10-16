# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 19:37:06 2022

@author: 18178
"""
root='C:\\22_summer_exp\\SmartExecutor_experiment_data\\'
import sys
import os

# add this path as we run this file in Spyder on Windows so that Spyder can find utils.mythril.utils
sys.path.append(root) # the project path on Windows


from utils import Constants


def file_read_smartian(file_path)->list:
    contract_info = []
    
    flg_info_mark="#@contract_info_time"
    flag_info = False
    
    covered_instructions=0
    covered_instructions_mark="Covered Instructions"
    
    covered_edges = 0
    covered_edges_mark="Covered Edges :"
    
    bugs={}
    bug_index=0
    bug_mark="Tx#"

    read_file = open(file_path, 'r', encoding='utf8')
    for line in read_file.readlines():
        line = line.strip('\n').strip()
        if len(line) == 0:
            continue 
        if covered_edges_mark in line:
            covered_edges=line.split(':')[-1]
            continue
        elif covered_instructions_mark in line:
            covered_instructions = line.split(':')[-1]
            continue
        elif bug_mark in line:
            #tx#2 found BlockstateDependency at eb2
            items=line.split("found")[1].strip().split(' ')
            bugs['bug'+str(bug_index)]={"name":items[0],"point":items[2]}
            bug_index+=1
            continue
        elif flg_info_mark in line:
            flag_info=True
            continue

        if flag_info:
            flag_info = False
            contract_info = line.split(':')
         
    return [contract_info,covered_edges,covered_instructions,bug_index,bugs]


def file_read(file_path)->list:
    statespace=[]
    flag_state=False
    flag_state_mark='#@statespace'
    
    coverage=[]
    flag_cov=False
    flag_cov_mark="#@coverage"
    
    bugs={}
    flag_bug=False
    flag_bug_mark='===='
    
    contract_info=[]
    flag_info=False
    flag_info_mark="#@contract_info_time"
    
    bug_name=''
    bug_index=0    
    
    total_instructions=0
    flag_total_instr_mark="@@contract_total_instructions:"      

    
    read_file= open(file_path,'r', encoding='utf8')
    for line in read_file.readlines():
        line=line.strip('\n').strip()
        if len(line)==0:
            continue
        if line.startswith(flag_state_mark):
            flag_state=True
            continue
        elif line.startswith(flag_cov_mark):
            flag_cov=True
            continue

            
        elif line.startswith(flag_bug_mark):            
            if line[0:5]=="=====":continue
            bug_index += 1
            bugs['bug' + str(bug_index)]={}
            bug_name=line.split('====')[1]
            bugs['bug'+str(bug_index)]['name']=bug_name
            flag_bug=True          
            continue
        
        elif line.startswith(flag_info_mark):
            flag_bug=False # if contract_info_time is reached, definitely flag_bug should  be false
            flag_info=True     
           
            continue
            
        elif line.startswith(flag_total_instr_mark):
            total_instructions=line.split(flag_total_instr_mark)[-1]           
            continue


        if flag_bug:
            line_eles=line.split(":")
            if line_eles[0].strip()=="SWC ID":
                bugs['bug'+str(bug_index)]['SWC_ID']=line_eles[1]
            elif line_eles[0].strip()=='Severity':
                bugs['bug'+str(bug_index)]['Severity']=line_eles[1]
            elif line_eles[0].strip() == 'Contract':
                bugs['bug' + str(bug_index)]['Contract'] = line_eles[1]
            elif line_eles[0].strip() == 'Function name':
                bugs['bug' + str(bug_index)]['Function_name'] = line_eles[1]
            elif line_eles[0].strip() == 'PC address':
                bugs['bug' + str(bug_index)]['PC_address'] = line_eles[1]
            elif line_eles[0].strip() == 'Estimated Gas Usage':
                bugs['bug' + str(bug_index)]['Estimated_Gas_Usage'] = line_eles[1]
            elif line_eles[0].strip() == 'In file':
                bugs['bug' + str(bug_index)]['file_point'] = line_eles[-1]
                
              

        elif flag_state:
            flag_state=False
            # line format: 25 nodes, 24 edges, 363 total states
            line_eles=line.split(',')
            for ele in line_eles:
                statespace.append(ele.strip().split(' ')[0])
        elif flag_cov:
            flag_cov=False            
            #line format:Achieved 5.50% coverage for code: 6060604052341561000f576
            # in case of timeout, no coverage is obtained
            if "coverage" in line:
                coverage.append(line.split(' ')[1])

        elif flag_info:
            flag_info=False
            contract_info=line.split(':')
        else:
            pass
    return  [contract_info,statespace,coverage,bugs,total_instructions]



def file_read_include_ftn_coverage(file_path)->list:
    # if file_path.split('\\')[-1].startswith('0x6b31cda4dea5c77559e3ed87361e15e6b28b3cde.sol__DharmaSmartWalletImplementationV7Prototype0Staging.txt'):
    #     print(f'xx')
    #     if os.path.exists(file_path):
    #         print('exists')
    #     else:
    #         print(f'dooes not exist')
    #     # return []
    
    contract_into_1st_line=[]
    flag_info_1st_mark='++++'
    
    statespace=[]
    flag_state=False
    flag_state_mark='#@statespace'
    
    coverage=[]
    flag_cov=False
    flag_cov_mark="#@coverage"
    
    bugs={}
    flag_bug=False
    flag_bug_mark='===='
    
    contract_info=[]
    flag_info=False
    flag_info_mark="#@contract_info_time"
    
    bug_name=''
    bug_index=0
    
    flag_go_through_sequence_generation=False
    flag_go_seq_mark="@@WEI:go_through_sequence_generation"
    
    total_instructions=0
    flag_total_instr_mark="@@contract_total_instructions:"
    
    function_coverage=[]
    flag_ftn_cov=False
    flag_ftn_cov_mark="#@function_coverage"
    
    deep_ftn_status=[0,0]
    flag_deep_ftn_mark="deep functions:"
    
    read_file= open(file_path,'r', encoding='utf-8')
    for line in read_file.readlines():
        line=line.strip('\n').strip()
        if len(line)==0:
            continue
        if line.startswith(flag_info_1st_mark):
            '++++ 0x0fd1021a603b347bfafdf028b56b993ca652c034.sol  :  0.5.16  :  BinaryOptionMarket ++++'
            line=line.strip('++++')
            contract_into_1st_line=line.split(":")
            contract_into_1st_line=[str(item.strip()) for item in contract_into_1st_line]
            continue
        if line.startswith(flag_state_mark):
            flag_state=True
            continue
        elif line.startswith(flag_cov_mark):
            flag_cov=True
            continue
        elif line.startswith(flag_ftn_cov_mark):
            flag_ftn_cov=True
            continue
            
        elif line.startswith(flag_bug_mark):            
            if line[0:5]=="=====":continue
            bug_index += 1
            bugs['bug' + str(bug_index)]={}
            bug_name=line.split('====')[1]
            bugs['bug'+str(bug_index)]['name']=bug_name
            flag_bug=True
            flag_ftn_cov=False # assume function coverage is printed before bug reports
            continue
        
        elif line.startswith(flag_info_mark):
            flag_bug=False # if contract_info_time is reached, definitely flag_bug should  be false
            flag_info=True
            flag_ftn_cov=False
           
            continue
        elif line.startswith(flag_go_seq_mark):
            flag_go_through_sequence_generation=True
            continue            
        elif line.startswith(flag_total_instr_mark):
            total_instructions=line.split(flag_total_instr_mark)[-1]           
            continue
        elif line.startswith(flag_deep_ftn_mark):
            #:deep functions: 0 out of 3 is(are) meaningfully executed.
            items=line.split(":")[1].strip().split(' ')
            deep_ftn_status=[items[0],items[3]]
            continue

        if flag_bug:
            line_eles=line.split(":")
            if line_eles[0].strip()=="SWC ID":
                bugs['bug'+str(bug_index)]['SWC_ID']=line_eles[1]
            elif line_eles[0].strip()=='Severity':
                bugs['bug'+str(bug_index)]['Severity']=line_eles[1]
            elif line_eles[0].strip() == 'Contract':
                bugs['bug' + str(bug_index)]['Contract'] = line_eles[1]
            elif line_eles[0].strip() == 'Function name':
                bugs['bug' + str(bug_index)]['Function_name'] = line_eles[1]
            elif line_eles[0].strip() == 'PC address':
                bugs['bug' + str(bug_index)]['PC_address'] = line_eles[1]
            elif line_eles[0].strip() == 'Estimated Gas Usage':
                bugs['bug' + str(bug_index)]['Estimated_Gas_Usage'] = line_eles[1]
            elif line_eles[0].strip() == 'In file':
                bugs['bug' + str(bug_index)]['file_point'] = line_eles[-1]
                
              

        elif flag_state:
            flag_state=False
            # line format: 25 nodes, 24 edges, 363 total states
            line_eles=line.split(',')
            for ele in line_eles:
                statespace.append(ele.strip().split(' ')[0])
        elif flag_cov:
            flag_cov=False            
            #line format:Achieved 5.50% coverage for code: 6060604052341561000f576
            # in case of timeout, no coverage is obtained
            if "coverage" in line:
                coverage.append(line.split(' ')[1])
        elif flag_ftn_cov:
            if '%' in line and ':' in line:
                function_coverage.append(line.split(":"))            
            
        elif flag_info:
            flag_info=False
            contract_info=line.split(':')
        else:
            pass
    if len(contract_info)==0:
        contract_info=contract_into_1st_line+[0,0,0,0]
    return  [contract_info,statespace,coverage,bugs,flag_go_through_sequence_generation,total_instructions,function_coverage,deep_ftn_status]


def file_read_batin(file_path)->list:

    address_to_line={}    
    mark_byte_address='byte address:'
    mark_line_no='line no:'
    
    mark_runtime_offset='#@runtime_code_offset:'
    runtime_offset=0
    
    flag_address=False
    address=0

    flag_info=False
    flag_info_mark="#@contract_info_time"
    contract_info=[]
    
    read_file= open(file_path,'r', encoding='utf8')
    for line in read_file.readlines():
        line=line.strip('\n').strip()
        if len(line)==0:
            continue
        if line.startswith(mark_byte_address):
            flag_address=True
            address=line.split(mark_byte_address)[-1].strip()
            continue
        elif line.startswith(mark_line_no):
            if flag_address:
                flag_address=False
                line_no=line.split(mark_line_no)[-1].strip()
                address_to_line[address]=line_no   
            continue
        elif line.startswith(mark_runtime_offset):
            runtime_offset=line.split(mark_runtime_offset)[-1].strip()
            
        elif line.startswith(flag_info_mark):
            flag_info=True
            continue
            
        if flag_info:           
            contract_info=line.split(':')
        
    return  [contract_info,runtime_offset,address_to_line]

    
    
    
    


if __name__ == "__main__":    
    
    file_name='0x5c3e96662397a75e334ca2db3c9835bdb0b2cb8e.sol__OTC.txt'
    path=Constants.base_path_dict["exp_phase2_3600s_1st"]+"mythril_results\\contracts_13_group_1\\mythril_group_1_results\\"
  
    results=file_read_include_ftn_coverage(path+file_name)
    print(results)
    results=file_read(path+file_name)
    print(results)


    # dir='C:\\22_summer_exp\\exp_test\\check_results\\contracts_1_group_1\\smartExecutor_group_1_results\\0x47f5fd811ef75c8f0823ef675401641eacf8d6a9.sol__LimitsDMAndCountryRestrictions.txt'
    # results=file_read_include_ftn_coverage(dir)
    # print(results)

    