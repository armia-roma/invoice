
import models
from schemas.invoice import Invoice
from fastapi import HTTPException, status
from dependencies import db_dependency
from typing import List
from pydantic import ValidationError


def create_invoice(data: List[dict], db: db_dependency):
    data = data[0]
    try:
        inv = Invoice.model_validate(data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    # Check purchase order existence
    po = db.query(models.PurchaseOrder).filter_by(
        id=inv.purchase_order_id).first()
    if not po:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase order with ID {inv.purchase_order_id} does not exist"
        )
    # Check invoice total does not exceed PO total
    if sum(invoice.total for invoice in po.invoices) + inv.total > po.total:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Total of invoices exceeds total of purchase order"
        )
    # Create  invoice

    new_invoice = models.Invoice(
        date=inv.date,
        total=inv.total,
        customer_id=inv.customer_id,
        purchase_order_id=inv.purchase_order_id
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice
