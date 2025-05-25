from services.invoice import create_invoice
from typing import Annotated
from fastapi import FastAPI, UploadFile, Depends, HTTPException
import boto3
import os
from utils.csv_reader import read_csv
from database import engine, get_db
from sqlalchemy.orm import Session
import models
from zeep import Client
from dotenv import load_dotenv
load_dotenv(override=True)

SOAP_WSDL_URL = os.getenv("SOAP_WSDL_URL")

db_dependency = Annotated[Session, Depends(get_db)]
s3_client = boto3.client("s3")

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

S3_BUCKET_NAME = "fast-api-upload-files"


@app.get("/")
def read_root():

    return {"Hello": "World"}


def save_file_locally(file_path: str, contents: bytes):
    with open(file_path, "wb") as buffer:
        buffer.write(contents)


def upload_to_s3(filename: str, contents: bytes):
    s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=filename, Body=contents)


@app.post("/upload")
async def upload_file(file: UploadFile, db: db_dependency):
    filename = file.filename
    if not filename:
        return {"error": "File is required"}
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    # Read file
    contents = await file.read()

    # Upload file local and S3
    save_file_locally(file_path, contents)
    try:
        upload_to_s3(filename, contents)
    except Exception as e:
        print(f"S3 upload failed: {e}")
    # read csv and create invoice
    reader = read_csv(contents)
    invoice = create_invoice(reader, db)

    # SOAP call for number to words
    try:
        client = Client(SOAP_WSDL_URL)
        soap_result = client.service.NumberToWords(invoice.total)
        print(soap_result)
        invoice.status = "valid"
        db.commit()
        db.refresh(invoice)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")
    return invoice


@app.get("/reconcile")
async def reconcile(db: db_dependency):
    results = []
    purchase_orders = db.query(models.PurchaseOrder).all()
    for po in purchase_orders:
        invoice_total = sum(invoice.total for invoice in po.invoices)
        status = True if invoice_total == po.total else False
        results.append({
            "purchase_order_id": po.id,
            "purchase_order_total": po.total,
            "invoice_total": invoice_total,
            "reconciled": status
        })
    return results
