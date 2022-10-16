# -*- coding: utf-8 -*-

root='C:\\22_summer_exp\\SmartExecutor_experiment_data\\'
import sys
import ast
import pandas as pd
sys.path.append(root) # the project path on Windows

from result_extraction import raw_result_extraction



smatian_vulnerability_names=['IntegerBug','Reentrancy','MishandledException','BlockstateDependency']
mythril_vulnerability_SWC_ID=['101','107','104', '120']
target_vulnerability_indices=[0,1,2,3]

tools=['mythril','smartExecutor','smartian']
benchmark_byteAddress_to_lineno={}




# #=======================================================
# # SB_all  results
# #======================================================
base_dirs_SB_all=[
            root+'exp_benchmark\\SB\\all\\results_1800s\\1st\\',           
          root+'exp_benchmark\\SB\\all\\results_1800s\\2nd\\', 
          root+'xp_benchmark\\SB\\all\\results_1800s\\3rd\\',
]

base_dirs=base_dirs_SB_all
targets=['SB_all_1st', 'SB_all_2nd', 'SB_all_3rd']
batin_dir=root+'exp_benchmark\\batin\\'
benchmark_batin_csv='SB_all_batin_results.csv'  
benchmark_vul_csv='SB_Curated_all_contract_info.csv' 


# # #=======================================================
# # # B2  results
# # #======================================================

# base_dirs_B2=[
#           root+'exp_benchmark\\B2\\results_1800s\\1st\\', 
#           root+'exp_benchmark\\B2\\results_1800s\\2nd\\',           
#           root+'exp_benchmark\\B2\\results_1800s\\3rd\\'
#             ]
# base_dirs=base_dirs_B2
# targets=['B2_1st', 'B2_2nd', 'B2_3rd']
# batin_dir=root+'exp_benchmark\\batin\\'
# benchmark_batin_csv='B2_batin_results.csv'  
# benchmark_vul_csv='B2_contract_info.csv'



# #=======================================================
# # SB IB_RE_ULC  results
# #======================================================
base_dirs_SB_IB_RE_ULC=[
        root+'exp_benchmark\\SB\IB_RE_ULC\\1800s_results\\1st\\',           
        root+'exp_benchmark\\SB\IB_RE_ULC\\1800s_results\\2nd\\',  
        root+'exp_benchmark\\SB\IB_RE_ULC\\1800s_results\\3rd\\',  
]
base_dirs=base_dirs_SB_IB_RE_ULC


targets=['SB_IB_RE_ULC_1st', 'SB_IB_RE_ULC_2nd', 'SB_IB_RE_ULC_3rd']
batin_dir=root+'exp_benchmark\\batin\\'
benchmark_batin_csv='SB_IB_RE_ULC_batin_results.csv'  
benchmark_vul_csv='SB_Curated_contract_info_IB_RE_ULC.csv' 


#=======================================================================================================================
#---------------------------------------------------------------
# combine the results in csv files

def combine_tool_results(base_dir:str, benchmark_vul_csv_path:str,tools:list,target:str)->pd.DataFrame:

    columns_needed=['solidity','solc','contract','time','cov_2','vulnerability']
    df_data_combined=pd.read_csv(benchmark_vul_csv_path)
    
    for tool in tools:
        csv_results=base_dir+tool+"_results.csv"
        df_data=pd.read_csv(csv_results)
        # filter some data not needed 
        if tool in 'mythril':
            # select columns        
            df_data=df_data[columns_needed]
            # rename columns
            df_data.columns=['solidity','solc','contract','mt_time','mt_cov_2','mt_vulnerability']
            
        elif tool in 'smartExecutor':        
            df_data=df_data[columns_needed] 
            df_data.columns=['solidity','solc','contract','se_time','se_cov_2','se_vulnerability']
        elif tool in 'smartian':
            columns_needed=['solidity', 'solc', 'contract', 'time', '#_edge', '#_instructioins','vulnerability']
            df_data=df_data[columns_needed]
            df_data.columns=['solidity', 'solc', 'contract', 'st_time', '#_edge', '#_instructioins','st_vulnerability']
          
        else:pass
        
        #merge data
        if df_data_combined.empty:
            df_data_combined=df_data
        else:
            df_data_combined=df_data_combined.merge(df_data,on=['solidity','solc','contract'])        
    df_data_combined.to_csv(base_dir+target+"_combined_results.csv")
    return df_data_combined
    

def get_byteAddr_to_line_number(batin_result_csv_path:str)->dict:
    df_benchmark_mapper =pd.read_csv(batin_result_csv_path)
    benchmark_byteAddress_to_lineno={}
    for index in range(len(df_benchmark_mapper)):
        key=df_benchmark_mapper.loc[index,'solidity']+"_"+df_benchmark_mapper.loc[index,'contract']
        
        address_to_line=ast.literal_eval(df_benchmark_mapper.loc[index,'address_to_line'])
        benchmark_byteAddress_to_lineno[key]=address_to_line
       
    return benchmark_byteAddress_to_lineno
    

    
#---------------------------------------------------------------
# for mythril and smartExecutor
def vul_id_line_pcAddr(vul:str, target_vul_id:str):
    vuls=[]
    res = ast.literal_eval(vul)
    if isinstance(res,dict):
        for bug in res.values():
            # print(bug['SWC_ID'])
            if str(bug['SWC_ID']).strip() in [target_vul_id,int(target_vul_id)]:
                if 'file_point' in bug.keys():
                    vuls.append({'SWC_ID':bug['SWC_ID'],"pcAddr":bug['PC_address'],'line':bug['file_point']})
                else:
                    vuls.append({'SWC_ID':bug['SWC_ID'],"pcAddr":bug['PC_address']})
    if len(vuls)==0:
        return '0'
    return str(vuls)

# for smartian (report vulnerabilities at byte addresses based runtime code)
def vul_byteAddr_lineno(solidty_file_name:str, contract_name:str, vul:str, target_vul_name:str):
    vuls=[]
    res=ast.literal_eval(vul)
    if isinstance(res,dict):
        for bug in res.values():
            if str(bug['name']).strip() in  target_vul_name:
                key=solidty_file_name+"_"+contract_name
                point_decimal=int(bug['point'], 16)
                
                if str(point_decimal) in benchmark_byteAddress_to_lineno[key].keys():
                    lineno=benchmark_byteAddress_to_lineno[key][str(point_decimal)]  
                else:
                    lineno='None'
                vuls.append({'name':bug['name'],'point_hex':bug['point'],'point_decimal':int(bug['point'], 16),'line':lineno})
    if len(vuls)==0:
        return '0'
    return str(vuls)




def find_target_vulnerabilities(df_data_combined_temp:pd.DataFrame,base_dir:str,target:str,target_vulnerability_indices:list): 
    
    #---------------------------------------------------------------
    # iterate all contracts to identify if the labeled vulnerabilities are reported by each tool or not
    m_vul_targets=[mythril_vulnerability_SWC_ID[index] for index in target_vulnerability_indices]
    smartian_vul_targets=[smatian_vulnerability_names[index] for index in target_vulnerability_indices]
    
    
    
    for i in range(len(df_data_combined_temp)):
    
        # vul_type=df_data_combined_temp.loc[i, "bugs_x"] #B2
        vul_type=df_data_combined_temp.loc[i, "vul_type"] #SB
        
        # get the labeled vulnerailities
        vul_types=ast.literal_eval(vul_type)
        types=[]
        if isinstance(vul_types,list):
            for item in vul_types:
                if item[0] not in types:
                    types.append(item[0].strip())
        if len(types)==0:continue  
    
        
        # find vulnerabilites that belong to the labeled vulnerabilities
        m_vul=""
        se_vul=""
        if 'UNCHECKED_LL_CALLS'in types and '104' in m_vul_targets :
            m_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "mt_vulnerability"],'104')
            se_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "se_vulnerability"],'104')
            
        if 'REENTRANCY' in types  and '107' in m_vul_targets :
            m_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "mt_vulnerability"],'107')
            se_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "se_vulnerability"],'107')
            
        if 'BAD_RANDOMNESS' in types and '120' in m_vul_targets :
            m_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "mt_vulnerability"],'120')
            se_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "se_vulnerability"],'120')
            
        if 'ARITHMETIC' in types and '101' in m_vul_targets :
            m_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "mt_vulnerability"],'101')
            se_vul+=vul_id_line_pcAddr(df_data_combined_temp.loc[i, "se_vulnerability"],'101')
        else:
            pass    
        df_data_combined_temp.loc[i, "mythril"]=m_vul
        df_data_combined_temp.loc[i, "smartExecutor"]=se_vul
        
        st_vul=""
        if 'UNCHECKED_LL_CALLS'in types and 'MishandledException' in smartian_vul_targets :
            st_vul+=vul_byteAddr_lineno(df_data_combined_temp.loc[i, "solidity"],df_data_combined_temp.loc[i, "contract"],df_data_combined_temp.loc[i, "st_vulnerability"],'MishandledException')
        
        if 'REENTRANCY' in types  and 'Reentrancy' in smartian_vul_targets :
            st_vul+=vul_byteAddr_lineno(df_data_combined_temp.loc[i, "solidity"],df_data_combined_temp.loc[i, "contract"],df_data_combined_temp.loc[i, "st_vulnerability"],'Reentrancy')
        
        if 'BAD_RANDOMNESS' in types and 'BlockstateDependency' in smartian_vul_targets :
            st_vul+=vul_byteAddr_lineno(df_data_combined_temp.loc[i, "solidity"],df_data_combined_temp.loc[i, "contract"],df_data_combined_temp.loc[i, "st_vulnerability"],'BlockstateDependency')
        
        if 'ARITHMETIC' in types and 'IntegerBug' in smartian_vul_targets : 
            st_vul+=vul_byteAddr_lineno(df_data_combined_temp.loc[i, "solidity"],df_data_combined_temp.loc[i, "contract"],df_data_combined_temp.loc[i, "st_vulnerability"],'IntegerBug')
    
        df_data_combined_temp.loc[i, "smartian"]= st_vul
        
      

    # #---------------------------------------------------------------
    # # mark 'no results' if a tool does not have results collected.
    # df_data_combined_filtered_out=df_data_combined_temp[df_data_combined_temp['mt_cov_2'].isin( ["-1",'0',0,-1])]
    # df_data_combined_filtered_out=df_data_combined_filtered_out[df_data_combined_filtered_out['se_cov_2'].isin( ["-1",'0',0,-1])] 
    # df_data_combined_filtered_out=df_data_combined_filtered_out[df_data_combined_filtered_out['#_edge'].isin(["0",0])] 
    # df_data_combined_filtered_out.to_csv(base_dir+target+"_combined_results_filtered_out.csv")     
    
    
    # #---------------------------------------------------------------
    # # mark 'no results' if a tool does not have results collected.
    # df_data_combined_temp=df_data_combined_temp[~df_data_combined_temp['mt_cov_2'].isin( ["-1",'0',0,-1])]
    # df_data_combined_temp=df_data_combined_temp[~df_data_combined_temp['se_cov_2'].isin( ["-1",'0',0,-1])] 
    # df_data_combined_temp=df_data_combined_temp[~df_data_combined_temp['#_edge'].isin(["0",0])] 
          
 
    #---------------------------------------------------------------
    # select_columns=['solidity','solc','contract','vul_type','bugs_x','mt_time','se_time','time','mythril','smartExecutor','smartian'] #B2
    select_columns=['solidity','solc','contract','vul_points','vul_type','mt_time','se_time','st_time','mythril','smartExecutor','smartian']#SB
    df_data_combined_temp=df_data_combined_temp[select_columns]
    df_data_combined_temp.to_csv(base_dir+target+"_combined_results_my_data.csv")
 
    
 
# get mapping from byte addresses to line numbers
benchmark_byteAddress_to_lineno=get_byteAddr_to_line_number(batin_dir+benchmark_batin_csv)
    
for idx,base_dir in enumerate( base_dirs):
    # combine each tool data to the data containing benchmark vulnerabilities
    df_combined=combine_tool_results(base_dir, base_dir+benchmark_vul_csv,tools,targets[idx])
    
    # find target vulnerabilities
    find_target_vulnerabilities(df_combined,base_dir,targets[idx],target_vulnerability_indices)
    