
# coding: utf-8

# # Assignment 4
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# This assignment requires that you to find **at least** two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of **weather phenomena** (see below) for the region of **Longueuil, Quebec, Canada**, or **Canada** more broadly.
# 
# You can merge these datasets with data from different regions if you like! For instance, you might want to compare **Longueuil, Quebec, Canada** to Ann Arbor, USA. In that case at least one source file must be about **Longueuil, Quebec, Canada**.
# 
# You are welcome to choose datasets at your discretion, but keep in mind **they will be shared with your peers**, so choose appropriate datasets. Sensitive, confidential, illicit, and proprietary materials are not good choices for datasets for this assignment. You are welcome to upload datasets of your own as well, and link to them using a third party repository such as github, bitbucket, pastebin, etc. Please be aware of the Coursera terms of service with respect to intellectual property.
# 
# Also, you are welcome to preserve data in its original language, but for the purposes of grading you should provide english translations. You are welcome to provide multiple visuals in different languages if you would like!
# 
# As this assignment is for the whole course, you must incorporate principles discussed in the first week, such as having as high data-ink ratio (Tufte) and aligning with Cairo’s principles of truth, beauty, function, and insight.
# 
# Here are the assignment instructions:
# 
#  * State the region and the domain category that your data sets are about (e.g., **Longueuil, Quebec, Canada** and **weather phenomena**).
#  * You must state a question about the domain category and region that you identified as being interesting.
#  * You must provide at least two links to available datasets. These could be links to files such as CSV or Excel files, or links to websites which might have data in tabular form, such as Wikipedia pages.
#  * You must upload an image which addresses the research question you stated. In addition to addressing the question, this visual should follow Cairo's principles of truthfulness, functionality, beauty, and insightfulness.
#  * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.
# 
# What do we mean by **weather phenomena**?  For this category you might want to consider seasonal changes, natural disasters, or historical trends.
# 
# ## Tips
# * Wikipedia is an excellent source of data, and I strongly encourage you to explore it for new data sources.
# * Many governments run open data initiatives at the city, region, and country levels, and these are wonderful resources for localized data sources.
# * Several international agencies, such as the [United Nations](http://data.un.org/), the [World Bank](http://data.worldbank.org/), the [Global Open Data Index](http://index.okfn.org/place/) are other great places to look for data.
# * This assignment requires you to convert and clean datafiles. Check out the discussion forums for tips on how to do this from various sources, and share your successes with your fellow students!
# 
# ## Example
# Looking for an example? Here's what our course assistant put together for the **Ann Arbor, MI, USA** area using **sports and athletics** as the topic. [Example Solution File](./readonly/Assignment4_example.pdf)

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns

get_ipython().magic('matplotlib notebook')


# In[2]:

NYC = pd.read_csv('NYCITY_weather.csv')
clean_NYC = NYC.copy()
clean_NYC = clean_NYC[['NAME','DATE','TMAX','TMIN']]
clean_NYC.ffill(inplace = True)
#clean_NYC.isnull().sum() #checking NaN value

#REMOVE LEAP YEAR
clean_NYC['DATE'] = pd.to_datetime(clean_NYC['DATE'])
clean_NYC = clean_NYC[~((clean_NYC.DATE.dt.month == 2)&(clean_NYC.DATE.dt.day==29))]


# In[3]:

MTL = pd.read_csv('MTL_weather.csv')
AUT = MTL.copy().iloc[0:3879]
AUT = AUT[['NAME','DATE','TMAX','TMIN']]

AUT.ffill(inplace=True)
#AUT.isnull().sum()

#REMOVE LEAP YEAR
AUT['DATE'] = pd.to_datetime(AUT['DATE'])
AUT = AUT[~((AUT.DATE.dt.month == 2)&(AUT.DATE.dt.day==29))]


# In[4]:

merged_max = AUT.merge(clean_NYC,on='DATE',how='inner')
merged_max = merged_max.drop(['TMIN_x','TMIN_y'],axis=1)
merged_max['DATE'] = pd.to_datetime(merged_max['DATE'],format='%y-%m-%d')
#merged_max.set_index('DATE',inplace=True)

merged_min = AUT.merge(clean_NYC,on='DATE',how='inner')
merged_min = merged_min.drop(['TMAX_x','TMAX_y'],axis=1)
#merged_min.set_index('DATE')


# In[86]:

import matplotlib.dates as mdates
fig, axs = plt.subplots(3,1,sharex=True,sharey='all',figsize=(8,6))
plt.subplots_adjust(hspace=0.3, wspace=0.75)
ax1 = plt.subplot(2,1,1)
Max_NYC, = ax1.plot(merged_max['DATE'],merged_max['TMAX_x'],c='red',alpha=0.7,label='Max MTL',linewidth=0.7)
Max_MTL, = ax1.plot(merged_max['DATE'],merged_max['TMAX_y'],c='blue',alpha =0.8,label='Max NYC',linewidth=0.7)



ax2 = plt.subplot(2,1,2)
Min_MTL, = ax2.plot(merged_min['DATE'],merged_min['TMIN_x'],c='orange',label='Min MTL',linewidth=0.7,alpha=0.6)
Min_NYC, = ax2.plot(merged_min['DATE'],merged_min['TMIN_y'],c='darkblue',label='Min NYC',linewidth=0.7,alpha=0.8)


#set x-ticks to month by January and July
months = mdates.MonthLocator(bymonth=(1,7))
myFmt = mdates.DateFormatter('%Y-%b')
myFmt2 = plt.FormatStrFormatter('%d $^\circ$C')
myFmt3 = plt.FormatStrFormatter('%d $^\circ$F')
ax1.xaxis.set_major_locator(months)
ax1.xaxis.set_major_formatter(myFmt)
ax1.yaxis.set_major_formatter(myFmt3)
ax2.xaxis.set_major_locator(months)
ax2.xaxis.set_major_formatter(myFmt)
ax2.set_yticks((-50,-25,0,25,50,75))
ax2.yaxis.set_major_formatter(myFmt3)

#add F-yaxis
#ax1_1 = ax1.twinx()
#T_f = lambda T_c: T_c*1.8 + 32
#ymin, ymax = ax1.get_ylim()
#ax1_1.plot([],[])
#ax1_1.set_ylim((T_f(ymin),T_f(ymax)))
#ax1_1.yaxis.set_major_formatter(myFmt3)

#ax2_1 = ax2.twinx()
#ymin_ax2,ymax_ax2=ax2.get_ylim()
#ax2_1.plot([],[])
#ax2_1.set_ylim((T_f(ymin),T_f(ymax)))
#ax2_1.yaxis.set_major_formatter(myFmt3)


#adjust xtick labels
ax1.set_xticklabels([]) #remove labels but keep the ticks
ax2.tick_params(labelsize=9) #adjust size to avoid incomplete labels
for label in ax2.get_xticklabels():
    label.set_ha("right")
    label.set_rotation(32)
    
#remove first and last tick label
plt.setp(ax2.get_xticklabels()[0], visible=False)
plt.setp(ax2.get_xticklabels()[-1], visible=False)

#change plot background color
ax1.set_facecolor('xkcd:powder blue')
ax1.patch.set_alpha(0.3)
ax2.set_facecolor('xkcd:powder blue')
ax2.patch.set_alpha(0.3)



plt.suptitle('Temparature Compairison between Montreal and NYC from 2005 to 2016')
ax1.set_title('Max Temperature')
ax2.set_title('Min Temperature')

ax1.legend(handles=[Max_NYC,Max_MTL,],bbox_to_anchor=(0.9, 0.25),prop=dict(size=7))
ax2.legend(handles=[Min_MTL,Min_NYC,],bbox_to_anchor=(1.03, 0.25),prop=dict(size=7))                                                     
ax1.grid(axis='y')
ax2.grid(axis='y')
#for i in range(2):
#    axs[i].spines['top'].set_visible(False)
#    axs[i].spines['right'].set_visible(False)
#remove spines on top and right
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
#ax1.spines['left'].set_visible(False)
#ax1.spines['bottom'].set_visible(False)

#interactivity not working
#def onclick(event):
#    y= event.ydata
#    plt.gca().set_title('you press {}'.format(event.data))
    #y_text = plt.text(1.5, 55000, 'y = %d' % y, bbox=dict(fc='white', ec='k'))
#plt.gcf().canvas.mpl_connect('botton_press_event', onclick);

plt.savefig('hw4.png')


# In[ ]:



