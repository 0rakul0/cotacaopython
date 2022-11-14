import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import random


ax = plt.axes(projection='3d')

z = np.linspace(0,15,1000)
x = np.sin(z)
y = np.cos(z)
#
# ax.plot3D(x,y,z, 'gray')

dadz = 15*np.random.random(100)
dadx = np.sin(dadz)+0.2*np.random.random(100)
dady = np.cos(dadz)+0.2*np.random.random(100)

ax.scatter3D(dadx, dady, dadz, c=dadz)
ax.set_xlabel('eixo x')
ax.set_ylabel('eixo y')
ax.set_zlabel('eixo z')


plt.show()
