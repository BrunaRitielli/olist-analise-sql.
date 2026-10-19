#%%
import pandas as pd
from pathlib import Path

# 1. Carregar a tabela
sellers = pd.read_csv("../dados/olist_sellers_dataset.csv")

# Visualizar as primeiras linhas da tabela
print(sellers.head())

#%%
# 2. Ver quantidade de linhas e colunas
print("\nDimensões:")
print(f"Linhas: {sellers.shape[0]}")
print(f"Colunas: {sellers.shape[1]}")

#%%
# 3. Ver nomes e tipos das colunas
print("\nInformações:")
sellers.info()

#%%
# 4. Verificar valores nulos
print("\nValores nulos:")
print(sellers.isna().sum())

#%%
# 5. Verificar as duplicatas
print("Vendedores Duplicados")
duplicatas = sellers["seller_id"].duplicated().sum()
print(duplicatas)

#%%
# 6. Ver quantos dígitos tem o Cep
sellers['tamanho_cep'] = sellers['seller_zip_code_prefix'].astype(str).str.len()
print("Quantidade de dígitos:")
print(sellers['tamanho_cep'].value_counts().sort_index())

#%%
# 7. Padronizar CEP
sellers["seller_zip_code_prefix"] = (
    sellers["seller_zip_code_prefix"]
    .astype(str)
    .str.zfill(5)
)
print("Cep padronizado para 5 dígitos")


#%%
# 8. Salvar
caminho_saida = Path("../dados/olist_sellers_dataset_limpos.csv")
sellers.to_csv(caminho_saida, index=False, encoding="utf-8-sig")

print(f"Arquivo salvo: {caminho_saida.exists()}")
print(f"Tamanho final: {sellers.shape}")
# %%
