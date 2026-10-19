--
-- =====================================================
-- PROJETO OLIST: ANÁLISE DE E-COMMERCE EM SQL
-- =====================================================
-- Perguntas de negócio respondidas neste arquivo:

-- 1. Como a receita evoluiu mês a mês?
-- 2. Quais categorias geram mais receita?
-- 3. Atraso na entrega derruba a nota de avaliação?
-- 4. Quem são os melhores vendedores por categoria?

--======================================================
-- PERGUNTA 1: Como a receita evoluiu mês a mês?
--======================================================

WITH mensal AS (
  SELECT
    STRFTIME('%Y-%m', o.order_purchase_timestamp) AS mes,
    SUM(p.payment_value) AS receita
  FROM olist_orders_dataset_limpos o
  JOIN olist_order_payments_dataset_limpos p
    ON p.order_id = o.order_id
  WHERE o.order_status = 'delivered'
  GROUP BY 1
)
SELECT
  mes,
  ROUND(receita, 2) AS receita,
  ROUND(
    100.0 * (receita - LAG(receita) OVER (ORDER BY mes))
    / LAG(receita) OVER (ORDER BY mes), 1
  ) AS crescimento_pct
FROM mensal
ORDER BY mes
LIMIT 6;


-- ==================================================
-- PERGUNTA 2: Quais categorias geram mais receita?
-- ==================================================
SELECT
  COALESCE(p.product_category_name, 'sem_categoria') AS categoria,
  ROUND(SUM(i.price), 2) AS receita,
  ROUND(100.0 * SUM(i.price) / SUM(SUM(i.price)) OVER (), 1) AS pct_do_total
FROM olist_order_items_dataset i
JOIN olist_orders_dataset_limpos o
  ON o.order_id = i.order_id
JOIN olist_products_dataset_limpos p
  ON p.product_id = i.product_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY receita DESC
LIMIT 10;

-- =====================================================
-- PERGUNTA 3: Atraso na entrega derruba a nota de avaliação?
-- =====================================================

WITH pedidos AS (
  SELECT
    o.order_id,
    JULIANDAY(DATE(o.order_delivered_customer_date))
      - JULIANDAY(DATE(o.order_estimated_delivery_date)) AS dias_diferenca
  FROM olist_orders_dataset_limpos o
  WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
),
faixas AS (
  SELECT
    order_id,
    CASE
      WHEN dias_diferenca <= 0 THEN '1. No prazo'
      WHEN dias_diferenca <= 3 THEN '2. Atraso de 1 a 3 dias'
      WHEN dias_diferenca <= 7 THEN '3. Atraso de 4 a 7 dias'
      ELSE '4. Atraso de mais de 7 dias'
    END AS situacao_entrega
  FROM pedidos
)
SELECT
  f.situacao_entrega,
  COUNT(*) AS avaliacoes,
  ROUND(AVG(r.review_score), 2) AS nota_media
FROM faixas f
JOIN olist_order_reviews_dataset_limpos r
  ON r.order_id = f.order_id
GROUP BY 1
ORDER BY 1;

-- =====================================================
-- PERGUNTA 4: Quem são os melhores vendedores por categoria?
-- =====================================================

WITH vendas AS (
  SELECT
    p.product_category_name AS categoria,
    i.seller_id,
    SUM(i.price) AS receita,
    COUNT(DISTINCT i.order_id) AS pedidos
  FROM olist_order_items_dataset i
  JOIN olist_orders_dataset_limpos o
    ON o.order_id = i.order_id
  JOIN olist_products_dataset_limpos p
    ON p.product_id = i.product_id
  WHERE o.order_status = 'delivered'
  GROUP BY 1, 2
),
ranking AS (
  SELECT
    categoria,
    seller_id,
    receita,
    pedidos,
    RANK() OVER (PARTITION BY categoria ORDER BY receita DESC) AS posicao
  FROM vendas
)
SELECT
  categoria,
  posicao,
  seller_id,
  ROUND(receita, 2) AS receita,
  pedidos
FROM ranking
WHERE posicao = 1
ORDER BY receita DESC
LIMIT 6;