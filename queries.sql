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
