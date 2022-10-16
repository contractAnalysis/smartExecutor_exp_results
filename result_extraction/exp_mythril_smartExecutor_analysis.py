# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 16:29:28 2022

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

import pandas as pd
sys.path.append(root) # the project path on Windows

from result_extraction import raw_result_extraction
from utils import helper

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
# collect all results for timeout 1800s and 900s
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
# targets=['1800s_1st','1800s_2nd','1800s_3rd','900s_1st','900s_2nd','900s_3rd'] 
# tools=['mythril','smartExecutor_phase1']

mark='mythril_vs_smartExecutor_'
targets=['1800s_1st','1800s_2nd','1800s_3rd','900s_1st','900s_2nd','900s_3rd'] 
tools=['mythril','smartExecutor']


# # --------------------------------------
# # get the general data from results
# general_data=[]
# for i, base_dir in enumerate(base_dirs):
#     target=targets[i]
#     for index, tool in enumerate(tools):
#         re=get_general_data(tool,base_dir)
#         general_data.append([target+"_"+tool]+re)

# df_general_data=pd.DataFrame(general_data)
# columns=['tool_results','total_contracts','total_time(h)','total_bugs','#_filtered_out','#_left','total_time_left(h)','total_states','total_bugs_left','ave_cov_left']
# df_general_data.columns=columns
# df_general_data=df_general_data.T
# df_general_data.to_csv(parent_dir+mark+"general_data_from_results.csv")





# # --------------------------------------
# # get the data from the same set of contracts
# data_on_same_contracts=[['results','total_contracts','total_time_1','total_bugs_1','total_state_1','ave_cov_1','total_time_2','total_bugs_2','total_state_2','ave_cov_2']]
# time_diff=[]
# bug_diff=[]
# cov_diff=[]
# for i, base_dir in enumerate(base_dirs):
#     target=targets[i]
#     re,time,bug,cov=get_data_from_same_contracts(tools[0],tools[1],base_dir)
#     data_on_same_contracts.append([target]+re)
#     time_diff.append(time)
#     bug_diff.append(bug)
#     cov_diff.append(cov)

# df_general_data_same=pd.DataFrame(data_on_same_contracts)
# df_general_data_same=df_general_data_same.T
# df_general_data_same.to_csv(parent_dir+mark+"general_data_on_same_contracts.csv",index=False)
# df_time_diff=pd.DataFrame(time_diff).T
# df_bug_diff=pd.DataFrame(bug_diff).T
# df_cov_diff=pd.DataFrame(cov_diff).T




# --------------------------------------
# combine the results for the same tool under the same timemout
# get the average for time,state, coverage, and bug
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


# --------------------------------------
# 1800s timeout
df_mythril_1800s=get_average_data(tools[0],base_dirs[0:3])
df_mythril_1800s.to_csv(parent_dir+tools[0]+"_1800s_results.csv",index=False)

df_smartExecutor_1800s=get_average_data(tools[1],base_dirs[0:3]) 
df_smartExecutor_1800s.to_csv(parent_dir+tools[1]+"_1800s_results.csv",index=False) 

df_mythril_1800s_needed=df_mythril_1800s[['solidity','solc','contract','ave_time','ave_state','ave_bug','ave_cov']]
df_smartExecutor_1800s_needed=df_smartExecutor_1800s[['solidity','solc','contract','ave_time','ave_state','ave_bug','ave_cov']]

df_mythril_1800s_needed.columns=['solidity','solc','contract','ave_time_x','ave_state_x','ave_bug_x','ave_cov_x']
df_smartExecutor_1800s_needed.columns=['solidity','solc','contract','ave_time_y','ave_state_y','ave_bug_y','ave_cov_y']

df_averaged_1800s=df_mythril_1800s_needed.merge(df_smartExecutor_1800s_needed,on=['solidity','solc','contract'])
df_averaged_1800s.to_csv(parent_dir+mark+'averaged_results_1800s_same_contracts.csv')



# --------------------------------------
# 900s timeout  
df_mythril_900s=get_average_data(tools[0],base_dirs[3:6])
df_mythril_900s.to_csv(parent_dir+tools[0]+"_900s_results.csv",index=False)  
    
df_smartExecutor_900s=get_average_data(tools[1],base_dirs[3:6])
df_smartExecutor_900s.to_csv(parent_dir+tools[1]+"_900s_results.csv",index=False)

df_mythril_900s_needed=df_mythril_900s[['solidity','solc','contract','ave_time','ave_state','ave_bug','ave_cov']]
df_smartExecutor_900s_needed=df_smartExecutor_900s[['solidity','solc','contract','ave_time','ave_state','ave_bug','ave_cov']]

df_mythril_900s_needed.columns=['solidity','solc','contract','ave_time_x','ave_state_x','ave_bug_x','ave_cov_x']
df_smartExecutor_900s_needed.columns=['solidity','solc','contract','ave_time_y','ave_state_y','ave_bug_y','ave_cov_y']

df_averaged_900s=df_mythril_900s_needed.merge(df_smartExecutor_900s_needed,on=['solidity','solc','contract'])
df_averaged_900s.to_csv(parent_dir+mark+'averaged_results_900s_same_contracts.csv')
        

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
    time_diff=df_data.apply(lambda x: x.ave_time_x - x.ave_time_y, axis=1).astype(float)
    bug_diff=df_data.apply(lambda x: x.ave_bug_x - x.ave_bug_y, axis=1).astype(float)
    cov_diff=df_data.apply(lambda x: x.ave_cov_x - x.ave_cov_y, axis=1).astype(float)
    state_diff=df_data.apply(lambda x: x.ave_state_x - x.ave_state_y, axis=1).astype(int)
    
    general_data=[total_contracts,total_time_1,total_state_1,total_bugs_1,ave_cov_1]+\
        [total_time_2,total_state_2,total_bugs_2,ave_cov_2]
    return general_data,time_diff,bug_diff,cov_diff,state_diff

general_data_1800s,time_diff_1800s,bug_diff_1800s,cov_diff_1800s,state_diff_1800s=get_general_averaged_data(df_averaged_1800s)
general_data_900s,time_diff_900s,bug_diff_900s,cov_diff_900s,state_diff_900s=get_general_averaged_data(df_averaged_900s)




# import numpy 

# import random
# import numpy
# from matplotlib import pyplot
# from utils import plot_helper


# import matplotlib.pyplot as plt



# ranges={
#         'state_diff_ranges':[['[','min',-1000,']'],['(',-1000,0,']'],['(',0,2000,']'],['(',2000,4000,']'],['(',4000,'max',']']],
#         'time_diff_ranges':[['[','min',0,']'],['(',0,250,']'],['(',250,500,']'],['(',500,'max',']']],
#         'bug_diff_ranges':[['[','min',-5,')'],['[',-5,0,')'],[0],['(',0,5,']'],['(',5,'max',']']],
#         'cov_diff_ranges':[['[','min',-5,')'],['[',-5,0,')'],[0],['(',0,5,']'],['(',5,'max',']']],
#         }

# ranges_keys=['state_diff_ranges','time_diff_ranges','bug_diff_ranges','cov_diff_ranges']
# y_labels=['Number of Contracts','Number of Contracts','Number of Contracts','Number of Contracts']
# x_labels=['Difference of the Number of States','Time Difference (s)','Difference of the Number of Bugs','Coverage Difference (%)']

# data_1800s=[state_diff_1800s,time_diff_1800s,bug_diff_1800s,cov_diff_1800s  ]
# data_900s=[state_diff_900s,time_diff_900s,bug_diff_900s,cov_diff_900s  ]

# labels_900s=['900s timeout','900s timeout','900s timeout','900s timeout']
# labels=['1800s timeout','1800s timeout', '1800s timeout','1800s timeout']
# colors=[(0.2, 0.4, 0.6, 0.6),'orange','green','purple']

# # # fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
# # fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(7.5,6))

# # ax0, ax1, ax2, ax3 = axes.flatten()

# # # ax1.plot(range(10), 'r')
# # # ax1 = fig.add_axes([left, bottom, width, height]) 
# # width=0.4


# # # left, bottom, width, height = 0.1, 0.3, 0.8, 0.6
# # # ax = fig.add_axes([left, bottom, width, height]) 

# # for index, ax in enumerate( axes.flatten()):
    
# #     plot_ranges=ranges[ranges_keys[index]]
   
# #     name=plot_helper.retrieve_names(plot_ranges)
# #     plot_data_900s=plot_helper.count_items(data_900s[index],plot_ranges)
# #     plot_data_1800s=plot_helper.count_items(data_1800s[index],plot_ranges)    
# #     y_label=y_labels[index]
# #     x_label=x_labels[index]
    
# #     ticks = np.arange(len(name))    
# #     bars_900s=ax.bar(ticks, plot_data_900s, width,label=labels_900s[index])
# #     bars=ax.bar(ticks + width, plot_data_1800s, width,label=labels[index])
# #     ax.set_ylabel(y_label)
# #     ax.set_xlabel(x_label)
# #     ax.set_xticks(ticks)
# #     ax.set_xticklabels(name)
# #     # ax.set_xticks(ticks + width/2)
# #     if index==0:        
# #         ax.legend(loc='best')
# #     for bar in bars:
# #         yval = bar.get_height()
# #         ax.text(bar.get_x(), yval + 1, yval)
# #     for bar in bars_900s:
# #         yval = bar.get_height()
# #         ax.text(bar.get_x(), yval + 1, yval)

# # fig.tight_layout()  
# # plt.savefig(parent_dir+"diff_state_time_bug_cov.pdf")  
# # plt.show()



# data_to_be_ploted=[data_900s,data_1800s]
# target=['_900s','_1800s']
# for i,data in enumerate( data_to_be_ploted):

#     fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(8,5))
#     width=0.4
#     for index, ax in enumerate( axes.flatten()):    
#         plot_ranges=ranges[ranges_keys[index]]   
#         name=plot_helper.retrieve_names(plot_ranges)
#         ticks = np.arange(len(name))  
     
#         plot_data_1800s=plot_helper.count_items(data[index],plot_ranges) 
        
#         y_label=y_labels[index]
#         x_label=x_labels[index]       
  
      
#         bars=ax.bar(ticks, plot_data_1800s, width,color=colors[index])
#         ax.set_ylabel(y_label)
#         ax.set_xlabel(x_label)
#         ax.set_xticks(ticks)
#         ax.set_xticklabels(name)
    
#         if index==0:        
#             ax.legend(loc='best')
#         for bar in bars:
#             yval = bar.get_height()
#             ax.text(bar.get_x(), yval-1, yval)
#         ax.spines['right'].set_visible(False)
#         ax.spines['top'].set_visible(False)
    
#     fig.tight_layout()  
#     plt.savefig(parent_dir+"diff_state_time_bug_cov"+target[i]+".pdf")  
#     plt.show()

