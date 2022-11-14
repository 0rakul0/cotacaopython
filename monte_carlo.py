import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as m
import numpy as np
from scipy.stats import norm

df = pd.read_csv('./statistica/hist/MXRF11.csv', sep=';')


list = ['values']
plt.figure()
ax1 = plt.subplot(211)
ax1.plot(df.days, df[list], alpha=1)
plt.title('MXFR11 (2017 - 2022)', fontsize=12)
ax1.legend(list)

for i in range(1):
    ax1.text(x=df.days[-1:], y=df[list[i]][-1:], s=list[i], fontsize=12, color='k')

n=len(df)

# exclui a coluna de datas para calculo de retorno
prec = df.drop(['days'], axis=1)

x= np.linspace(1,n,n)
coef = np.polyfit(x,df['values'], 1)
tendencia = coef[1]+coef[0]*x

print('+++++++++ coeficientes tendencia linear y = b + ax ++++++++++')
print(f'a = {coef[0]}, b = {coef[1]}')

ax1 = plt.subplot(212)
ax1.plot(x, df['values'], '-k', x, tendencia, '-k')
ax1.fill_between(x, df['values'], tendencia, facecolor='gray')
plt.xlabel('meses', fontsize=16)
plt.show()


plt.figure()
ax1=plt.subplot(211)
filtro = m.detrend_linear(df['values'])
mi = filtro.mean() # retorno médio dos ativos por colunas
sigma = filtro.std() # desvio padrão
ax1.plot(x, filtro, '-k')


ax1=plt.subplot(212)
ax1.hist(np.asarray(filtro, dtype='float'), bins=10, alpha=0.3)
plt.title('+++++ histograma da diferença entre a tendencia durante os anos de 2016 a 2022', fontsize=10)
xmin, xmax = plt.xlim()
eixox=np.linspace(xmin, xmax, 100)
eixoy=norm.pdf(eixox,mi,sigma)
ax1.plot(eixox, eixoy, '--k', linewidth=3)
plt.xlabel('classes para a diferença entre tendencias e cota', fontsize=10)
plt.show()

#++++++++++++++++ simulação de monte carlo +++++++++++++++++++++++++
num = 15
meses = 5
alert = np.zeros((meses, num))
simul = np.zeros((meses, num))
eixo = np.zeros((meses, num))

for j in range(num):
    for i in range(meses):
        eixo[i,0] = n+i
        alert[i,j] = np.random.normal(mi, sigma/np.sqrt(n))*np.sqrt(1)
        simul[i,j]=df['values'][-1:]+alert[i,j]

#++++++++++++++ grafico monte carlo ++++++++++++++++++++++++

plt.figure()
plt.plot(x[-5:], df['values'][-5:], '-k')
plt.plot(eixo[:,0], simul, '-k', alpha=0.5)
plt.xlabel('meses', fontsize=12)
plt.ylabel('cota MXFR11', fontsize=12)
plt.grid()
plt.title('simulação monte carlo para o MXFR11', fontsize=13)

plt.show()

print(' ')
print('++++++++++++++++ RESULTADO DA SIMULAÇÃO DE MONTE CARLO ++++++++++++++++')
print('MEDIA REAL (detrends) = ', float(mi))
print('MEDIA DA SIMULAÇÃO (detrends) = ', simul.mean())
print('VOLATILUDADE REAL (desvio padrão dos detrends passados ) = ',float(sigma))
print('VOLATILUDADE DA SIMULAÇÃO (desvio padrão dos detrends futuros) = ', simul.std() )
print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')