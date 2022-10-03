# imports
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np

# page config
st.set_page_config(layout='wide', page_icon=":bar_chart", page_title="House Rocket - Analysis")


# carregando os dados
def get_data(__path__):
    df = pd.read_csv(__path__, sep=',')
    df['id'] = df['id'].astype(str)
    df['date'] = pd.to_datetime(df['date'])
    return df


data = get_data('datasets/kc_house_data.csv')

# import style
with open('./style/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.header(':bar_chart: Dashboard - House Rocket Analytics')
st.markdown('  ')

# classificação tipo
conditionlist = [
    (data['bedrooms'] <= 1),
    (data['bedrooms'] >= 2) & (data['bedrooms'] <= 3),
    (data['bedrooms'] >= 4)]

choicelist = ['studio', 'apartment', 'house']

data['tipo'] = np.select(conditionlist, choicelist)

# classificação condição
conditionlist = [
    (data['condition'] <= 1),
    (data['condition'] >= 2) & (data['condition'] <= 3),
    (data['condition'] >= 4)]

choicelist = ['bad', 'regular', 'good']

data['situation'] = np.select(conditionlist, choicelist)

# classificação level
conditionlist = [
    (data['price'] <= 321950),
    (data['price'] > 321950) & (data['price'] <= 450000),
    (data['price'] > 450000) & (data['price'] <= 6450000),
    (data['price'] > 645000)]

choicelist = ['0', '1', '2', '3']

data['level'] = np.select(conditionlist, choicelist)

# =========================================================================== Filtros sidebar=======================================================================================
st.sidebar.write('Utilize os filtros abaixo:')
tipo = st.sidebar.multiselect('Tipo de Imóvel', options=data['tipo'].unique(), default=data['tipo'].unique())
situation = st.sidebar.multiselect('Situação do Imóvel', options=data['situation'].unique(), default=data['situation'].unique())
level = st.sidebar.multiselect('Nível de preço', options=data['level'].unique(), default=data['level'].unique())

# Query
if (tipo != []) & (situation != []) & (level != []):
    data = data.loc[data['tipo'].isin(tipo)]
    data = data.loc[data['level'].isin(level)]
    data = data.loc[data['situation'].isin(situation)]

elif (tipo == []) & (situation != []) & (level != []):
    data = data.loc[data['situation'].isin(situation)]
    data = data.loc[data['level'].isin(level)]

elif (tipo != []) & (situation == []) & (level != []):
    data = data.loc[data['tipo'].isin(tipo)]
    data = data.loc[data['level'].isin(level)]

elif (tipo != []) & (situation != []) & (level == []):
    data = data.loc[data['tipo'].isin(tipo)]
    data = data.loc[data['situation'].isin(situation)]

elif (tipo == []) & (situation == []) & (level != []):
    data = data.loc[data['level'].isin(level)]

elif (tipo == []) & (situation != []) & (level == []):
    data = data.loc[data['situation'].isin(situation)]

elif (tipo != []) & (situation == []) & (level == []):
    data = data.loc[data['tipo'].isin(tipo)]

elif (tipo == []) & (situation == []) & (level == []):
    data.copy()

# =================================================================================== charts ====================================================================================

# 1 - Qual o total de imóveis do conjunto de dados?
total_imoveis = data['id'].nunique()

# 2 - Qual o preço médio dos imóveis ?
preco_medio = data['price'].mean()

# 3 - Qual valor do imóvel mais caro? ?
max_price = data['price'].max()

# 4 - Qual valor do imóvel mais barato?
min_price = data['price'].min()


# Formatar metricas
def formatar_decimal(__path__):
    formato = "{:,.2f}".format(__path__).replace(",", "X").replace(".", ".").replace("X", ".")
    return formato


def formatar_real(__path__):
    formato = "{:,.2f}".format(__path__).replace(",", "X").replace(".", ".").replace("X", ",")
    return formato


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Total de imóveis:', formatar_decimal(total_imoveis))

with col2:
    st.metric('Preço Médio Imóveis:', f'${formatar_real(preco_medio)}')

with col3:
    st.metric('Preço Mínimo Imóveis:', f'${formatar_real(min_price)}')

with col4:
    st.metric('Preço Máximo Imóveis:', f'${formatar_real(max_price)}')

st.markdown('---')

# 5 - Quais os tipos de imóveis analisados (studio, apartment, house)?
col1, col2 = st.columns(2)

with col2:
    total_tipo = data['tipo'].value_counts()
    fig_pie_tipo = px.pie(total_tipo, values='tipo', names=total_tipo.index, title='Tipo de imóvel:', hole=.5,
                          color=total_tipo.index, color_discrete_map={'studio': '#2E5902',
                                                                      'apartment': '#D96941',
                                                                      'house': '#13678A'})
    st.plotly_chart(fig_pie_tipo, use_container_width=True)

# 6 - Qual o preço médio por tipo de imóvel?
with col1:
    media_price = data.groupby(by=["tipo"]).mean()[["price"]].sort_values(by="price")
    fig_bar_price = px.bar(media_price, x=media_price.index, y='price', color=media_price.index,
                           title='Preço médio por tipo de imóvel:', text_auto=True,
                           color_discrete_map={'studio': '#2E5902',
                                               'apartment': '#D96941',
                                               'house': '#13678A'})

    fig_bar_price.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar_price, use_container_width=True)

col1, col2 = st.columns(2)

# 7 - Qual a média de quartos por tipo de imóvel?
with col1:
    media_bedrooms = data.groupby(by=["tipo"]).mean()[["bedrooms"]].sort_values(by="bedrooms")
    fig_bar_bedrooms = px.bar(media_bedrooms, x=media_bedrooms.index, y='bedrooms', color=media_bedrooms.index,
                              title='Média de quartos por tipo:', text_auto=True,
                              color_discrete_map={'studio': '#2E5902',
                                                  'apartment': '#D96941',
                                                  'house': '#13678A'})

    fig_bar_bedrooms.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar_bedrooms, use_container_width=True)

# 8 - Qual a média de banheiros por tipo de imóvel?
with col2:
    media_bathrooms = data.groupby(by=["tipo"]).mean()[["bathrooms"]].sort_values(by="bathrooms")
    fig_bar_bathrooms = px.bar(media_bathrooms, x=media_bathrooms.index, y='bathrooms', color=media_bathrooms.index,
                               title='Média de banheiros por tipo:', text_auto=True,
                               color_discrete_map={'studio': '#2E5902',
                                                   'apartment': '#D96941',
                                                   'house': '#13678A'})

    fig_bar_bathrooms.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar_bathrooms, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    total_situation = data['situation'].value_counts()
    fig_situation = px.pie(total_situation, values='situation', names=total_situation.index,
                           title='Situação do Imóvel:', hole=.5,
                           color=total_situation.index, color_discrete_map={'bad': '#2E5902',
                                                                            'regular': '#D96941',
                                                                            'good': '#13678A'})
    st.plotly_chart(fig_situation, use_container_width=True)

with col2:
    media_price = data.groupby(by=["situation"]).mean()[["price"]].sort_values(by="price")
    fig_bar_price = px.bar(media_price, x=media_price.index, y='price', color=media_price.index,
                           title='Preço médio por situação de imóvel::', text_auto=True,
                           color_discrete_map={'bad': '#2E5902',
                                               'regular': '#D96941',
                                               'good': '#13678A'})

    fig_bar_price.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar_price, use_container_width=True)


# 9 - Quais recursos de uma casa mais impactam no preço?
data_heatmap = data[['price',
                     'bedrooms',
                     'bathrooms',
                     'condition',
                     'yr_built',
                     'waterfront',
                     'sqft_living',
                     'sqft_lot',
                     'view',
                     'grade',
                     'sqft_above',
                     'sqft_basement',
                     'sqft_living15',
                     'sqft_lot15',
                     'yr_renovated',
                     'floors']].corr()

heatmap = px.imshow(data_heatmap, text_auto=True, aspect="auto", color_continuous_scale='balance',
                    title='Matriz de correlação entre as variáveis:')

st.plotly_chart(heatmap, use_container_width=True)

# mapa
st.markdown('Localização imóveis:')
data_map = data[['id', 'lat', 'long', 'price']]
fig_map = px.scatter_mapbox(data, lat='lat', lon='long',
                            hover_name='id',
                            hover_data=['price'],
                            color_discrete_sequence=['blueviolet'],
                            zoom=10,
                            size='price',
                            size_max=15,
                            height=500, )

fig_map.update_layout(mapbox_style='open-street-map')
fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig_map, use_container_width=True)
st.write('Data Overview:', data)
