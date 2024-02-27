import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper


async def get_orders_with_products_assoc(session: AsyncSession, query: str):
    stmt = text(query)
    result = await session.execute(stmt)
    orders = result.fetchall()
    column_names = result.keys()  # Получаем имена столбцов
    orders_list = []
    for order in orders:
        order_dict = dict(zip(column_names, order))
        orders_list.append(order_dict)
    return orders_list


def generate_query(order_ids: list[int]) -> str:
    query = f"""
        with cte as (
            select opa.order_id,
                   opa.product_id,
                   opa.count as product_count
            from order_product_association opa
            where opa.order_id in {tuple(order_ids)}
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
        """
    return query


def print_orders(reorganized_orders):
    print("=+=+=+=")
    print(
        f"Страница сборки заказов {', '.join(str(order_id) for order_id in reorganized_orders[0].keys())}\n"
    )

    for item in reorganized_orders:
        rack_title = item["rack_title"]
        print(f"===Стеллаж {rack_title}")

        for order_id, products in item.items():
            if isinstance(order_id, int):
                for product_id, product_info in products.items():
                    product_title = product_info["product_title"]
                    product_count = product_info["product_count"]
                    additional_racks = product_info["additional_racks"]
                    additional_racks_str = (
                        ", ".join(additional_racks) if additional_racks else ""
                    )

                    print(f"{product_title} (id={product_id})")
                    print(f"заказ {order_id}, {product_count} шт")
                    if additional_racks_str:
                        print(f"доп стеллаж: {additional_racks_str}")
                    print()


async def reorganize_orders(orders):
    reorganized_orders = []

    for order in orders:
        rack_title = order["rack_title"]
        order_id = order["order_id"]
        product_id = order["product_id"]
        product_title = order["product_title"]
        product_count = order["product_count"]
        is_primary = order["is_primary"]

        # Создаем словарь для хранения информации о товаре
        product_info = {
            "product_id": product_id,
            "product_title": product_title,
            "product_count": product_count,
            "additional_racks": [],
        }

        # Проверяем, является ли стеллаж основным
        if is_primary:
            # Поиск или создание элемента для текущего стеллажа
            found = False
            for item in reorganized_orders:
                if item["rack_title"] == rack_title:
                    found = True
                    if order_id not in item:
                        item[order_id] = {product_id: product_info}
                    elif product_id not in item[order_id]:
                        item[order_id][product_id] = product_info
                    else:
                        item[order_id][product_id]["product_count"] += product_count
                    break

            if not found:
                reorganized_orders.append(
                    {"rack_title": rack_title, order_id: {product_id: product_info}}
                )
        else:
            # Добавляем дополнительный стеллаж для продукта
            for item in reorganized_orders:
                if order_id in item and product_id in item[order_id]:
                    item[order_id][product_id]["additional_racks"].append(rack_title)
                    break

    return reorganized_orders


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    order_ids = [10, 11, 14, 15]
    query = generate_query(order_ids)
    orders = await get_orders_with_products_assoc(session, query)
    reorganized_orders = await reorganize_orders(orders)
    print_orders(reorganized_orders)


async def main():
    async with db_helper.session_factory() as session:
        await demo_get_orders_with_products_with_assoc(session)


if __name__ == "__main__":
    asyncio.run(main())
