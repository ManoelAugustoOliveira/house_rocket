# framework:https://streamlit.io/
# biblioteca gráfica:https://plotly.com/python/

#imports
import pandas as pd
import plotly.express as px
import streamlit as st

# page config
st.set_page_config(layout='wide', page_icon=":bar_chart", page_title="House Hocket - Analysis")

st.title('House Sales in King County, USA')
st.write("""Este conjunto de dados contém preços de venda de casas para King County.
         Inclui casas vendidas entre maio de 2014 e maio de 2015.
         A análise das informações disponibilizadas tem como objetivo fornecer informações que auxiliem
         no processe de aquisições dos imoveis e indiquem quais estão em ótimas localização e possuem preço baixo.""")

st.write("fonte:https://www.kaggle.com/datasets/harlfoxem/housesalesprediction")

st.write("""**Estratégia de negócio:**

Quanto maior a diferença entre a compra e a venda, maior o lucro da empresa e portanto maior sua receita.
Entretanto, as casas possuem muitos atributos que as tornam mais ou menos atrativas aos compradores e vendedores e a localização e o período do ano também podem influenciar os preços.

**A seguir vamos responder as seguintes perguntas**:""")

st.write("**1** - Qual o total de imóveis do conjunto de dados?")
st.write("**2** - Qual o preço médio dos imóveis ?")
st.write("**3** - Qual valor do imóvel mais caro?")
st.write("**4** - Qual valor do imóvel mais barato?")
st.write("**5** - Quais os tipos de imóveis analisados (studio, apartment, house)?")
st.write("**6** - Qual o preço médio por tipo de imóvel?")
st.write("**7** - Qual a média de quartos por tipo de imóvel?")
st.write("**8** - Qual a média de banheiros por tipo de imóvel?")
st.write("**9** - Qual a situação dos imóveis analisados?")
st.write("**10** - Qual o preço médio levando em conta a situação do imóvel?")
st.write("**11** - Qual a localização dos imóveis?")
