# -*- coding: utf-8 -*-
"""james_delivery_v2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rH_N1ufBpp7HXvwBg2z8MrUgu1RAaOFO

referencia: 
https://www.kaggle.com/andreshg/timeseries-analysis-a-complete-guide
https://support.sisense.com/kb/en/article/visualizing-forecasting-data-prophet-in-plotly-%E2%80%94-python
"""

#!pip install fbprophet
#!pip install pystan
#!pip install --upgrade plotly

# importar os pacotes necessários
import pandas as pd
import plotly.express as px
import numpy as np

#importar o arquivo csv do meu repositório público no github 
dataset='https://raw.githubusercontent.com/maiaufrrj/superstore_data/main/superstore_dataset2011-2015.csv'
df = pd.read_csv(dataset, encoding= 'unicode_escape')

# visualizar início dos dados
df.head()

#criando dicionário para entender cada recurso disponível e posteriormente modificar dataframe

columns = {'Row ID':'id_linha',
           'Order ID': 'id_pedido', 
           'Order Date': 'data_pedido',
           'Ship Date': 'data_envio',
           'Ship Mode': 'modalidade_frete',
           'Customer ID': 'id_cliente',
           'Customer Name': 'cliente',
           'Segment': 'segmento',
           'City': 'cidade',
           'State': 'estado',
           'Country': 'país',
           'Postal Code': 'cod_postal',
           'Market': 'mercado',
           'Region': 'regiao',
           'Product ID': 'id_produto',
           'Category': 'categoria_produto',
           'Sub-Category': 'subcategoria_produto',
           'Product Name': 'produto',
           'Sales': 'vendas',
           'Quantity': 'quantidade',
           'Discount': 'desconto',
           'Profit': 'lucro',
           'Shipping Cost': 'custo_envio',
           'Order Priority': 'prioridade'
           }
#trocando nomes das colunas e selecionando coluna de índice
df=df.rename(columns=columns).set_index('id_pedido')

df.head()

df['vendas_unit']=df['vendas']/df['quantidade']
df['custo_envio_unit']=df['custo_envio']/df['quantidade']
df['lucro_unit']=df['lucro']/df['quantidade']
df.sample(50)

fig1 = px.histogram(df, x='mercado', y='vendas', histfunc='sum').update_xaxes(categoryorder='total descending')
fig1.show()

fig2 = px.histogram(df, x='mercado', y="custo_envio", histfunc='sum').update_xaxes(categoryorder='total descending')
fig2.show()

#verificando os 20 países que somaram as maiores vendas
topVendas_20_paises = df.groupby(['país']).agg({'vendas':sum})
topVendas_20_paises.sort_values(by='vendas', ascending=False, inplace=True)
topVendas_20_paises.style.format("{:.1f}")
topVendas_20_paises = topVendas_20_paises[:20]

fig2 = px.histogram(topVendas_20_paises, x=topVendas_20_paises.index, y='vendas', histfunc='sum').update_xaxes(categoryorder='total descending')
fig2.show()

#verificando os 20 países que somaram os maiores lucros
topLucro_20_paises = df.groupby(['mercado']).agg({'lucro':sum})
topLucro_20_paises.sort_values(by='lucro', ascending=False, inplace=True)
topLucro_20_paises.style.format("{:.1f}")
topLucro_20_paises = topLucro_20_paises[:20]

fig3 = px.histogram(topLucro_20_paises, x=topLucro_20_paises.index, y='lucro', histfunc='sum').update_xaxes(categoryorder='total descending')
fig3.show()

#verificando os 20 países que somaram os menores lucros
bottomLucro_20_paises = df.groupby(['país']).agg({'lucro':sum})
bottomLucro_20_paises.sort_values(by='lucro', ascending=True, inplace=True)
bottomLucro_20_paises.style.format("{:.1f}")
bottomLucro_20_paises = bottomLucro_20_paises[:20]

fig3 = px.histogram(bottomLucro_20_paises, x=bottomLucro_20_paises.index, y='lucro', histfunc='sum').update_xaxes(categoryorder='total ascending')
fig3.show()

import plotly.io as pio
aggs = ["count","sum","avg","median","mode","rms","stddev","min","max","first","last"]

agg = []
agg_func = []
for i in range(0, len(aggs)):
    agg = dict(
        args=['transforms[0].aggregations[0].func', aggs[i]],
        label=aggs[i],
        method='restyle'
    )
    agg_func.append(agg)

data = [dict(
  type = 'choropleth',
  locationmode = 'country names',
  locations = df['país'],
  z = df['vendas'],
  autocolorscale = False,
  colorscale = 'Portland',
  reversescale = False,
  transforms = [dict(
    type = 'aggregate',
    groups = df['país'],
    aggregations = [dict(
        target = 'z', func = 'sum', enabled = True)
    ]
  )]
)]

layout = dict(
  title = '<b>Agregação de Vendas</b><br>escolha o tipo de agregação',
  xaxis = dict(title = 'Subject'),
  yaxis = dict(title = 'Score', range = [0,22]),
  height = 600,
  width = 900,
  updatemenus = [dict(
        x = 0.85,
        y = 1.15,
        xref = 'paper',
        yref = 'paper',
        yanchor = 'top',
        active = 1,
        showactive = False,
        buttons = agg_func
  )]
)

fig_dict = dict(data=data, layout=layout)

pio.show(fig_dict, validate=False)

import plotly.io as pio
aggs = ["count","sum","avg","median","mode","rms","stddev","min","max","first","last"]

agg = []
agg_func = []
for i in range(0, len(aggs)):
    agg = dict(
        args=['transforms[0].aggregations[0].func', aggs[i]],
        label=aggs[i],
        method='restyle'
    )
    agg_func.append(agg)

data = [dict(
  type = 'choropleth',
  locationmode = 'country names',
  locations = df['país'],
  z = df['lucro'],
  autocolorscale = False,
  colorscale = 'Portland',
  reversescale = False,
  transforms = [dict(
    type = 'aggregate',
    groups = df['país'],
    aggregations = [dict(
        target = 'z', func = 'sum', enabled = True)
    ]
  )]
)]

layout = dict(
  title = '<b>Agregação de Lucro</b><br>escolha o tipo de agregação',
  xaxis = dict(title = 'Subject'),
  yaxis = dict(title = 'Score', range = [0,22]),
  height = 600,
  width = 900,
  updatemenus = [dict(
        x = 0.85,
        y = 1.15,
        xref = 'paper',
        yref = 'paper',
        yanchor = 'top',
        active = 1,
        showactive = False,
        buttons = agg_func
  )]
)

fig_dict = dict(data=data, layout=layout)

pio.show(fig_dict, validate=False)

#categorias de produto que promoveram maiores fontes de lucro
fig4 = px.histogram(df, x='categoria_produto', y='lucro', histfunc='sum').update_xaxes(categoryorder='total descending')
fig4.show()

fig5 = px.scatter(df, x='custo_envio', y='vendas', color='mercado')
fig5.show()

fig6 = px.scatter(df, x='custo_envio', y='desconto',color='mercado')
fig6.show()

#criar dataset resumido em vendas mensais
df2=df
df2.index = pd.to_datetime(df2['data_pedido'])

df2['mes_ano'] = pd.to_datetime(df2['data_pedido']).apply(lambda x: '{month}-{year}'.format(month=x.month, year=x.year))

df_vendas = df2.groupby('mes_ano')['vendas'].sum()
df_vendas.to_frame()

df_vendas = pd.DataFrame({'mes_ano':df_vendas.index, 'vendas':df_vendas.values})
df_vendas['ano'] = pd.DatetimeIndex(df_vendas['mes_ano']).year
df_vendas['mes'] = pd.DatetimeIndex(df_vendas['mes_ano']).month

#último dia do mês
from pandas.tseries.offsets import MonthEnd
df_vendas['ultimo_dia_mes'] = pd.to_datetime(df_vendas['mes_ano']) + MonthEnd(1)

df_vendas = df_vendas.sort_values(['ano', 'mes'], ascending = (True, True))
df_vendas.set_index('mes_ano')
#df_vendas.head(50)

#gráfico para visualizar evolução de vendas
fig = px.line(df_vendas, x='ultimo_dia_mes', y="vendas")
fig.show()

#criar dataset resumido em vendas mensais
df3=df
df3.index = pd.to_datetime(df3['data_pedido'])

df3['mes_ano'] = pd.to_datetime(df3['data_pedido']).apply(lambda x: '{month}-{year}'.format(month=x.month, year=x.year))

df_lucro = df3.groupby('mes_ano')['lucro'].sum()
df_lucro.to_frame()

df_lucro = pd.DataFrame({'mes_ano':df_lucro.index, 'lucro':df_lucro.values})
df_lucro['ano'] = pd.DatetimeIndex(df_lucro['mes_ano']).year
df_lucro['mes'] = pd.DatetimeIndex(df_lucro['mes_ano']).month

#último dia do mês
from pandas.tseries.offsets import MonthEnd
df_lucro['ultimo_dia_mes'] = pd.to_datetime(df_lucro['mes_ano']) + MonthEnd(1)

df_lucro = df_lucro.sort_values(['ano', 'mes'], ascending = (True, True))
df_lucro.set_index('mes_ano')

#gráfico para visualizar evolução de lucro mensal
fig = px.line(df_lucro, x='ultimo_dia_mes', y="lucro")
fig.show()

train_size = int(0.85 * len(df_vendas))
test_size = len(df_vendas) - train_size

univariate_df = df_vendas[['ultimo_dia_mes', 'vendas']].copy()
univariate_df.columns = ['ds', 'y']

train = univariate_df.iloc[:train_size, :]

x_train, y_train = pd.DataFrame(univariate_df.iloc[:train_size, 0]), pd.DataFrame(univariate_df.iloc[:train_size, 1])
x_valid, y_valid = pd.DataFrame(univariate_df.iloc[train_size:, 0]), pd.DataFrame(univariate_df.iloc[train_size:, 1])

print(len(train), len(x_valid))

#https://towardsdatascience.com/time-series-prediction-using-prophet-in-python-35d65f626236
#https://towardsdatascience.com/facebook-prophet-for-time-series-forecasting-in-python-part1-d9739cc79b1d

from sklearn.metrics import mean_absolute_error, mean_squared_error
from fbprophet import Prophet
import math

# Train the model
model = Prophet()
model.fit(train)

#future= model.make_future_dataframe(periods=test_size)
#future.tail(2)

#x_valid = model.make_future_dataframe(periods=test_size, freq='w')
#future= model.make_future_dataframe(periods=12, freq='m')

future = model.make_future_dataframe(periods=12, freq='m')
future.tail(3)

# Predict on valid set
y_pred = model.predict(future)

# Calculo de métricas
score_mae = mean_absolute_error(y_valid, y_pred.tail(test_size)['yhat'])
score_rmse = math.sqrt(mean_squared_error(y_valid, y_pred.tail(test_size)['yhat']))

print(score_mae,score_rmse)

#print(Fore.GREEN + 'RMSE: {}'.format(score_rmse))

from fbprophet.plot import plot_plotly, plot_components_plotly
plot_plotly(model, y_pred)

#forecast = y_pred
#forecast.head(100)

componente_mensal = model.plot_components(y_pred)

#https://facebook.github.io/prophet/docs/diagnostics.html
from fbprophet.diagnostics import cross_validation, performance_metrics 
df_vendas_cv = cross_validation(model, initial='240 days', period='60 days', horizon = '120 days')

#https://www.youtube.com/watch?v=CW1PZwNG-wQ
relatorio_regressao = performance_metrics(df_vendas_cv)
relatorio_regressao.head()

relatorio_regressao['mape'].mean()

from fbprophet.plot import plot_cross_validation_metric
fig = plot_cross_validation_metric(df_vendas_cv, metric='mape')

"""MAPE: Erro Absoluto Médio Percentual

# ![mape.jpg](data:image/jpeg;base64,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)
"""

# Plotar previsão
#import seaborn as sns
#f, ax = plt.subplots(1)
#f.set_figheight(8)
#f.set_figwidth(30)

#model.plot(y_pred, ax=ax)

#sns.lineplot(x=x_valid['ds'], y=y_valid['y'], ax=ax, color='orange', label='Ground truth') #navajowhite

#ax.set_title(f'Previsão de Vendas \n MAE: {score_mae:.2f}, RMSE: {score_rmse:.2f}', fontsize=14)
#ax.set_xlabel(xlabel='Data', fontsize=14)
#ax.set_ylabel(ylabel='Vendas', fontsize=14)

#plt.show()

#gráfico para visualizar evolução de lucro mensal
#fig = px.line(df_lucro, x='mes_ano', y="lucro")
#fig.show()

"""Testando LSTM

"""

from sklearn.preprocessing import MinMaxScaler

data = univariate_df.filter(['y'])

#Converter dataframe para array (numpy)
dataset = data.values

#Mudando a escala 
#scaler = MinMaxScaler(feature_range=(-1, 0))
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(dataset)

scaled_data[:10]

# Defines the rolling window
look_back = 3
# Split into train and test sets
train, test = scaled_data[:train_size-look_back,:], scaled_data[train_size-look_back:,:]

def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(look_back, len(dataset)):
        a = dataset[i-look_back:i, 0]
        X.append(a)
        Y.append(dataset[i, 0])
    return np.array(X), np.array(Y)

x_train, y_train = create_dataset(train, look_back)
x_test, y_test = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

print(len(x_train), len(x_test))

from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import EarlyStopping

#Build the LSTM model
model = Sequential()
early_stop = EarlyStopping(monitor='val_loss', patience = 20)

model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(25))
model.add(Dropout(0.1))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error') 

#Train the model
history = model.fit(x_train, y_train, batch_size=1, epochs=500, validation_data=(x_test, y_test), callbacks=[early_stop])

model.summary()

# Lets predict with the model
train_predict = model.predict(x_train)
test_predict = model.predict(x_test)

# invert predictions
train_predict = scaler.inverse_transform(train_predict)
y_train = scaler.inverse_transform([y_train])

test_predict = scaler.inverse_transform(test_predict)
y_test = scaler.inverse_transform([y_test])

# Get the root mean squared error (RMSE) and MAE
score_rmse = np.sqrt(mean_squared_error(y_test[0], test_predict[:,0]))
score_mae = mean_absolute_error(y_test[0], test_predict[:,0])
#print(Fore.GREEN + 'RMSE: {}'.format(score_rmse))

import matplotlib.pyplot as plt
import seaborn as sns
x_train_ticks = univariate_df.head(train_size)['ds']
y_train = univariate_df.head(train_size)['y']
x_test_ticks = univariate_df.tail(test_size)['ds']

# Plot the forecast
f, ax = plt.subplots(1)
f.set_figheight(6)
f.set_figwidth(15)

sns.lineplot(x=x_train_ticks, y=y_train, ax=ax, label='Train Set') #navajowhite
sns.lineplot(x=x_test_ticks, y=test_predict[:,0], ax=ax, color='green', label='Prediction') #navajowhite
sns.lineplot(x=x_test_ticks, y=y_test[0], ax=ax, color='orange', label='Ground truth') #navajowhite

ax.set_title(f'Previsão de vendas \n MAE: {score_mae:.2f}, RMSE: {score_rmse:.2f}', fontsize=14)
ax.set_xlabel(xlabel='Data', fontsize=14)
ax.set_ylabel(ylabel='Vendas', fontsize=14)

plt.show()