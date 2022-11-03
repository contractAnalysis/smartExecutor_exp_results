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
# get data from collected results for timeout 1800s and 900s
# Mythril vs Phase 1 of SmartExecutor
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

# mark='mythril_vs_smartExecutor_phase1_'

cases=['mythril_vs_smartExecutor_phase1','mythril_vs_smartExecutor']
targets=['1800s_1st','1800s_2nd','1800s_3rd','900s_1st','900s_2nd','900s_3rd'] 
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

def get_general_data(tool:str,base_dir:str):
    total_contracts=0
    total_time=0
    total_bugs=0
    
    count_filtered_out=0
    count_left=0
    count_time=0
    count_bugs=0
    count_states=0
   
    results_csv=tool+"_results.csv"
    df_results=pd.read_csv(base_dir+results_csv)
    total_contracts=df_results.shape[0]
    
    columns_needed=['solidity','solc','contract','time','num_states','cov_2','vulnerability']
    df_results_needed=df_results[columns_needed]
    

    df_results_needed['num_states']=df_results_needed.apply(lambda x: convert_integer(x.num_states,x.solidity), axis=1)     
    df_results_needed['time']=df_results_needed.apply(lambda x: float(x.time), axis=1)
    df_results_needed['cov_2']=df_results_needed.apply(lambda x: convert_coverage_float(x.cov_2,x.solidity), axis=1)
   
    # count number of vulnerabilities
    df_results_needed['vulnerability']=df_results_needed.apply(lambda x: helper.get_num_vul(x.vulnerability), axis=1)
    
    total_time=df_results_needed['time'].sum()/3600
    total_bugs=df_results_needed['vulnerability'].sum()
    
    # filter out contracts that have no coverage or have three coverage data items(marked by -1 as the value for coverage)
    df_results_left=df_results_needed[df_results_needed['cov_2']>0]
    df_results_left.to_csv(base_dir+tool+"_left.csv",index=False)
    
    df_results_filtered_out=df_results_needed[df_results_needed['cov_2']<=0]
    df_results_filtered_out.to_csv(base_dir+tool+"_filtered_out.csv",index=False)
    
    count_left=df_results_left.shape[0]
    count_filtered_out=df_results_filtered_out.shape[0]
    count_time=df_results_left['time'].sum()/3600
    count_bugs=df_results_left['vulnerability'].sum()
    count_ave_cov=df_results_left['cov_2'].mean()
    count_states=df_results_left['num_states'].sum()   
    return [total_contracts, total_time,total_bugs,count_filtered_out,count_left,count_time,count_states,count_bugs,count_ave_cov]



#=======================================================
# get the general data from results
#======================================================

general_data=[]
for i, base_dir in enumerate(base_dirs):
    target=targets[i]
    for index, tool in enumerate(tools):
        re=get_general_data(tool,base_dir)
        general_data.append([target+"_"+tool]+re)
df_general_data=pd.DataFrame(general_data)
columns=['tool_results','total_contracts','total_time(h)','total_bugs','#_filtered_out','#_left','total_time_left(h)','total_states','total_bugs_left','ave_cov_left']
df_general_data.columns=columns
df_general_data=df_general_data.T
df_general_data.to_csv(parent_dir+"x_general_data_from_results.csv")




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
# get the data from the same set of contracts for each run ( i.e., not on the averaged results of the three runs))
#======================================================

data_on_same_contracts=[['results','total_contracts','total_time_1','total_bugs_1','total_state_1','ave_cov_1','total_time_2','total_bugs_2','total_state_2','ave_cov_2']]
time_diff=[]
bug_diff=[]
cov_diff=[]
for i, base_dir in enumerate(base_dirs):
    target=targets[i]
    re,time,bug,cov=get_data_from_same_contracts(tools[0],tools[1],base_dir)
    data_on_same_contracts.append([target]+re)
    time_diff.append(time)
    bug_diff.append(bug)
    cov_diff.append(cov)

df_general_data_same=pd.DataFrame(data_on_same_contracts)
df_general_data_same=df_general_data_same.T
df_general_data_same.to_csv(parent_dir+"x_general_data_on_same_contracts.csv",index=False)
df_time_diff=pd.DataFrame(time_diff).T
df_bug_diff=pd.DataFrame(bug_diff).T
df_cov_diff=pd.DataFrame(cov_diff).T




#=======================================================
# combine the results for the same tool under the same timemout.
# average the results of the three runs.
#======================================================

def get_average_data(tool:str,base_dirs:list):
    assert len(base_dirs)==3
    suffix=['_x','_y','_z']
    df_combine=pd.DataFrame()
    for i in range(len(base_dirs)):
        base_dir=base_dirs[i]      
        df_results=pd.read_csv(base_dir+tool+"_left.csv")
        df_results['time']=df_results['time'].map(lambda x: float(x))
        df_results['num_states']=df_results['num_states'].map(lambda x: int(x))
        df_results['cov_2']=df_results['cov_2'].map(lambda x: float(x))
        df_results['vulnerability']=df_results['vulnerability'].map(lambda x: float(x))
        df_results.columns=['solidity','solc','contract','time'+suffix[i],'num_states'+suffix[i],'cov_2'+suffix[i],'vulnerability'+suffix[i]]
        if df_combine.empty:
            df_combine=df_results
        else:
            df_combine=df_combine.merge(df_results,on=['solidity','solc','contract'])
    df_combine['ave_time']=df_combine.apply(lambda x: helper.average([x.time_x,x.time_y,x.time_z]),axis=1)
    df_combine['ave_state']=df_combine.apply(lambda x: helper.average([x.num_states_x,x.num_states_y,x.num_states_z]),axis=1)
    df_combine['ave_bug']=df_combine.apply(lambda x: helper.average([x.vulnerability_x,x.vulnerability_y,x.vulnerability_z]),axis=1)
    df_combine['ave_cov']=df_combine.apply(lambda x: helper.average([x.cov_2_x,x.cov_2_y,x.cov_2_z]),axis=1)
    return df_combine           


timeouts=[1800,900]
timeouts_paths=[[0,3],[3,6]]
for idx,timeout in enumerate(timeouts):
    for tool in tools:
        # --------------------------------------
        # 1800s timeout
        df_data=get_average_data(tool,base_dirs[timeouts_paths[idx][0]:timeouts_paths[idx][1]])
       
        df_data.to_csv(parent_dir+tool+"_x_combined_averaged_"+str(timeout)+"s_results.csv",index=False)
       
        
 # df_data_needed=df_data[['solidity','solc','contract','ave_time','ave_state','ave_bug','ave_cov']]       



#=======================================================
# Mythril vs SmartExecutor on the same set of contracts(averaged)
#======================================================

def get_general_averaged_data(df_data:pd.DataFrame):
    total_contracts=df_data.shape[0]
    total_time_1=df_data['ave_time_x'].sum()
    total_time_2=df_data['ave_time_y'].sum()
    total_bugs_1=df_data['ave_bug_x'].sum()
    total_bugs_2=df_data['ave_bug_y'].sum()
    total_state_1=df_data['ave_state_x'].sum()
    total_state_2=df_data['ave_state_y'].sum()
    ave_cov_1=df_data['ave_cov_x'].mean()
    ave_cov_2=df_data['ave_cov_y'].mean()
    
    general_data=[total_contracts,total_time_1,total_state_1,total_bugs_1,ave_cov_1]+\
        [total_time_2,total_state_2,total_bugs_2,ave_cov_2]
    return general_data

timeouts=[1800,900]
case='mythril_vs_smartExecutor'
tools=['mythril','smartExecutor']

general_data=[['','total contracts','total_time1','total_states1','total_bugs1','avg_cov1','total_time2','total_states2','total_bugs2','avg_cov2']]
for timeout in timeouts:    
    # combine the results of the considered tools   
    df_combine=pd.DataFrame()
    for tool in tools:
        combined_csv_name=tool+"_x_combined_averaged_"+str(timeout)+"s_results.csv"
        df_data=pd.read_csv(parent_dir+combined_csv_name)
        df_data_needed=df_data[['solidity','solc','contract','ave_time','ave_state','ave_bug','ave_cov']]
    
        if df_combine.empty:
            df_combine=df_data_needed
        else:
            df_combine=df_combine.merge(df_data_needed,on=['solidity','solc','contract'])
    
    # get the data from the combined results
    df_combine.to_csv(parent_dir+case+"_x_combined_averaged_"+str(timeout)+"s_results.csv",index=False)
    re=get_general_averaged_data(df_combine)
    results_for=str(timeout)+"s results"
    general_data.append([results_for]+re)
    
df_general=pd.DataFrame(general_data)
df_general=df_general.T
df_general.to_csv(parent_dir+case+"_general_data_on_combined_averaged_data.csv",index=False)
    




#=============================================================
# plot on the difference Distributions of the four metric data series
#=============================================================

import numpy 
import random


from utils import plot_helper
import matplotlib.pyplot as plt

def plot_differences_of_metrics(target,data,ranges,ranges_key,x_labels,y_labels):
    
    colors=[(0.2, 0.4, 0.6, 0.6),'orange','green','purple']
    
    fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(8,5))
    width=0.4
    for index, ax in enumerate( axes.flatten()):    
        plot_ranges=ranges[ranges_keys[index]]   
        name=plot_helper.retrieve_names(plot_ranges)
        ticks = np.arange(len(name))  
     
        plot_data=plot_helper.count_items(data[index],plot_ranges) 
        
        y_label=y_labels[index]
        x_label=x_labels[index]       
  
      
        bars=ax.bar(ticks, plot_data, width,color=colors[index])
        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)
        ax.set_xticks(ticks)
        ax.set_xticklabels(name)
    
        if index==0:        
            ax.legend(loc='best')
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x(), yval-1, yval)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
    
    fig.tight_layout()  
    plt.savefig(parent_dir+"diff_state_time_bug_cov"+target+".pdf")  
    plt.show()
    

ranges={
        'state_diff_ranges':[['[','min',-1000,']'],['(',-1000,0,']'],['(',0,2000,']'],['(',2000,4000,']'],['(',4000,'max',']']],
        'time_diff_ranges':[['[','min',0,']'],['(',0,250,']'],['(',250,500,']'],['(',500,'max',']']],
        'bug_diff_ranges':[['[','min',-5,')'],['[',-5,0,')'],[0],['(',0,5,']'],['(',5,'max',']']],
        'cov_diff_ranges':[['[','min',-5,')'],['[',-5,0,')'],[0],['(',0,5,']'],['(',5,'max',']']],
        }

ranges_keys=['state_diff_ranges','time_diff_ranges','bug_diff_ranges','cov_diff_ranges']
y_labels=['Number of Contracts','Number of Contracts','Number of Contracts','Number of Contracts']
x_labels=['Difference in the Number of States','Time Difference (s)','Difference in the Number of Bugs','Coverage Difference (%)']



#=======================================================
# plot: Mythril vs SmartExecutor on the same set of contracts(averaged,combined)
#======================================================
timeouts=[1800,900]
case='mythril_vs_smartExecutor'

for timeout in timeouts:
    # get the differences for each metrics
    combined_csv=case+"_x_combined_averaged_"+str(timeout)+"s_results.csv"
    df_data=pd.read_csv(parent_dir+combined_csv)

    time_diff=df_data.apply(lambda x: x.ave_time_x - x.ave_time_y, axis=1).astype(float)
    bug_diff=df_data.apply(lambda x: x.ave_bug_x - x.ave_bug_y, axis=1).astype(float)
    cov_diff=df_data.apply(lambda x: x.ave_cov_x - x.ave_cov_y, axis=1).astype(float)
    state_diff=df_data.apply(lambda x: x.ave_state_x - x.ave_state_y, axis=1).astype(int)


    data=[state_diff,time_diff,bug_diff,cov_diff]
    target="_"+case+'_'+str(timeout)
    
    plot_differences_of_metrics(target,data,ranges,ranges_keys,x_labels,y_labels)






#=======================================================
# SmartExecutor vs Phase 1 of SmartExecutor on the same set of contracts(averaged)
#======================================================

def get_general_averaged_data(df_data:pd.DataFrame):
    total_contracts=df_data.shape[0]
    total_time_1=df_data['ave_time_x'].sum()
    total_time_2=df_data['ave_time_y'].sum()
    total_bugs_1=df_data['ave_bug_x'].sum()
    total_bugs_2=df_data['ave_bug_y'].sum()
    total_state_1=df_data['ave_state_x'].sum()
    total_state_2=df_data['ave_state_y'].sum()
    ave_cov_1=df_data['ave_cov_x'].mean()
    ave_cov_2=df_data['ave_cov_y'].mean()
    
    general_data=[total_contracts,total_time_1,total_state_1,total_bugs_1,ave_cov_1]+\
        [total_time_2,total_state_2,total_bugs_2,ave_cov_2]
    return general_data

timeouts=[1800,900]
case='smartExecutor_vs_smartExecutor_phase1'
tools=['smartExecutor','smartExecutor_phase1']

general_data=[['','total contracts','total_time1','total_states1','total_bugs1','avg_cov1','total_time2','total_states2','total_bugs2','avg_cov2']]
for timeout in timeouts:    
    # combine the results of the considered tools   
    df_combine=pd.DataFrame()
    for tool in tools:
        combined_csv_name=tool+"_x_combined_averaged_"+str(timeout)+"s_results.csv"
        df_data=pd.read_csv(parent_dir+combined_csv_name)
        df_data_needed=df_data[['solidity','solc','contract','ave_time','ave_state','ave_bug','ave_cov']]
    
        if df_combine.empty:
            df_combine=df_data_needed
        else:
            df_combine=df_combine.merge(df_data_needed,on=['solidity','solc','contract'])
    
    # get the data from the combined results
    df_combine.to_csv(parent_dir+case+"_x_combined_averaged_"+str(timeout)+"s_results.csv",index=False)
    re=get_general_averaged_data(df_combine)
    results_for=str(timeout)+"s results"
    general_data.append([results_for]+re)
    
df_general=pd.DataFrame(general_data)
df_general=df_general.T
df_general.to_csv(parent_dir+case+"_general_data_on_combined_averaged_data.csv",index=False)


#=======================================================
# plot: SmartExecutor vs Phase 1 of SmartExecutor on the same set of contracts(averaged,combined)
#======================================================
timeouts=[1800,900]
case='SmartExecutor_vs_smartExecutor_phase1'
for timeout in timeouts:
    # get the differences for each metrics
    combined_csv=case+"_x_combined_averaged_"+str(timeout)+"s_results.csv"
    df_data=pd.read_csv(parent_dir+combined_csv)

    time_diff=df_data.apply(lambda x: x.ave_time_x - x.ave_time_y, axis=1).astype(float)
    bug_diff=df_data.apply(lambda x: x.ave_bug_x - x.ave_bug_y, axis=1).astype(float)
    cov_diff=df_data.apply(lambda x: x.ave_cov_x - x.ave_cov_y, axis=1).astype(float)
    state_diff=df_data.apply(lambda x: x.ave_state_x - x.ave_state_y, axis=1).astype(int)


    data=[state_diff,time_diff,bug_diff,cov_diff]
    target="_"+case+'_'+str(timeout)
    
    plot_differences_of_metrics(target,data,ranges,ranges_keys,x_labels,y_labels)








#=======================================================
# Mythril vs Phase 1 of SmartExecutor on the same set of contracts(averaged)
#======================================================

def get_general_averaged_data(df_data:pd.DataFrame):
    total_contracts=df_data.shape[0]
    total_time_1=df_data['ave_time_x'].sum()
    total_time_2=df_data['ave_time_y'].sum()
    total_bugs_1=df_data['ave_bug_x'].sum()
    total_bugs_2=df_data['ave_bug_y'].sum()
    total_state_1=df_data['ave_state_x'].sum()
    total_state_2=df_data['ave_state_y'].sum()
    ave_cov_1=df_data['ave_cov_x'].mean()
    ave_cov_2=df_data['ave_cov_y'].mean()
    
    general_data=[total_contracts,total_time_1,total_state_1,total_bugs_1,ave_cov_1]+\
        [total_time_2,total_state_2,total_bugs_2,ave_cov_2]
    return general_data

timeouts=[1800,900]
case='mythril_vs_smartExecutor_phase1'
tools=['mythril','smartExecutor_phase1']

general_data=[['','total contracts','total_time1','total_states1','total_bugs1','avg_cov1','total_time2','total_states2','total_bugs2','avg_cov2']]
for timeout in timeouts:    
    # combine the results of the considered tools   
    df_combine=pd.DataFrame()
    for tool in tools:
        combined_csv_name=tool+"_x_combined_averaged_"+str(timeout)+"s_results.csv"
        df_data=pd.read_csv(parent_dir+combined_csv_name)
        df_data_needed=df_data[['solidity','solc','contract','ave_time','ave_state','ave_bug','ave_cov']]
    
        if df_combine.empty:
            df_combine=df_data_needed
        else:
            df_combine=df_combine.merge(df_data_needed,on=['solidity','solc','contract'])
    
    # get the data from the combined results
    df_combine.to_csv(parent_dir+case+"_x_combined_averaged_"+str(timeout)+"s_results.csv",index=False)
    re=get_general_averaged_data(df_combine)
    results_for=str(timeout)+"s results"
    general_data.append([results_for]+re)
    
df_general=pd.DataFrame(general_data)
df_general=df_general.T
df_general.to_csv(parent_dir+case+"_general_data_on_combined_averaged_data.csv",index=False)


#=======================================================
# plot: SmartExecutor vs Phase 1 of SmartExecutor on the same set of contracts(averaged,combined)
#======================================================
timeouts=[1800,900]
case='Mythril_vs_smartExecutor_phase1'
for timeout in timeouts:
    # get the differences for each metrics
    combined_csv=case+"_x_combined_averaged_"+str(timeout)+"s_results.csv"
    df_data=pd.read_csv(parent_dir+combined_csv)

    time_diff=df_data.apply(lambda x: x.ave_time_x - x.ave_time_y, axis=1).astype(float)
    bug_diff=df_data.apply(lambda x: x.ave_bug_x - x.ave_bug_y, axis=1).astype(float)
    cov_diff=df_data.apply(lambda x: x.ave_cov_x - x.ave_cov_y, axis=1).astype(float)
    state_diff=df_data.apply(lambda x: x.ave_state_x - x.ave_state_y, axis=1).astype(int)


    data=[state_diff,time_diff,bug_diff,cov_diff]
    target="_"+case+'_'+str(timeout)
    
    plot_differences_of_metrics(target,data,ranges,ranges_keys,x_labels,y_labels)








#=======================================================
# Mythril vs SmartExecutor vs Phase 1 of SmartExecutor on the same set of contracts(averaged)
#======================================================
def get_general_averaged_data(df_data:pd.DataFrame):
    total_contracts=df_data.shape[0]
    total_time_1=df_data['ave_time_x'].sum()
    total_time_2=df_data['ave_time_y'].sum()
    total_time_3=df_data['ave_time_z'].sum()
    total_bugs_1=df_data['ave_bug_x'].sum()
    total_bugs_2=df_data['ave_bug_y'].sum()
    total_bugs_3=df_data['ave_bug_z'].sum()
    total_state_1=df_data['ave_state_x'].sum()
    total_state_2=df_data['ave_state_y'].sum()
    total_state_3=df_data['ave_state_z'].sum()
    ave_cov_1=df_data['ave_cov_x'].mean()
    ave_cov_2=df_data['ave_cov_y'].mean()
    ave_cov_3=df_data['ave_cov_z'].mean()
    
    general_data=[total_contracts,total_time_1,total_state_1,total_bugs_1,ave_cov_1]+\
        [total_time_2,total_state_2,total_bugs_2,ave_cov_2]+\
          [total_time_3,total_state_3,total_bugs_3,ave_cov_3]
    return general_data

timeouts=[1800,900]
case='mythril_vs_smartExecutor_vs_phase1_of_smartExecutor'
tools=['mythril','smartExecutor','smartExecutor_phase1']
general_data=[['','total contracts','total_time1','total_states1','total_bugs1','avg_cov1']+\
              ['total_time2','total_states2','total_bugs2','avg_cov2']+\
                  ['total_time3','total_states3','total_bugs3','avg_cov3']
              ]

identifiers=['_x','_y','_z']
for timeout in timeouts:
    # combine the results of the considered tools   
    df_combine=pd.DataFrame()
    for idx,tool in enumerate(tools):
        combined_csv_name=tool+"_x_combined_averaged_"+str(timeout)+"s_results.csv"
        df_data=pd.read_csv(parent_dir+combined_csv_name)
        df_data_needed=df_data[['solidity','solc','contract','ave_time','ave_state','ave_bug','ave_cov']]
        # change the column names
        df_data_needed.columns=['solidity','solc','contract','ave_time'+identifiers[idx],'ave_state'+identifiers[idx],'ave_bug'+identifiers[idx],'ave_cov'+identifiers[idx]]
    
        if df_combine.empty:
            df_combine=df_data_needed
        else:
            df_combine=df_combine.merge(df_data_needed,on=['solidity','solc','contract'])
    
    df_combine.to_csv(parent_dir+case+"_x_combined_averaged_"+str(timeout)+"s_results.csv",index=False)
    
    # get the data from the combined results
    df_combine.to_csv(parent_dir+case+"_x_combined_averaged_"+str(timeout)+"s_results.csv",index=False)
    re=get_general_averaged_data(df_combine)
    results_for=str(timeout)+"s results"
    general_data.append([results_for]+re)    

df_general=pd.DataFrame(general_data)
df_general=df_general.T
df_general.to_csv(parent_dir+case+"_general_data_on_combined_averaged_data.csv",index=False)
    



