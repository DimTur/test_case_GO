from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .order_product_association import order_product_association_table

if TYPE_CHECKING:
    from .product import Product


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32), unique=True)
    products: Mapped[list["Product"]] = relationship(
        secondary=order_product_association_table,
        back_populates="orders",
    )
