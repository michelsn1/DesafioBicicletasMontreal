# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 20:08:18 2018

@author: miche
"""

# Importando as bibliotecas
import numpy as np
import pandas as pd
from datetime import date
import collections

                    
# Importando os dados de aluguel de bicicleta e os climaticos
datasetbike = pd.read_csv('Bixi_time.csv', encoding = 'ISO-8859-1')
datasetclimate = pd.read_csv('Climate2.csv', encoding = 'ISO-8859-1')

#Criando o dataset final
legenda=['Ano','Mês','Dia', 'Hora','Dia da Semana', 'Temperatura(ºC)',
         'Ponto de Orvalho(ºC)', 'Umidade Relativa', 'Velocidade do Vento(Km/h)',
         'Visibilidade', 'Nº de Alugueis por hora']
datasetfinal=pd.DataFrame(index= datasetclimate.index, columns=legenda)

#Importando as variaveis de tempo e clima para a base de dados
datasetfinal.iloc[:,0]=datasetclimate.iloc[:,2] #Ano
datasetfinal.iloc[:,1]=datasetclimate.iloc[:,3] #Mês
datasetfinal.iloc[:,2]=datasetclimate.iloc[:,4] #Dia
datasetfinal.iloc[:,5]=datasetclimate.iloc[:,7] #Temperatura
datasetfinal.iloc[:,6]=datasetclimate.iloc[:,9] #Ponto de Orvalho
datasetfinal.iloc[:,7]=datasetclimate.iloc[:,11] #Umidade Relativa
datasetfinal.iloc[:,8]=datasetclimate.iloc[:,15] #Velocidade do Vento
datasetfinal.iloc[:,9]=datasetclimate.iloc[:,17] #Visibilidade

#Criando a variável dia da semana:
for i in range(len(datasetclimate)):
    hora=datasetclimate.iloc[i,5][0:2]
    datasetfinal.iloc[i,3]=int(hora)
    diadasemana=date(datasetclimate.iloc[i,2],datasetclimate.iloc[i,3],
    datasetclimate.iloc[i,4]).weekday();
    datasetfinal.iloc[i,4]=diadasemana
    
#Somando o nº de bicicletas alugadas em cada hora
databike = ["" for x in range(len(datasetbike))]
for i in range(len(datasetbike)):
    databike[i]=datasetbike.iloc[i,1][0:13]
counter=collections.Counter(databike)


# Preenchendo no dataset a variável do nº de bicicletas alugadas por hora
valores = list(counter.values())
datas = list(counter.keys())
for i in range(len(datasetfinal)):
    data=[datasetfinal.iloc[i,0], datasetfinal.iloc[i,1],datasetfinal.iloc[i,2],
    datasetfinal.iloc[i,3]]
    for k in range(len(datas)):
        datacomp=[int(datas[k][0:4]),int(datas[k][5:7]),int(datas[k][8:10]),
                  int(datas[k][11:13])]
        ano=datacomp[0]
        mes=datacomp[1]
        dia=datacomp[2]
        hora=datacomp[3]
        if(ano==data[0] and mes ==int(data[1]) and dia ==int(data[2]) and hora==int(data[3])):
            datasetfinal.iloc[i,10]=valores[k]

#Exportando para CSV:       
datasetfinal.to_csv('DatasetFinal.csv', encoding='utf-8')

