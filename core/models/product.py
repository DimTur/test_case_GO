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
    from .order import Order


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32), unique=True)
    orders: Mapped[list["Order"]] = relationship(
        secondary=order_product_association_table,
        back_populates="products",
    )
