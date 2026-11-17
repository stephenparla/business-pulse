# Business Pulse API

A learning project for **BubbleSort AI**. Business Pulse is an early-stage, read-only business intelligence API that will help a business owner understand key metrics such as revenue, orders, customers, and outstanding receivables.

The project uses fictional company data during development.

## Goals

- Build REST APIs with Python and FastAPI.
- Store business data in PostgreSQL using SQLModel.
- Calculate business metrics with validated, deterministic queries.
- Prepare the API for a future read-only AI assistant that retrieves facts through approved tools.

## Tech stack

- Python
- FastAPI
- SQLModel / SQLAlchemy
- PostgreSQL
- Pydantic
- pytest (testing)

## Initial data model

The initial database contains these tables:

- `organizations` — businesses using the platform.
- `customers` — customers belonging to an organization.
- `orders` — customer orders.
- `order_items` — products and quantities within an order.
- `invoices` — invoices issued to customers.
- `payments` — payments received.
- `payment_allocations` — amounts applied from payments to invoices.

Tenant-owned records include an `organization_id` so data can be isolated by business.

## Getting started

### 1. Create a PostgreSQL database

```sql
CREATE DATABASE bubblesort_pulse_dev;
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If a `requirements.txt` file exists:

```bash
pip install -r requirements.txt
```

Typical dependencies for this project include `fastapi`, `uvicorn[standard]`, `sqlmodel`, `psycopg[binary]`, and `python-dotenv` (or `pydantic-settings` for configuration).

### 4. Configure the database connection

Create a local `.env` file and set your connection string. Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/bubblesort_pulse_dev
```

Replace the username and password with your local PostgreSQL credentials. Do not commit `.env` or real credentials to source control.

### 5. Run the API

From the project root, run:

```bash
uvicorn app.main:app --reload
```

Update `app.main:app` if your FastAPI application is located elsewhere.

Open the interactive API documentation at:

- http://127.0.0.1:8000/docs

## Initial API scope

The first business metrics endpoints are planned to cover:

```text
GET /business/revenue-summary
GET /business/order-summary
GET /business/top-customers
GET /business/receivables
```

These endpoints should calculate results from PostgreSQL using predefined, parameterized queries. The database account used by the AI assistant should be read-only.

## Example API calls

After the app starts, the first call can create the fictional organization and customer data:

```bash
curl -X POST "http://127.0.0.1:8000/business/seed-data"
```

Example response:

```json
{
  "message": "fictional company and customer data inserted",
  "organization_id": "7d4d9b2e-0ba9-4f2a-a4f1-bc9c8e42d640",
  "organization_name": "Northwind Operations"
}
```

Use the returned `organization_id` in the summary queries:

```bash
curl "http://127.0.0.1:8000/business/revenue-summary?organization_id=7d4d9b2e-0ba9-4f2a-a4f1-bc9c8e42d640"
curl "http://127.0.0.1:8000/business/order-summary?organization_id=7d4d9b2e-0ba9-4f2a-a4f1-bc9c8e42d640"
curl "http://127.0.0.1:8000/business/top-customers?organization_id=7d4d9b2e-0ba9-4f2a-a4f1-bc9c8e42d640"
curl "http://127.0.0.1:8000/business/receivables?organization_id=7d4d9b2e-0ba9-4f2a-a4f1-bc9c8e42d640"
```

Example response shapes:

```json
{
  "organization_id": "7d4d9b2e-0ba9-4f2a-a4f1-bc9c8e42d640",
  "total_revenue": 4555.5,
  "paid_revenue": 3795.0,
  "outstanding_revenue": 760.5,
  "invoice_count": 4
}
```

```json
{
  "organization_id": "7d4d9b2e-0ba9-4f2a-a4f1-bc9c8e42d640",
  "total_orders": 4,
  "completed_orders": 3,
  "pending_orders": 1,
  "cancelled_orders": 0,
  "total_order_value": 4765.5,
  "average_order_value": 1191.375
}
```

```json
[
  {
    "customer_id": "b9b83c98-7d72-4b94-9b8b-6f0eb418f65d",
    "customer_code": "APEX-001",
    "customer_name": "Apex Retail",
    "total_revenue": 945.0,
    "order_count": 1
  }
]
```

```json
[
  {
    "customer_id": "9aa8c463-1fd6-4e2a-a1d3-33d6d3fa7ad6",
    "customer_code": "REDWOOD-004",
    "customer_name": "Redwood Logistics",
    "outstanding_amount": 1837.5,
    "invoice_count": 1
  }
]
```

## Development principles

- Keep API routes, business logic, database access, and SQLModel table definitions separate.
- Use `Decimal` for monetary values; avoid floating-point arithmetic for currency.
- Validate request parameters and use parameterized SQL.
- Scope every tenant-owned query by `organization_id`.
- Do not let an LLM execute arbitrary SQL.
- Keep AI responses grounded in results returned by approved application functions.
- Use database migrations (for example, Alembic) as the schema evolves.
- Use fictional or synthetic data until a customer explicitly authorizes data access.

## Project status

Early development / learning MVP. The database-backed API is being built first. LLM tool calling, MCP integration, Business DNA, and agentic capabilities are future steps—not prerequisites for the initial API.
