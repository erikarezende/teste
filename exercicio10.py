import seaborn as sns

# Criando o gráfico com Seaborn (gráfico de barras)
df_total_melted = df_total.melt(id_vars='Estado', value_vars=['Quantidade_de_Homens', 'Quantidade_de_Mulheres'], var_name='Sexo', value_name='Quantidade')

# Criando o gráfico
plt.figure(figsize=(10, 6))
sns.barplot(x='Estado', y='Quantidade', hue='Sexo', data=df_total_melted, palette="Set2")

# Adicionando título e rótulos
plt.title('Quantidade de Homens e Mulheres Deputados por Estado')
plt.xlabel('Estado')
plt.ylabel('Quantidade de Deputados')

# Exibindo o gráfico
plt.tight_layout()
plt.show()

st.pyplot(plt)
