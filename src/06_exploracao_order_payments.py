#%%
import pandas as pd
from pathlib import Path

# 1. Carregar a tabela de pagamentos
payments = pd.read_csv("../dados/olist_order_payments_dataset.csv")

# Mostrar as primeiras linhas da tabela
print(payments.head())

#%%
# 2. Ver quantidade de linhas e colunas
print("\nDimensões:", payments.shape)

#%%
# 3. Ver valores nulos por colunas
print("\nValores nulos:")
print(payments.isna().sum())

#%%
# 4. Validações
print("\nValores negativos no valor:")
print((payments["payment_value"] <0).sum())

print("\nParcelas:")
print((payments["payment_installments"]<0).sum())


#%%
# 5. Salvar 
caminho = Path("../dados/olist_order_payments_dataset_limpos.csv")
payments.to_csv(caminho, index=False, encoding="utf-8-sig")
print(f"\nSalvo: {caminho.exists()} | Tamanho: {payments.shape}")

