#Nov 1st, 2023 written by Nanase Harada
#Tested with Python version 3.9.12
import numpy as np
import pca_lib as plib
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt, colors
#from sklearn.decomposition import PCA
import matplotlib as mpl
import pandas as pd
import itertools
#--------------------------------------


#Read the standardized intensity matrix as pandas DataFrame

df = pd.read_csv('std_datalist.csv',index_col=0)

#print('Shape of the dataframe',df.shape,df.shape[0])

#Number of transition
ntran = df.shape[0]

#Transpose the datalist
dft = df.transpose()
#Obtain the correlation matrix
corrmat = dft.corr()
#print(type(corrmat))

cmap = plt.cm.bwr
fig,ax = plt.subplots()
#Display matrix
ax.matshow(corrmat,cmap=cmap)

y=[]
for i in range(ntran):
    y.append(ntran*[i])

sc = plt.scatter(ntran*list(range(ntran)),y,c=corrmat.values,cmap= cmap,s=20,marker='s')

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

#Obtain the list of transition names
tran = df.index.values.tolist()

#Create lists l1, l2 with sizes of ntran*ntran to label the scatter points.
l1 = ntran*list(tran)
#print(np.shape(list(tran)),ntran)
l2=[]
for j in range(ntran):
    l2.append(ntran*[tran[j]])
l1 = list(np.array(l1).flatten())
l2 = list(itertools.chain.from_iterable(l2))

#Function to update annotation--------------------------------
def update_annot(ind):
    i = ind["ind"][0]
    pos = sc.get_offsets()[i]
    annot.xy = pos
    text = l1[i]+' vs. '+l2[i]
    annot.set_text(text)
    #annot.get_bbox_patch().set_facecolor(cmap(int(text)/10))

#Function to make an event happen when hovering the cursor----
def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        print('ind',ind)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()
#---------------------------------------------------------------
#plt.colorbar(sc)
#print(np.shape(l1))

fig.canvas.mpl_connect("motion_notify_event", hover)
plt.colorbar(sc,location='bottom', pad=0.1,fraction = 0.04)
plt.show()



