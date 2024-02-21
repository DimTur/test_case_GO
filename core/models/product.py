from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base

if TYPE_CHECKING:
    from .order_product_association import OrderProductAssociation
    from .product_rack_association import ProductRackAssociation


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32), unique=True)
    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product"
    )
    racks_products_details: Mapped[list["ProductRackAssociation"]] = relationship(
        back_populates="product"
    )
