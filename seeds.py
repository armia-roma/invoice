from datetime import date
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def seed_purchase_orders():
    db = SessionLocal()
    try:
        # Sample purchase orders
        sample_pos = [
            models.PurchaseOrder(
                date=date(2025, 5, 25),
                total=1500.50
            ),
            models.PurchaseOrder(
                date=date(2025, 5, 25),
                total=2750.75
            ),
            models.PurchaseOrder(
                date=date(2025, 5, 25),
                total=999.99
            ),
            models.PurchaseOrder(
                date=date(2025, 5, 24),
                total=3250.00
            ),
            models.PurchaseOrder(
                date=date(2025, 5, 23),
                total=1875.25
            )
        ]
        
        # Add all purchase orders
        db.add_all(sample_pos)
        db.commit()
        
        print("Successfully added sample purchase orders!")
        
        # Print the inserted POs
        all_pos = db.query(models.PurchaseOrder).all()
        for po in all_pos:
            print(f"PO ID: {po.id}, Date: {po.date}, Total: ${po.total:,.2f}")
            
    except Exception as e:
        print(f"Error seeding purchase orders: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    # Seed the database
    seed_purchase_orders()
