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
