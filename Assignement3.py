
# coding: utf-8

# In[3]:

# Use the following data for this assignment:
get_ipython().magic('matplotlib notebook')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.cm import ScalarMappable


df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

err_1992 = np.std(df.iloc[0])/np.sqrt(3650)#standard error for 1992
mean_1992 = np.mean(df.iloc[0])
err_1993 = np.std(df.iloc[1])/np.sqrt(3650)#standard error for 1993
mean_1993 = np.mean(df.iloc[1])
err_1994 = np.std(df.iloc[2])/np.sqrt(3650)#standard error for 1994
mean_1994 = np.mean(df.iloc[2])
err_1995 = np.std(df.iloc[3])/np.sqrt(3650)#standard error for 1995
mean_1995 = np.mean(df.iloc[3])
errs = [err_1992,err_1993,err_1994,err_1995]

df['mean']=df.mean(axis=1)

#means=[]
#for i in range(4):
#    means.append(df.iloc[i]['mean'])
df


# In[51]:

import scipy.stats as st
y=42134

fig,ax=plt.subplots(figsize=(6,8))
cmap =  plt.get_cmap('RdBu')
norm = mpl.colors.Normalize()
colors = cmap(norm((df['mean'] - df['mean'].mean())/df['mean'].std()))
#colors = cmap(st.norm.cdf(df['mean']/df['mean']))
#cmap =  plt.get_cmap('RdBu')
my_plot = ax.bar(df.index,df['mean'],yerr=errs,width=0.99,capsize=6,linewidth=6,color=colors,ecolor='gray')

plt.xticks(df.index,['1992','1993','1994','1995'])
plt.xlabel('Year')
plt.ylabel('Sample Mean with 95% CI')
plt.axhline(y=df['mean'].mean(), color='r', linestyle='-.', linewidth=3, label='Mean of four years')
ax.text(1990.8,42500, "42012", va='center', ha="left", bbox=dict(facecolor="w",alpha=0.5),transform=ax.transData)
anarray = mpl.cm.ScalarMappable(norm = norm,cmap =cmap)
anarray.set_array([])
#plt.legend()
fig.colorbar(anarray,orientation='horizontal')
#plt.savefig('hw3.png')

def onclick(event):
    y = event.ydata
    hoz_line.set_ydata(event.ydata)
    yt = np.append(yt_o, y)
    plt.gca().set_yticks(yt)
    y_text = plt.text(1.5, 55000, 'y = %d' % y, bbox=dict(fc='white', ec='k'))

    probs = [compute_probs(y, ci) for ci in conf_ints]
    for i in range(len(df)):
        bars[i].set_color(cpick.to_rgba(probs[i]))
        bars[i].set_edgecolor('gray')


plt.gcf().canvas.mpl_connect('button_press_event', onclick);


# In[107]:

print(st.norm.cdf(y-df.iloc[1]['mean']/errs[1]))


# In[20]:

print(df['mean'].mean())


# In[ ]:



