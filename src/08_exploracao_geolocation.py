#%%
import pandas as pd
from pathlib import Path

# Carregar a tabela de geococalização
geo = pd.read_csv("../dados/olist_geolocation_dataset.csv")

# 1. Visualizar as primeiras linhas da tabela
print(geo.head())

#%%
# 2. Ver quantidades de linhas e colunas
print("\nDimensões:", geo.shape)

#%%
# 3. ver valores nulos por colunas
print("Valores nulos:")
print(geo.isna().sum())

#%%
# 4. Padronizar CEP
geo['geolocation_zip_code_prefix'] = (
    geo['geolocation_zip_code_prefix']
    .astype(str)
    .str.zfill(5)
)

# Agrupar por CEP — vários pontos → 1 ponto representativo por CEP
geo_agregado = geo.groupby('geolocation_zip_code_prefix', as_index=False).agg({
    'geolocation_lat': 'median',
    'geolocation_lng': 'median',
    'geolocation_city': 'first',
    'geolocation_state': 'first'
})

print(f"\nPontos originais: {len(geo)} → CEPs únicos: {len(geo_agregado)}")

#%%
# 5. Salvar 
caminho = Path("../dados/olist_geolocation_dataset_limpos.csv")
geo_agregado.to_csv(caminho, index=False, encoding="utf-8-sig")
print(f"Salvo: {caminho.exists()} | Tamanho final: {geo_agregado.shape}")

