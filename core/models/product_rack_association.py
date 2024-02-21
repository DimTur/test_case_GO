from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .product import Product
    from .rack import Rack


class ProductRackAssociation(Base):
    __tablename__ = "product_rack_association"
    __table_args__ = (
        UniqueConstraint(
            "rack_id",
            "product_id",
            name="idx_unique_product_rack",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    rack_id: Mapped[int] = mapped_column(ForeignKey("racks.id"))

    product: Mapped["Product"] = relationship(back_populates="racks_products_details")
    rack: Mapped["Rack"] = relationship(back_populates="products_racks_details")
