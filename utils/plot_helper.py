# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 22:29:09 2022

@author: 18178
"""

import math

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])




ranges=[['[','min',-10,']'],['(',-10,-5,']'],['(',-5,0,')'],[0],['(',0,5,']'],['(',5,10,']'],['(',10,'max',']']]

time_diff_ranges=[['[','min',-250,']'],['(',-250,0,']'],['(',0,250,']'],['(',250,500,']'],['(',500,'max',']']]
state_diff_ranges=[['[','min',-250,']'],['(',-250,0,']'],['(',0,250,']'],['(',250,500,']'],['(',500,'max',']']]
cov_diff_ranges=[['[','min',-5,')'],['[',-5,0,')'],[0],['(',0,5,']'],['(',5,'max',']']]
bug_diff_ranges=[['[','min',-5,')'],['[',-5,0,')'],[0],['(',0,5,']'],['(',5,'max',']']]

def retrieve_names_0(ranges:list):
    names=[]
    for item in ranges:
        if len(item)==1:
            names.append(f'{item[0]}')           
        elif len(item)==4:
            if isinstance(item[1],int) and abs(item[1])>=500:                
                item1=f"{item[1] // 1000:,}K" 
            else: item1=item[1]
            if  isinstance(item[2],int) and abs(item[2])>=500:
                item2=f"{item[2] // 1000:,}K"
            else:item2=item[2]
            # names.append(f'{item[0]}{item[1]},{item[2]}{item[3]}')
            names.append(f'{item[0]}{item1},{item2}{item[3]}')   
        else:
            pass
    return names

def retrieve_names(ranges:list):
    names=[]
    for item in ranges:
        if len(item)==1:
            names.append(f'{human_format(item[0])}')           
        elif len(item)==4:
            if isinstance(item[1],int) and abs(item[1])>=500:                
                item1=human_format(item[1]) 
            else: item1=item[1]
            if  isinstance(item[2],int) and abs(item[2])>=500:
                item2=human_format(item[2])
            else:item2=item[2]
            # names.append(f'{item[0]}{item[1]},{item[2]}{item[3]}')
            names.append(f'{item[0]}{item1},{item2}{item[3]}')   
        else:
            pass
    return names

def count_items(data:list,ranges:list):
    counts=[]
    min_item=min(data)
    max_item=max(data)
    left=0
    right=0
    for item_range in ranges:
        if len(item_range)==1:
            number=len([item for item in data if item==item_range[0]])
            counts.append(number)
            
        elif len(item_range)==4:
            
            if item_range[1]=='min':
                left=min_item
            else:
                left=item_range[1]

            if item_range[2]=='max':
                 right=max_item
            else:
                right=item_range[2]            
            if item_range[0]=="(" and item_range[3]==')':
                number=len([item for item in data if item>left and item< right])
            elif item_range[0]=="(" and item_range[3]==']':
                number=len([item for item in data if item>left and item<= right])
            elif item_range[0]=="[" and item_range[3]==')':
                number=len([item for item in data if item>=left and item< right])                
            elif item_range[0]=="[" and item_range[3]==']':
                number=len([item for item in data if item>=left and item<= right])
            counts.append(number)
    return counts

print(retrieve_names(ranges))
# x=range(-5,20)
# print(count_items(x,ranges))
# print(count_items(x,state_diff_ranges))
# print(count_items(x,time_diff_ranges))
# print(count_items(x,cov_diff_ranges))
print(retrieve_names(state_diff_ranges))
print(retrieve_names(time_diff_ranges))
print(retrieve_names(cov_diff_ranges))
print(retrieve_names(bug_diff_ranges))

