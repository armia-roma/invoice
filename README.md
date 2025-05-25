# Invoice Management System

A FastAPI-based invoice management system that handles file uploads, invoice processing, and purchase order reconciliation.

## Features

-   File upload handling (both local storage and AWS S3)
-   CSV invoice processing
-   Purchase order reconciliation
-   SOAP integration for number-to-words conversion
-   MySQL database integration
-   RESTful API endpoints

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd invoice
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```

3. Install required packages:

```bash
pip install fastapi uvicorn sqlalchemy pymysql python-multipart boto3 zeep python-dotenv alembic
```

## Configuration

1. Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/invoice
SOAP_WSDL_URL=your_soap_wsdl_url
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

2. Create S3 bucket:

    - Sign in to AWS Console
    - Go to S3 service
    - Click "Create bucket"
    - Enter bucket name: `fast-api-upload-files`
    - Choose your preferred region
    - Keep other settings as default (or adjust based on your security requirements)
    - Click "Create bucket"

3. Initialize the database:

```bash
alembic upgrade head
```

4. Seed the database with sample purchase orders:

```bash
python seeds.py
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

-   `GET /`: Root endpoint (Hello World)
-   `POST /upload`: Upload and process invoice files
-   `GET /reconcile`: Reconcile purchase orders with invoices

## API Documentation

Once the application is running, you can access:

-   Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
