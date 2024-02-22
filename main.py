import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Order, Product, OrderProductAssociation, ProductRackAssociation
from core.models.db_helper import db_helper


async def get_orders_with_products_assoc(
    session: AsyncSession, order_ids: list[int]
) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details)
            .joinedload(OrderProductAssociation.product)
            .joinedload(Product.racks_products_details)
            .joinedload(ProductRackAssociation.rack)
        )
        .filter(Order.id.in_(order_ids))
        .order_by(Order.id)
    )
    result = await session.execute(stmt)
    orders = result.scalars().fetchall()
    return list(orders)


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    order_ids = [10, 11, 14, 15]
    orders = await get_orders_with_products_assoc(session, order_ids)

    print("=+=+=+=")
    print(f"Страница сборки заказов {', '.join(map(str, order_ids))}\n")

    racks_products = {}

    for order in orders:
        for order_product_detail in order.products_details:
            product = order_product_detail.product
            rack_title = None
            for rack_assoc in product.racks_products_details:
                if rack_assoc.is_primary:
                    rack_title = rack_assoc.rack.title
                    break
            if rack_title:
                if rack_title not in racks_products:
                    racks_products[rack_title] = []
                racks_products[rack_title].append(order_product_detail)

    for rack_title, products in racks_products.items():
        print(f"===Стеллаж {rack_title}")
        for product_detail in products:
            product = product_detail.product
            print(
                f"{product.title} (id={product.id})\n"
                f"заказ {product_detail.order.id}, {product_detail.count} шт"
            )
            additional_racks = []
            for rack_assoc in product.racks_products_details:
                if not rack_assoc.is_primary:
                    additional_racks.append(rack_assoc.rack.title)
            if additional_racks:
                print(f"доп стеллаж: {', '.join(additional_racks)}")
            print()


async def demo_m2m(session: AsyncSession):
    await demo_get_orders_with_products_with_assoc(session)


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())
