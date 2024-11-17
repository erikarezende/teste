import requests
import pandas as pd
import streamlit as st
import seaborn as sns

url='https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=F&ordem=ASC&ordenarPor=nome'

response = requests.get(url).json()

response.keys()

#acessando a chave dados do dicionário
dfmulheres = pd.DataFrame(response['dados'])

#contando a quantidade de uf de deputadas
uf_counts = dfmulheres['siglaUf'].value_counts()

# Transformando a Series em um DataFrame
df_uf_counts = uf_counts.reset_index()

# Renomeando as colunas para tornar mais claro
df_uf_counts.columns = ['Estado', 'Quantidade_de_Mulheres']

#dados deputados homens por UF
url2='https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=M&ordem=ASC&ordenarPor=nome'

response_h = requests.get(url2).json()

#acessando a chave 'dados' do dicionário e criando o dataframe
dfhomens = pd.DataFrame(response_h['dados'])

#contando a quantidade de uf de deputados
uf_counts_h = dfhomens['siglaUf'].value_counts()

# Transformando a Series em um DataFrame
df_uf_counts_h = uf_counts_h.reset_index()

# Renomeando as colunas para tornar mais claro
df_uf_counts_h.columns = ['Estado', 'Quantidade_de_Homens']

# Exibindo o DataFrame
print(df_uf_counts_h)

df_total = pd.merge(df_uf_counts, df_uf_counts_h, on='Estado', how='outer')

#adicionando a coluna total de deputados

df_total['Total_de_deputados'] = df_total['Quantidade_de_Mulheres'] + df_total['Quantidade_de_Homens']

st.title('Quantidade de Deputados Homens e Mulheres por UF"')

# filtro por estado
estados = df_total['Estado'].unique()
estadoFiltro = st.selectbox(
    'Qual estado selecionar?',
     estados)
dadosFiltrados = df_total[df_total['Estado'] == estadoFiltro]
if st.checkbox('Mostrar tabela'):
  st.write(dadosFiltrados)

df_filtrado_melted = dadosFiltrados.melt(id_vars='Estado', 
                                         value_vars=['Quantidade_de_Mulheres', 'Quantidade_de_Homens'], 
                                         var_name='Sexo', 
                                         value_name='Quantidade')

# Criando o gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x='Sexo', y='Quantidade', data=df_filtrado_melted, palette="Set2")

# Adicionando título e rótulos
plt.title(f'Quantidade de Mulheres e Homens Deputados no Estado de {estadoFiltro}')
plt.xlabel('Sexo')
plt.ylabel('Quantidade de Deputados')

# Exibindo o gráfico no Streamlit
st.pyplot(plt)


st.header('Quantidade de Deputados e Deputadas por UF')

st.bar_chart(df_total, x="Estado", y=["Quantidade_de_Mulheres", "Quantidade_de_Homens"], color=["#FF0000", "#0000FF"])

st.header('Quantidade de Deputados Homens e Mulheres')

qtdeMulheresDepUf = (df_total['Quantidade_de_Mulheres'].sum())
st.write("A quantidade de Deputadas é " + str(qtdeMulheresDepUf))

qtdeHomensDepUf = (df_total['Quantidade_de_Homens'].sum())
st.write("A quantidade de Deputados é " + str(qtdeHomensDepUf))
