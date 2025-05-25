from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Enum
from database import Base
from sqlalchemy.orm import relationship

import enum


class InvoiceStatus(enum.Enum):
    valid = "Valid"
    pending = "Pending"


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    total = Column(Float, nullable=False)

    # relationship to invoices(One-to-Many)
    invoices = relationship("Invoice", back_populates="purchase_order")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    total = Column(Float, nullable=False)
    customer_id = Column(Integer, nullable=False)
    purchase_order_id = Column(Integer, ForeignKey(
        "purchase_orders.id"), nullable=False)
    status = Column(Enum(InvoiceStatus),
                    default=InvoiceStatus.pending, nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="invoices")
