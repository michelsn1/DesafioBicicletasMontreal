# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 12:09:55 2018

@author: miche
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as sm
from datetime import datetime

# Importando o Dataset
dataset = pd.read_csv('DatasetFinal.csv')
dataset['Horario'] = (dataset.apply(lambda row: datetime(
                              int(row['Ano']), int(row['Mês']), int(row['Dia']),
                              int(row['Hora'])), axis=1))

#Lidando com a possibilidade de nenhuma bicicleta ter sido alugada em um horário
dataset.iloc[:,11]=dataset.iloc[:,11].fillna(0)
np.argwhere(np.isnan(dataset.iloc[:,11]))

#Criando os vetores de entrada e saída
X = dataset.iloc[:, 1:11].values
y = dataset.iloc[:, 11].values

# Trabalhando com a possibilidade de falta de dados em X
from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0)
imputer = imputer.fit(X[:, 1:11])
X[:, 1:11] = imputer.transform(X[:, 1:11])


#Dividindo os dados em Training set e Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)



# Ajustando o modelo de Random Forest Regression
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor()
regressor.fit(X_train, y_train)


#Olhando os valores de Adjusted R² e P-Value
#Busca pelas variáveis de entrada mais importantes(P-Value<0.05)
X_opt= X_train[:,[0,1,2,3,4,5,6,7,8,9]]
regressor_OLS=sm.OLS(endog=y_train, exog = X_opt).fit()
regressor_OLS.summary()

#Remoção do Ponto de Orvalho
X_opt= X_train[:,[0,1,2,3,4,5,7,8,9]] 
regressor_OLS=sm.OLS(endog=y_train, exog = X_opt).fit()
regressor_OLS.summary()

#Remoção do dia
X_opt= X_train[:,[0,1,3,4,5,7,8,9]]
regressor_OLS=sm.OLS(endog=y_train, exog = X_opt).fit()
regressor_OLS.summary()

#Remoção do ano
X_opt= X_train[:,[1,3,4,5,7,8,9]]
regressor_OLS=sm.OLS(endog=y_train, exog = X_opt).fit()
regressor_OLS.summary()

#Remoção da velocidade do vento
X_opt= X_train[:,[1,3,4,5,7,9]]
regressor_OLS=sm.OLS(endog=y_train, exog = X_opt).fit()
regressor_OLS.summary()
X_test=X_test[:,[1,3,4,5,7,9]]

# Ajustando o novo modelo
regressor.fit(X_opt, y_train)

#Otimizando os Hiperparâmetros do modelo 
from sklearn.model_selection import GridSearchCV
#parameters = [{}]#Teste 1 - Valores Padrões com otimização das variaveis- Resultado:0.9158
#parameters = [{ #Teste 2
#    'bootstrap': [True],
#    'max_depth': [None, 10, 50],
#    'max_features': [2, 3],
#    'min_samples_leaf': [1,3],
#    'min_samples_split': [2,3],
#    'n_estimators': [10,50, 100] #Resultado:0,9206
#    }]
parameters = [{ #Teste 3
    'bootstrap': [True],
    'max_depth': [40,50,60], #40
    'max_features': [2,3,4],#4
    'min_samples_leaf': [1],#1
    'min_samples_split': [3,4],#3
    'n_estimators': [100,200,500] #500
    }]#Resultado:0,9266 
grid_search = GridSearchCV(estimator = regressor, param_grid = parameters,
                          cv =3, n_jobs=-1, )
grid_search = grid_search.fit(X_opt,y_train)
melhorresultado = grid_search.best_score_
melhoresparametros = grid_search.best_params_

regressor = RandomForestRegressor(n_estimators=500,bootstrap=True,max_depth=40,
                                  max_features=4,min_samples_leaf=3)
regressor.fit(X_opt, y_train)

#Observando-se os resultados previstos
y_pred = regressor.predict(X_test)


# Gráfico - Análise Geral
eixoX=np.arange(0,10320,100)
eixoy=X[range(0,10320,100),:]
eixoy=regressor.predict(eixoy[:,[1,3,4,5,7,9]])
plt.scatter(eixoX, y[range(0,10320,100)], color = 'red')
plt.plot(eixoX, eixoy, color = 'blue')
plt.title('Comparação entre os resultados reais e o modelo - Dataset Inteiro')
plt.xlabel('Número da linha')
plt.ylabel('Nº de Bicicletas Alugadas')
plt.show()

# Gráfico2 - Análise do mês 6 de 2016
eixoX=np.arange(6288,7007,5)
eixoy=X[range(6288,7007,5),:]
eixoy=regressor.predict(eixoy[:,[1,3,4,5,7,9]])
plt.scatter(eixoX, y[range(6288,7007,5)], color = 'red')
plt.plot(eixoX, eixoy, color = 'blue')
plt.title('Comparação entre os resultados reais e o modelo - Junho de 2016')
plt.xlabel('Número da linha')
plt.ylabel('Nº de Bicicletas Alugadas')
plt.show()


