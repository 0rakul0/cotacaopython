from mpl_toolkits import mplot3d
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



plt.style.use("ggplot")
x=["MXRF11","RZAG11","BIME11","VGIA11"]
y=[57,60,60,67]
z=[6,7,6.2,10]

plt.figure(figsize=(12,7))

ax=plt.subplot(221)
ax.bar(x,y,color='black', alpha=0.7)

ax=plt.subplot(222)
ax.barh(x,y,color='black', alpha=0.7)

ax=plt.subplot(223)
saltar = (0,0,0,0.1)
ax.pie(y, explode=saltar, labels=x, autopct='%1.1f%%')
ax.axis('equal')

ax=plt.subplot(224)
cmap = sns.cubehelix_palette(8, start=0, light=1, as_cmap=True)
sns.kdeplot(x=y, y=z, cmap=cmap, fill=True)

plt.figure(figsize=(12,7))
ab=plt.subplot(221)
sns.kdeplot(x=y, y=z)
plt.show()