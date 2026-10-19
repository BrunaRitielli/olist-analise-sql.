#%%
import pandas as pd

orders = pd.read_csv("../dados/olist_orders_dataset_limpos.csv")
order_items = pd.read_csv("../dados/olist_order_items_dataset.csv")
products = pd.read_csv("../dados/olist_products_dataset_limpos.csv")
sellers = pd.read_csv("../dados/olist_sellers_dataset.csv")
reviews = pd.read_csv("../dados/olist_order_reviews_dataset_limpos.csv")
payments = pd.read_csv("../dados/olist_order_payments_dataset_limpos.csv")
customers = pd.read_csv("../dados/clientes_limpos_tratados.csv")
geolocation = pd.read_csv("../dados/olist_geolocation_dataset_limpos.csv")

print("Todas as tabelas carregadas com sucesso")

# %%
import sqlite3

conn = sqlite3.connect("../dados/olist.db")

orders.to_sql("olist_orders_dataset_limpos", conn, if_exists="replace", index=False)
order_items.to_sql("olist_order_items_dataset", conn, if_exists="replace", index=False)
products.to_sql("olist_products_dataset_limpos", conn, if_exists="replace", index=False)
sellers.to_sql("olist_sellers_dataset", conn, if_exists="replace", index=False)
reviews.to_sql("olist_order_reviews_dataset_limpos", conn, if_exists="replace", index=False)
payments.to_sql("olist_order_payments_dataset_limpos", conn, if_exists="replace", index=False)
customers.to_sql("clientes_limpos_tratados", conn, if_exists="replace", index=False)
geolocation.to_sql("olist_geolocation_dataset_limpos", conn, if_exists="replace", index=False)

tabelas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)["name"]
for t in tabelas:
    n = pd.read_sql(f"SELECT COUNT(*) AS n FROM {t}", conn)["n"][0]
    print(f"{t}: {n} linhas")

conn.close()
print("\nBanco olist.db criado com sucesso")
# %%
