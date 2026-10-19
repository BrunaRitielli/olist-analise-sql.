#%%
import pandas as pd
from pathlib import Path

# 1. Carregar a tabela de pedidos
orders = pd.read_csv("../dados/olist_orders_dataset.csv")

# Visualizar a tabela
print(orders.head())

#%%
# 2. Quantidade de linhas e colunas
print("\nDimensões")
print(orders.shape)

#%%
# 3. Nomes e tipos das colunas
print("\nInformações gerais")
orders.info()

#%%
# 4. Verificar valores nulos por coluna
print("\nValores nulos por coluna ")
print(orders.isnull().sum())

#%%
# 5. Verificar duplicatas pelo ID do pedido
print("\nPedidos duplicados (deve ser 0):")
print(orders["order_id"].duplicated().sum())

#%%
# 6. Valores nulos por status do pedido
nulos_por_status = (
    orders.groupby("order_status")[
        [
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date"
        ]
    ]
    .apply(lambda x: x.isnull().sum())
    .reset_index()
)
print("\n=== Valores nulos por status ===")
print(nulos_por_status.to_string(index=False))

#%%
# 7. Converter TODAS as colunas de data para formato datetime
colunas_data = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]
for coluna in colunas_data:
    orders[coluna] = pd.to_datetime(orders[coluna], errors="coerce")

print("\n Tipos após conversão ")
print(orders.dtypes)

#%%
# Sobe 1 pasta de dentro de src/ e entra em dados/
caminho_saida = Path("../dados/olist_orders_dataset_limpos.csv")

orders.to_csv(caminho_saida, index=False, encoding="utf-8-sig")

print("Arquivo salvo:", caminho_saida.exists())
print("Tamanho final:", orders.shape)
# %%
