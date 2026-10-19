#%%
import pandas as pd

# 1. Carregar tabela de itens de pedidos
order_items = pd.read_csv("../dados/olist_order_items_dataset.csv")

# Visualizar as primeiras linhas
print(order_items.head())

#%%
# 2. Verificar estrutura e tipos de dados
print("\nInformações ")
order_items.info()  # não precisa de print()

#%%
# 3. Converter data limite de postagem de texto para formato de data
order_items['shipping_limit_date'] = pd.to_datetime(order_items['shipping_limit_date'])
print("\nTipo após conversão:", order_items['shipping_limit_date'].dtype)

#%%
# 4. Verificar dados faltantes
print("\nValores nulos por coluna ")
print(order_items.isna().sum())

#%%
# 5. Verificar duplicatas de pedido (é normal repetir!)
print("\nRepetição de pedidos ")
print("order_id repetidos (ESPERADO > 0):", order_items['order_id'].duplicated().sum())

#%%
# 6. Tamanho total da tabela
print("\nDimensões ")
print(f"Linhas: {order_items.shape[0]}")
print(f"Colunas: {order_items.shape[1]}")

#%%
# 7. Resumo de valores numéricos
print("\nResumo de preços e fretes")
print(order_items[['price', 'freight_value']].describe())

#%%
# 8. Verificar chave única da tabela → pedido + número do item
duplica_chave = order_items.duplicated(subset=['order_id', 'order_item_id']).sum()
print("\nDuplicatas pela chave única (deve ser 0):", duplica_chave)

# Quantidades de valores distintos
print("\nValores distintos:")
print(f"Pedidos: {order_items['order_id'].nunique()}")
print(f"Produtos: {order_items['product_id'].nunique()}")
print(f"Vendedores: {order_items['seller_id'].nunique()}")

#%%
# 9. Verificar valores negativos (impossíveis)
print("\nValores inválidos")
print("Preços negativos (deve ser 0):", (order_items['price'] < 0).sum())
print("Frete negativo (deve ser 0):", (order_items['freight_value'] < 0).sum())

#%%
# 10. Salvar tabela limpa em novo arquivo
from pathlib import Path

# Caminho CERTO — sem barra no começo ✅
caminho_saida = Path("../dados/order_items_limpos.csv")

order_items.to_csv(caminho_saida, index=False, encoding='utf-8-sig')

# Conferir se deu certo
print(f"Arquivo salvo: {caminho_saida.exists()}")
print(f"Tamanho final: {order_items.shape}")








