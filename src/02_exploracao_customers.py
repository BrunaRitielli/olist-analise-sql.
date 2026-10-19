#%%
import pandas as pd

# Carregar tabela de clientes
customers = pd.read_csv("../dados/olist_customers_dataset.csv")

#Visualizar as primeiras linhas
print(customers.head())

#%%
# Ver quantidade de linhas e colunas
print("\nDimensões:")
print(customers.shape)

#%%
# Ver nomes e tipos das colunas
print("\nInformaçoes:")
print(customers.info())

#%%
# ver valores nulos por coluna
print("\nValores nulos:")
print(customers.isnull().sum())


# %%
#Verificar clientes duplicados pelo ID único
print("\nClientes duplicados:")
print(customers["customer_unique_id"].duplicated().sum())

#%%
# Verificar duplicidade do customer_id 
print("\ncustomer_id duplicados:")
print(customers["customer_id"].duplicated().sum())

#%%
# Quantidade de pessoas únicas
print("\nClientes únicos (customer_unique_id):")
print(customers["customer_unique_id"].nunique())

#%%
# conferir: total de linhas - pessoas únicas deve bater com os duplicados
print("\nLinhas - únicos:")
print(len(customers) - customers
["customer_unique_id"].nunique())

#%%
# Estados: ver valores e contagem 
print("\nEstados:")
print(customers["customer_state"].value_counts())
print("Estados distintos:", customers
["customer_state"].nunique())

#%%
# Cidades: ver as mais frequentes e quantas existem

print("\nCidades (top15):")
print(customers["customer_city"].value_counts().head(15))
print("cidades distintas:", customers
["customer_city"].nunique())

#%%
#Inconsistências de texto: espaços extras e maiúsculas/minúsculas
print("\ncidades com espaço extra no inicio/fim:")
print((customers["customer_city"] !=
customers["customer_city"].str.strip()).sum())

print("\nCidades com letras maiúsculas:")
print(customers["customer_city"].str.contains(r"[A-Z]").sum())

print("\nCidades distintas depois de padronizar (strip + lower):")
print(customers["customer_city"].str.strip().str.lower().nunique())

#%%
# CEP: conferir o tipo (se for int64, perdeu zero à esquerda)
print("\nTipo do CEP:")
print(customers["customer_zip_code_prefix"].dtype)

print("\nCEPs com menos de 5 dígitos:")
print((customers["customer_zip_code_prefix"].astype(str).str.len() < 5).sum())

#%%
# 1. Padronizar CEP para 5 dígitos (prefixo)
customers['customer_zip_code_prefix'] = customers['customer_zip_code_prefix'].astype(str).str.zfill(5)
print(customers[['customer_zip_code_prefix']])

#%%
# 2. Verificar CEPs com menos de 5 dígitos após padronização
print("CEPs com menos de 5 dígitos após padronizaçao:")
cep_invalidos = (customers["customer_zip_code_prefix"].str.len() <5).sum()
print(cep_invalidos)

#%%
# 3. Verificar customer_id duplicados
print("\nCustomer_id duplicados:")
print(customers['customer_id'].duplicated().sum())

#%%
# 4. Resumo final
print("\n=== RESUMO CUSTOMERS ===")
print(f"Linhas totais: {len(customers)}")
print(f"Clientes únicos (customer_unique_id): {customers['customer_unique_id'].nunique()}")
print(f"Customer_id únicos: {customers['customer_id'].nunique()}")
print(f"Estados distintos: {customers['customer_state'].nunique()}")
print(f"Cidades distintas: {customers['customer_city'].nunique()}")
print(f"CEPs distintos: {customers['customer_zip_code_prefix'].nunique()}")
print(f"CEPs inválidos (< 5 dígitos): {cep_invalidos}")

#%%
#Salvar tabela tratada em novo arquivo CSV
customers.to_csv("../dados/clientes_limpos_tratados.csv", index=False, encoding='utf-8-sig')

#%%
# Importa a biblioteca para trabalhar com caminhos de arquivos
from pathlib import Path
# Importa o Pandas para ler e conferir os dados
import pandas as pd

# Define onde o arquivo salvo está localizado
caminho_arquivo = Path("../dados/clientes_limpos_tratados.csv")

# Verifica se o arquivo foi criado/existe na pasta
print("Arquivo existe na pasta?", caminho_arquivo.exists())

# Se o arquivo existir, faz a conferência do conteúdo
if caminho_arquivo.exists():
    # Carrega o arquivo salvo de volta para verificar
    clientes_conferencia = pd.read_csv(caminho_arquivo)
    
    # Mostra o tamanho: quantidade de linhas e colunas
    print(f"Tamanho da tabela salva: {clientes_conferencia.shape}")
    print("Arquivo salvo e conferido com sucesso!")
else:
    # Avisa se o arquivo não foi encontrado
    print(" Arquivo NÃO encontrado — verifique o caminho e o nome.")

