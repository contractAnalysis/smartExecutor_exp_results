# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 22:13:28 2022

@author: 18178
"""

import matplotlib.pyplot as plt
import numpy as np

#=========================================================================
# plot one dataset with bar chart
# plot execution time for SB benchmark
data = [10,7,50]
names=['Mythril','SmartExecutor','Smartian']
y_label='Total Time (h)'

fig = plt.figure(figsize=(5,3), dpi=200)
left, bottom, width, height = 0.1, 0.1, 0.85, 0.85
ax = fig.add_axes([left, bottom, width, height]) 
 
width = 0.35   
ticks = np.arange(len(names))    
bars=ax.bar(ticks, data, width)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x()+width/3, yval+width/3, yval)

ax.set_ylabel(y_label)
ax.set_xticks(ticks)
ax.set_xticklabels(names)
fig.tight_layout
plt.savefig('C:\\22_summer_exp\\exp_benchmark\\SB\IB_RE_ULC\\1800s_results\\'+"exp_benchmark_SB_IB_RE_ULC_execution_time.pdf")
plt.show()


#=========================================================================
# # plot three datasets with bar chart
# # plot execution time for SB benchmark
data0=[9.924800421,6.781670429,50.0284007]
data1=[9.785350039,6.767505587,50.02925239]
data2=[9.790555944,6.709767567,50.02991652]


names=['Mythril','SmartExecutor','Smartian']
y_label='Total Time (h)'

fig = plt.figure(figsize=(5,3), dpi=200)
left, bottom, width, height = 0.1, 0.1, 0.85, 0.85
ax = fig.add_axes([left, bottom, width, height]) 
 
width = 0.35   
ticks = np.arange(len(names))    
ax.bar(ticks, data0, width)
ax.bar(ticks+ width, data1, width)
ax.bar(ticks+ width+ width,data2, width)

ax.set_ylabel(y_label)
ax.set_xticks(ticks + width)
ax.set_xticklabels(names)
fig.tight_layout
plt.savefig('C:\\22_summer_exp\\exp_benchmark\\SB\IB_RE_ULC\\1800s_results\\'+"exp_benchmark_SB_IB_RE_ULC_3_execution_time.pdf")
plt.show()










#=========================================================================
# plot two datasets with bar chart

gaussian_numbers = np.random.normal(size=10000)

plt.hist(gaussian_numbers)
plt.title("Gaussian Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()



#=========================================================================
last_week_cups = (20, 35, 30, 35, 27)
this_week_cups = (25, 32, 34, 20, 25)
names = ['Mary', 'Paul', 'Billy', 'Franka', 'Stephan']

fig = plt.figure(figsize=(6,5), dpi=200)
left, bottom, width, height = 0.1, 0.3, 0.8, 0.6
ax = fig.add_axes([left, bottom, width, height]) 
 
width = 0.35   
ticks = np.arange(len(names))    
ax.bar(ticks, last_week_cups, width, label='Last week')
ax.bar(ticks + width, this_week_cups, width, align="center",
    label='This week')

ax.set_ylabel('Cups of Coffee')
ax.set_title('Coffee Consummation')
ax.set_xticks(ticks + width/2)
ax.set_xticklabels(names)

ax.legend(loc='best')
plt.show()




#=========================================================================
import random
import numpy
from matplotlib import pyplot

x = [random.gauss(3,1) for _ in range(400)]
y = [random.gauss(4,2) for _ in range(400)]

bins = numpy.linspace(-10, 10, 100)

pyplot.hist(x, bins, alpha=0.5, label='x')
pyplot.hist(y, bins, alpha=0.5, label='y')
pyplot.legend(loc='upper right')
pyplot.show()