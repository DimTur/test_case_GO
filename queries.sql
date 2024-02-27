SELECT
  order_product_association.order_id AS order_product_association_order_id,
  order_product_association.id AS order_product_association_id,
  order_product_association.product_id AS order_product_association_product_id,
  order_product_association.count AS order_product_association_count,
  racks_1.id AS racks_1_id,
  racks_1.title AS racks_1_title,
  product_rack_association_1.id AS product_rack_association_1_id,
  product_rack_association_1.is_primary AS product_rack_association_1_is_primary,
  product_rack_association_1.product_id AS product_rack_association_1_product_id,
  product_rack_association_1.rack_id AS product_rack_association_1_rack_id,
  products_1.id AS products_1_id,
  products_1.title AS products_1_title
FROM
  order_product_association
  LEFT OUTER JOIN products AS products_1 ON products_1.id = order_product_association.product_id
  LEFT OUTER JOIN product_rack_association AS product_rack_association_1 ON products_1.id = product_rack_association_1.product_id
  LEFT OUTER JOIN racks AS racks_1 ON racks_1.id = product_rack_association_1.rack_id
WHERE
  order_product_association.order_id IN (10,11,14,15)

--
SELECT
  order_product_association.order_id AS с,
  order_product_association.count AS order_product_association_count,
  racks_1.title AS racks_1_title,
  product_rack_association_1.is_primary AS product_rack_association_1_is_primary,
  products_1.id AS products_1_id,
  products_1.title AS products_1_title
FROM
  order_product_association
  LEFT OUTER JOIN products AS products_1 ON products_1.id = order_product_association.product_id
  LEFT OUTER JOIN product_rack_association AS product_rack_association_1 ON products_1.id = product_rack_association_1.product_id
  LEFT OUTER JOIN racks AS racks_1 ON racks_1.id = product_rack_association_1.rack_id
WHERE
  order_product_association.order_id IN (10,11,14,15)


--
with cte as (
    select opa.order_id,
           opa.product_id,
           opa.count as product_count
    from order_product_association opa
    where opa.order_id in (10, 11, 14, 15)
    )
select cte.order_id,
       cte.product_id,
       cte.product_count,
       p.title as product_title,
       r.id,
       r.title as rack_title,
       pra.is_primary
from cte
inner join products p on cte.product_id = p.id
inner join product_rack_association pra on p.id = pra.product_id
inner join racks r on pra.rack_id = r.id;