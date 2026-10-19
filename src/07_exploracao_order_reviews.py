#%%
import pandas as pd
from pathlib import Path

# 1. Carregar a tabela de avaliações
reviews = pd.read_csv("../dados/olist_order_reviews_dataset.csv")

# Visualizar as primeiras linhas da tabela
print(reviews.head())

#%%
# 2. Ver quantidades de linhas e colunas
print("\nDimensões:",reviews.shape)

#%%
# 3. Ver valores nulos por coluna
print("Valores nulos:")
print(reviews.isna().sum())

#%%
# 3.1 Preencher comentários vazios
reviews['review_comment_title'] = reviews['review_comment_title'].fillna("sem_titulo")
reviews['review_comment_message'] = reviews['review_comment_message'].fillna("sem_comentario")

#%%
# 4. Ver nomes e tipos das colunas
print("\nInformações:")
print(reviews.info())

#%%
# 4.1 Converter datas
colunas_data = ['review_creation_date', 'review_answer_timestamp']
for col in colunas_data:
    reviews[col] = pd.to_datetime(reviews[col], errors="coerce")
print("\nDatas convertidas")

#%%
# 5.  Salvar 
caminho = Path("../dados/olist_order_reviews_dataset_limpos.csv")
reviews.to_csv(caminho, index=False, encoding="utf-8-sig")
print(f"Salvo: {caminho.exists()} | Tamanho: {reviews.shape}")

