import datetime as dt
import numpy as np
import skfuzzy as fuzz
from pytrends.request import TrendReq
from skfuzzy import control as ctl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import seaborn as sns

#+++++++++++++++++ eixo das abscissas para as fun. pertinencias ++++++++++++++++++++
preco = ctl.Antecedent(np.arange(17,30,1), 'preço')
vol = ctl.Antecedent(np.arange(0,2e8,1e5), 'volume')
dec = ctl.Consequent(np.arange(0,2e8,1e5), 'decisao')

#++++++++++++++++++++ precos +++++++++++++++++++++++++
preco['barato'] = fuzz.gaussmf(preco.universe, 18,2)
preco['medio'] = fuzz.gaussmf(preco.universe, 22,2)
preco['caro'] = fuzz.gaussmf(preco.universe, 30, 2)
preco.view()
plt.text(x=18, y=0.8, s='barato', fontsize=10)
plt.text(x=22, y=0.8, s='medio', fontsize=10)
plt.text(x=28, y=0.8, s='caro', fontsize=10)

#++++++++++++++++++++volume+++++++++++++++++++++++++++++
vol['baixo'] = fuzz.gaussmf(vol.universe,0.4e8,6e7)
vol['medio'] = fuzz.gaussmf(vol.universe,0.6e8,2e7)
vol['alto'] = fuzz.gaussmf(vol.universe,1e8,3e7)
vol.view()
plt.text(x=0.25e8, y=0.8, s='abixo', fontsize=10)
plt.text(x=0.5e8, y=0.8, s='medio', fontsize=10)
plt.text(x=1e8, y=0.8, s='alto', fontsize=10)

#+++++++++++++++++++decisao de compra +++++++++++++++++++++
dec['comprar'] = fuzz.gaussmf(dec.universe,0.4e8,6e7)
dec['manter'] = fuzz.gaussmf(dec.universe,0.6e8,2e7)
dec['vender'] = fuzz.gaussmf(dec.universe,1e8,3e7)
dec.view()
plt.text(x=0.25e8, y=0.8, s='comprar', fontsize=10)
plt.text(x=0.5e8, y=0.8, s='manter', fontsize=10)
plt.text(x=1e8, y=0.8, s='vender', fontsize=10)

#+++++++++++++++ logica de compra e venda +++++++++++++++++++
regra1 = ctl.Rule(preco['barato'] & vol['baixo'], dec['comprar'])
regra2 = ctl.Rule(preco['barato'] & vol['alto'], dec['comprar'])
regra3 = ctl.Rule(preco['medio'] & vol['baixo'], dec['comprar'])
regra4 = ctl.Rule(preco['medio'] & vol['medio'], dec['manter'])
regra5 = ctl.Rule(preco['medio'] & vol['alto'], dec['vender'])
regra6 = ctl.Rule(preco['caro'] & vol['alto'], dec['vender'])

#++++++++++++++ controle +++++++++++++
decisao_ctl=ctl.ControlSystem([regra1,regra2,regra3,regra4,regra5,regra6])
decisao=ctl.ControlSystemSimulation(decisao_ctl)

#+++++++++++++ funcao de calculo defuzz ++++++++++++++
def indFz(entrada):
    #input
    print(entrada)
    decisao.input['preço'] = entrada[0]
    decisao.input['volume'] = entrada[1]
    #output
    decisao.compute()
    return (decisao.output['decisao'])

#+++++++++++++++++ aplicação ++++++++++++++++++++++++
data = yf.download("PETR4.SA", start="2020-01-01", end="2022-09-30")
#+++++++++++++++++ decisao final +++++++++++++++++++++
mval = np.zeros((len(data),3))
for i in range(len(data)):
    res1 = indFz([data['Close'].values[i],data['Volume'].values[i]])
    j=0
    for t in dec.terms:
        s = np.interp(res1, dec.universe, dec[t].mf)
        mval[i,j] = s
        j=j+1
mval = pd.DataFrame(mval, columns=['compra', 'manter', 'vender'])
dec_fuzz = mval.idxmax(axis=1)
print('+++++ decisao final ++++++')
print(dec_fuzz)
print('++++++++++++++++++++++++++')

dec.view(sim=decisao)
plt.text(x=0.25e8, y=0.8, s='comprar', fontsize=13)
plt.text(x=0.5e8, y=0.8, s='manter', fontsize=13)
plt.text(x=1e8, y=0.8, s='vender', fontsize=13)
plt.show()

figura=plt.figure(figsize=(20, 7))
ax1=plt.subplot(111)
plt.title('Petrobras - PETR4')
ax1.plot(data.index, data['Close'], '--k')
ax1.set_ylabel('PETR4', fontsize=12)
for i in range(len(dec_fuzz)):
    ax1.text(x=data.index[i], y=data['Close'].values[i], s=str(dec_fuzz[i]), fontsize=10)

ax2 = ax1.twinx()
ax2.plot(data.index, data['Volume'])
ax2.set_ylabel('Volume', fontsize=15)
plt.show()