import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Order, Product, OrderProductAssociation, ProductRackAssociation
from core.models.db_helper import db_helper


async def create_order(session: AsyncSession, title: str) -> Order:
    order = Order(title=title)

    session.add(order)
    await session.commit()

    return order


async def create_product(session: AsyncSession, title: str) -> Product:
    product = Product(title=title)

    session.add(product)
    await session.commit()

    return product


# async def create_orders_and_products(session: AsyncSession):
#     order_1 = await create_order(session, title="order_1")
#     order_2 = await create_order(session, title="order_2")
#
#     notebook = await create_product(session, title="Ноутбук")
#     telephone = await create_product(session, title="Телефон")
#     watch = await create_product(session, title="Часы")
#
#     order_1 = await session.scalar(
#         select(Order)
#         .where(Order.id == order_1.id)
#         .options(selectinload(Order.products))
#     )
#     order_2 = await session.scalar(
#         select(Order)
#         .where(Order.id == order_2.id)
#         .options(selectinload(Order.products))
#     )
#
#     order_1.products.append(notebook)
#     order_1.products.append(telephone)
#     order_2.products.append(notebook)
#     order_2.products.append(telephone)
#     order_2.products.append(watch)
#
#     await session.commit()


# async def get_orders_with_products(session: AsyncSession) -> list[Order]:
#     stmt = (
#         select(Order)
#         .options(
#             selectinload(Order.products),
#         )
#         .order_by(Order.id)
#     )
#     orders = await session.scalars(stmt)
#
#     return list(orders)


# async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
#     orders = await get_orders_with_products(session)
#     for order in orders:
#         print(order.id, order.title, "products:")
#         for product in order.products:  # type: Product
#             print("-", product.id, product.title)


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details)
            .joinedload(OrderProductAssociation.product)  # new
            .joinedload(Product.racks_products_details)  # new
            .joinedload(ProductRackAssociation.rack),  # new
        )
        .order_by(Order.id)
    )
    result = await session.execute(stmt)
    orders = result.scalars().fetchall()

    return list(orders)


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)

    for order in orders:
        print(order.id, order.title, "products:")
        for (
            order_product_detail
        ) in order.products_details:  # type: OrderProductAssociation
            racks_titles = [
                rack_assoc.rack.title
                for rack_assoc in order_product_detail.product.racks_products_details
            ]
            print(
                "-",
                order_product_detail.product.id,
                order_product_detail.product.title,
                "qty:",
                order_product_detail.count,
                "racks:",
                racks_titles,
            )


async def demo_m2m(session: AsyncSession):
    # await create_orders_and_products(session)
    # await demo_get_orders_with_products_through_secondary(session)
    await demo_get_orders_with_products_with_assoc(session)


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())


# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' db_test_case_go
