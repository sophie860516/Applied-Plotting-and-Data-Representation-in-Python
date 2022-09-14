
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

get_ipython().magic('matplotlib notebook')
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    
    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[2]:

weather = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
weather.head()


# In[3]:


weather['Date'] = pd.to_datetime(weather['Date'])
weather.set_index('Date')


weather05_14 = weather.copy()
weather05_14 = weather05_14[(weather05_14.Date >='2005-01-01')& (weather05_14.Date <='2014-12-31')]
weather05_14 = weather05_14[~((weather05_14.Date.dt.month == 2)&(weather05_14.Date.dt.day==29))]
weather05_14['Date'] = weather05_14['Date'].dt.strftime('%m-%d')
weather05_14['Data_Value'] = weather05_14['Data_Value']*0.1
weather05_14.head()


# In[4]:

weather2015 = weather.copy()
weather2015 = weather2015[(weather2015.Date >='2015-01-01')& (weather2015.Date <='2015-12-31')]
weather2015 = weather2015[~((weather2015.Date.dt.month == 2)&(weather2015.Date.dt.day==29))]
weather2015['Date'] = weather2015['Date'].dt.strftime('%m-%d')
weather2015['Data_Value'] = weather2015['Data_Value']*0.1

dfmax2015 = weather2015.groupby('Date').max()
dfmin2015 = weather2015.groupby('Date').min()

dfmax2015.index = pd.to_datetime(dfmax2015.index,format='%m-%d')
dfmin2015.index = pd.to_datetime(dfmin2015.index,format='%m-%d')

dfmax2015


# In[5]:

dfmin05_14 = weather05_14.groupby('Date').min()
dfmax05_14 = weather05_14.groupby('Date').max()



# In[6]:

dfmax05_14.index = pd.to_datetime(dfmax05_14.index,format='%m-%d')
dfmin05_14.index = pd.to_datetime(dfmax05_14.index,format='%m-%d')


# In[7]:

Max_merged = pd.merge(dfmax05_14,dfmax2015,how = 'outer',left_index = True,right_index=True)

#Max_merged['max_val'] = Max_merged[['Data_Value_x','Data_Value_y']].max(axis=1)
Max_merged.drop(['ID_x','ID_y','Element_x','Element_y'],axis=1)
def max_val(x):
    if (x['Data_Value_y']>x['Data_Value_x']):
        return x['Data_Value_y'] 
Max_merged['max_val'] = Max_merged.apply(max_val,axis=1)


# In[8]:

Min_merged = pd.merge(dfmin05_14,dfmin2015,how = 'outer',left_index = True,right_index=True)

#Min_merged['min_val'] = Min_merged[['Data_Value_x','Data_Value_y']].min(axis=1)
Min_merged.drop(['ID_x','ID_y','Element_x','Element_y'],axis=1)
def min_val(x):
    if (x['Data_Value_y']<x['Data_Value_x']):
        return x['Data_Value_y'] 
Min_merged['min_val'] = Min_merged.apply(min_val,axis=1)


# In[57]:

import matplotlib.dates as mdates
plt.figure(figsize=(8, 5))
line_min,= plt.plot(dfmin05_14.index,dfmin05_14['Data_Value'],'-',label = 'Min temp 2005-2014',linewidth=1)
line_max, = plt.plot(dfmin05_14.index,dfmax05_14['Data_Value'],'-',label = 'Max temp 2005-2014',linewidth=1)
dotmax, = plt.plot(dfmin05_14.index,Max_merged['max_val'].values,color='red', marker='o',markersize=3,label = 'Extreme Max 2015',linestyle='None')
dotmin, = plt.plot(dfmin05_14.index,Min_merged['min_val'].values,color='red', marker='o',markersize=3,label = 'Extreme Min 2015',linestyle='None')
ax=plt.gca()
myFmt = mdates.DateFormatter('%b')
myFmt2 = plt.FormatStrFormatter('%d $^\circ$C')
myFmt3 = plt.FormatStrFormatter('%d $^\circ$F')
months = mdates.MonthLocator()
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(myFmt)
ax.yaxis.set_major_formatter(myFmt2)
#setting Farh. y-axis
ax2 = ax.twinx()
T_f = lambda T_c: T_c*1.8 + 32
ymin, ymax = ax.get_ylim()
ax2.set_ylim((T_f(ymin),T_f(ymax)))
ax2.plot([],[])
ax2.yaxis.set_major_formatter(myFmt3)
plt.grid()
ax.fill_between(dfmin05_14.index, dfmin05_14['Data_Value'],dfmax05_14['Data_Value'],facecolor='grey', alpha=0.2)

#for spine in ax.spines.values():
 #   spine.set_visible(False)

plt.title('Ann Arbor, Michigan, United States',fontsize=10)
plt.suptitle('Daily Historical High & Low over 2005-2014 and Breaking Points in 2015' )
#plt.ylabel('Temperature')
ax.set_ylabel("Temperature [Celsius]")
ax2.set_ylabel("Temperature [Fahrenheit]")
ax.set_xlabel('Months')
#plt.legend([line_plot,dotmax,dotmin],['Min temp 2005-2014', 'Max temp 2005-2014','Extreme Max 2015','Extreme min 2015'])
plt.legend(handles=[line_min,line_max,dotmax,dotmin],loc ='lower center',bbox_to_anchor=(0.65, 0.02))


plt.rcParams['savefig.facecolor']='white'
plt.rcParams['axes.facecolor']='white'
plt.savefig('hw2.png')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[44]:




# In[ ]:



