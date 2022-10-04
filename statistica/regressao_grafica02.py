import numpy as np
import time
import matplotlib.pyplot as plt
import random


plt.style.use('ggplot')
plt.ion()

x = np.arange(1,6)

for i in range(10):
    dados = np.random.randint(20, 30, 5)
    plt.cla()
    plt.clf()
    plt.bar(x, dados)
    plt.pause(0.1)

plt.ioff()
plt.show()