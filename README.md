#  Análise de Dados: E-commerce Brasileiro (Olist)

##  Sobre o Projeto
Análise de cerca de 100 mil pedidos do e-commerce brasileiro Olist (2016-2018). Os dados foram validados em Python, gravados em um banco SQLite e analisados em SQL para responder 4 perguntas de negócio.

##  Conjunto de Dados
Fonte: Olist Brazilian E-Commerce Public Dataset (Kaggle).

##  Fluxo do Projeto
1. **Python (pandas):** validação e preparação de cada tabela
2. **Python (sqlite3):** gravação das tabelas tratadas no `olist.db`
3. **SQL (VS Code + SQLTools):** 4 queries de análise

##  Etapa 1: Validação e Preparação dos Dados

| Tabela | Principais tratamentos |
|---|---|
| Clientes |`olist_customers_dataset.csv` | CEP padronizado para 5 dígitos; `customer_id` sem duplicados; 27 estados e 4.119 cidades validados. Os 3.345 repetidos em `customer_unique_id` não são erro: são clientes que compraram mais de uma vez (96.096 clientes únicos). |
| Pedidos |`olist_orders_dataset.csv` | Datas convertidas para `datetime`; nulos tratados com justificativa; `order_id` confirmado como único. |
| Itens do pedido | `olist_order_items_dataset.csv` |Chave composta `order_id` + `order_item_id` validada como única; nenhum valor negativo; produtos e vendedores distintos conferidos. |
| Produtos | `olist_products_dataset.csv` | 610 produtos sem categoria, mantidos e rotulados como 'sem_categoria' nas consultas para não perder vendas; nulos numéricos preservados para não distorcer médias. |
| Vendedores |`olist_sellers_dataset.csv` | CEP padronizado para 5 dígitos; sem duplicados por `seller_id`; sem nulos. |
| Avaliações | `olist_order_reviews_dataset.csv` | Notas validadas na escala de 1 a 5; nulos conferidos; `review_id` não é chave única, então um pedido pode ter mais de uma avaliação. |
| Pagamentos |  `olist_order_payments_dataset.csv` | Validação de nulos e de valores negativos em `payment_value` e `payment_installments`, sem problemas encontrados. Um pedido pode ter mais de um pagamento, por isso a receita é somada por pedido. |
| Geolocalização | `olist_geolocation_dataset.csv` | CEP convertido para texto com 5 dígitos; vários pontos por CEP agrupados com a mediana de latitude e longitude. Preparada, mas não utilizada nas 4 análises finais. |


> Os cálculos de atraso (data de entrega menos data prevista) e de valores são feitos diretamente nas queries SQL, não foram salvos nos CSVs.

## Etapa 2: Perguntas e Respostas

### Pergunta 1: Como a receita evoluiu mês a mês?
- **Método:** junção de pedidos e pagamentos, apenas pedidos entregues, agrupamento por mês e `LAG()` para o crescimento percentual
- **Resultado:** crescimento forte ao longo de 2017, com pico em novembro de 2017 (cerca de R$ 1,15 milhão); em 2018 a receita se estabilizou em torno de R$ 1 milhão por mês
- **Atenção:** 2016 tem pouquíssimos pedidos (dezembro/2016: R$ 19,62), o que gera um crescimento percentual sem significado em janeiro de 2017. Esse período foi tratado como baixo volume
- **Insight:** o negócio ganhou tração em 2017. O pico de novembro possivelmente reflete a Black Friday (hipótese)

### Pergunta 2: Quais categorias geram mais receita?
- **Método:** junção de 3 tabelas, soma do preço por categoria e participação percentual com `SUM() OVER ()` (Top 10)
- **Resultado:**

| Categoria | Receita | % do total |
|---|---|---|
| beleza_saude | R$ 1.233.131,72 | 9,3% |
| relogios_presentes | R$ 1.166.176,98 | 8,8% |
| cama_mesa_banho | R$ 1.023.434,76 | 7,7% |
| esporte_lazer | R$ 954.852,55 | 7,2% |
| informatica_acessorios | R$ 888.724,61 | 6,7% |
| moveis_decoracao | R$ 711.927,69 | 5,4% |
| utilidades_domesticas | R$ 615.628,69 | 4,7% |
| cool_stuff | R$ 610.204,10 | 4,6% |
| automotivo | R$ 578.966,65 | 4,4% |
| brinquedos | R$ 471.286,48 | 3,6% |

- **Insight:** as 5 primeiras categorias concentram cerca de 40% da receita e as 10 primeiras cerca de 62%: a receita é bem concentrada em poucas categorias

### Pergunta 3: Atraso na entrega derruba a nota de avaliação?
- **Método:** `JULIANDAY()` para a diferença de datas, `CASE WHEN` para faixas de atraso e média das notas

| Situação da entrega | Avaliações | Nota média |
|---|---|---|
| No prazo | 89.944 | 4,29 |
| Atraso de 1 a 3 dias | 1.856 | 3,29 |
| Atraso de 4 a 7 dias | 1.756 | 2,10 |
| Atraso de mais de 7 dias | 2.797 | 1,70 |

- **Insight:** quanto maior o atraso, menor a nota (queda de até 2,6 pontos). Os atrasos são cerca de 7% das avaliações, mas concentram as piores notas. Isso mostra forte associação, mas não prova sozinho que o atraso é a única causa

### Pergunta 4: Quem são os melhores vendedores por categoria?
- **Método:** `RANK() OVER (PARTITION BY categoria ORDER BY receita DESC)`, mostrando o 1º colocado de cada categoria (Top 10 por receita)

| Categoria | Vendedor (id) | Receita | Pedidos | Ticket médio |
|---|---|---|---|---|
| relogios_presentes | 4869f7a5... | R$ 198.822,03 | 974 | R$ 204 |
| moveis_escritorio | 7c67e144... | R$ 171.605,82 | 882 | R$ 195 |
| pcs | 53243585... | R$ 163.322,76 | 143 | R$ 1.142 |
| cama_mesa_banho | 4a3ca931... | R$ 162.206,95 | 1.431 | R$ 113 |
| cool_stuff | 7a67c85e... | R$ 133.408,69 | 1.051 | R$ 127 |
| moveis_decoracao | 1025f0e2... | R$ 110.770,46 | 785 | R$ 141 |

- **Insight:** há vendedores que ganham por volume (cama_mesa_banho: 1.431 pedidos a R$ 113 em média) e outros por valor do produto (pcs: 143 pedidos a R$ 1.142 em média)

## Decisões e Limitações
- Todas as análises consideram apenas pedidos com status `delivered`
- A pergunta 1 usa o valor de pagamentos (inclui frete); as perguntas 2 e 4 usam o preço dos itens (sem frete)
- Os 610 produtos sem categoria foram mantidos na base; não aparecem no Top 10 de categorias
- Um pedido pode ter mais de uma avaliação, então o número de avaliações pode ser maior que o de pedidos

## Ferramentas Utilizadas
- **Python / pandas:** validação e preparação dos dados
- **SQLite / SQL:** consultas, agrupamentos e análises
- **VS Code + SQLTools:** ambiente de desenvolvimento

## Técnicas de SQL
`JOIN`, `GROUP BY`, CTE, `CASE WHEN`, funções de janela (`LAG`, `RANK`, `SUM() OVER`), funções de data do SQLite (`STRFTIME`, `JULIANDAY`) e `LIMIT`.

## Como Reproduzir
1. Baixe o dataset da Olist no Kaggle e coloque os CSVs em `dados/`
2. Rode o tratamento em Python
3. Rode `src/02_criar_banco.py` para gerar o `olist.db`
4. Conecte o SQLTools ao `olist.db` e rode `src/analise.sql`

## Conclusão
Os dados foram validados com critério, as decisões sobre nulos foram justificadas e as análises mostraram padrões claros de receita, concentração por categoria, impacto da logística na satisfação e perfis diferentes de vendedores.

---

**Autora:** Bruna Ritielli - Cientista de dados
**LinkedIn:** linkedin.com/in/bruna-ritielli
**Data:** Outubro/2026
