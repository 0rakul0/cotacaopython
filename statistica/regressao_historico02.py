import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


nome_csv = "mxrf11"
try:
    df_base = pd.read_csv(f'./hist/{nome_csv.upper()}.csv', sep=";")
    print(df_base.head())
except Exception as e:
    print(e)
dados = []
for x in df_base['redimentos']:
    valor = x
    dados.append(valor)

plt.figure()
plt.subplot(221)
sns.boxplot(data=dados)
sns.stripplot(data=dados, marker='o', color='black')
plt.ylabel(f'BOXPLOT - {nome_csv}', fontsize=14)

plt.subplot(222)
sns.histplot(dados, kde=True)
plt.ylabel(f'AMOSTRA - {nome_csv}', fontsize=14)

plt.subplot(223)
sns.violinplot(dados)
plt.ylabel(f'VIOLIN - {nome_csv}', fontsize=14)


plt.show()

