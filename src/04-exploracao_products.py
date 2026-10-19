#%%
import pandas as pd

# 1. Carregar tabela de produtos
products = pd.read_csv("../dados/olist_products_dataset.csv")

# Visualizar as primeiras linhas
print(products.head())

#%%
# 2. Ver quantidade de linhas e colunas
print("\nDimensões:")
print(products.shape)

#%%
# 3. Ver nomes e tipos das colunas
print("\nInformações:")
products.info()

#%%
# 4. Ver valores nulos por colunas
print("\nValores nulos:")
print(products.isnull().sum())

#%%
# 5. Resolver os valores nulos

# 5.1  Categoria vazia → damos um nome explicito
products["product_category_name"] = products["product_category_name"].fillna("sem_categoria")

# 5.2 Nome, descrição, fotos vazios → preenchemos com 0
colunas_texto = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty"
]
products[colunas_texto] = products[colunas_texto].fillna(0)

# 5.3 Peso e dimensões vazios → preenchemos com 0
colunas_medidas = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]
products[colunas_medidas] = products[colunas_medidas].fillna(0)

# 5.4 Conferir se zerou tudo 
print("Valores nulos após tratamento:")
print(products.isna().sum())


#%%
# 5. Verificar produtos duplicados pelo ID (esperado: 0)
print("\nproduct_id duplicados:")
print(products["product_id"].duplicated().sum())

#%%
# 6. Salvar a tabela 

from pathlib import Path

caminho = Path("../dados/olist_products_dataset_limpos.csv")
products.to_csv(caminho, index=False, encoding="utf-8-sig")

print(f"Salvo: {caminho.exists()} | Tamanho: {products.shape}")




