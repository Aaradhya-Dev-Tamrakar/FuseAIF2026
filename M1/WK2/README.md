# Classical Models API
**Fuse AI Fellowship 2026 - Week 2**

A fully refactored, 12-Factor App compliant RESTful API application for managing customer data, built with FastAPI and PostgreSQL.

## Overview

This API provides comprehensive endpoints for managing customer records, their associated orders and payments, as well as an extensive statistics module. The application demonstrates best practices for building modular, scalable REST APIs with Python, including database integration, environment configuration, containerization, and centralized logging.

## Tech Stack

- **Framework**: FastAPI 0.136.1
- **Server**: Uvicorn 0.46.0
- **ORM**: SQLAlchemy 2.0.49
- **Database**: PostgreSQL 16 (via psycopg2)
- **Data Validation**: Pydantic 2.13.4
- **Python**: 3.12+
- **Infrastructure**: Docker & Docker Compose

## Features (12-Factor App Ready)

- ✅ **Containerization**: Fully Dockerized with automatic database initialization and health checks.
- ✅ **Configuration**: Environment variables managed strictly via `.env` file (`pydantic-settings`).
- ✅ **Logging**: Centralized event-stream logging (`app/logger.py`) mapping to `stdout` and file.
- ✅ **Stateless**: The API service relies on the separate PostgreSQL container for state.
- ✅ **Modular Architecture**: Endpoints split logically into `router.py` and `stats_router.py`.
- ✅ **Rich Responses**: Relational database queries fetching nested associated data (e.g., fetching a customer includes their orders and payments).

## Project Structure

```text
├── main.py              # FastAPI application entry point
├── app/
│   ├── crud.py          # Centralized database query logic
│   ├── router.py        # Customer endpoints router
│   ├── employees_router.py # Employees endpoints router
│   ├── offices_router.py   # Offices endpoints router
│   ├── orderdetails_router.py # OrderDetails endpoints router
│   ├── orders_router.py    # Orders endpoints router
│   ├── payments_router.py  # Payments endpoints router
│   ├── productlines_router.py # ProductLines endpoints router
│   ├── products_router.py  # Products endpoints router
│   ├── stats_router.py  # Asynchronous Statistics endpoints router
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic validation schemas (V2 format)
│   ├── database.py      # Database connection and session management
│   ├── config.py        # Configuration settings
│   ├── logger.py        # Logging configuration
│   └── seed.sql         # Database initialization script
├── Dockerfile           # Docker image configuration (Python 3.12)
├── docker-compose.yml   # Multi-service orchestration (api & db)
├── pyproject.toml       # Project metadata and dependencies
└── requirements.txt     # Python dependencies
```

## Getting Started

### Prerequisites

- Docker and Docker Compose

### Running the Application

The absolute easiest and recommended way to run this project is via Docker Compose. It automatically spins up the database, runs the `seed.sql` script, and launches the API.

1. **Clone the repository and set up environment**
   Ensure your `.env` file has the appropriate variables without spaces around the equal signs:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password
   POSTGRES_DB=mydatabase
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```

2. **Start the services**
   ```bash
   docker compose up --build
   ```

The API will be mapped to your host machine's port `8080` to prevent conflicts.
Access it at: **http://localhost:8080**

*(Note: If you run into database initialization issues due to caching, wipe the volume with `docker compose down -v` and rebuild).*

## Interactive API Documentation

Once running, access the interactive API documentation at:
- **Swagger UI**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc**: [http://localhost:8080/redoc](http://localhost:8080/redoc)

## API Endpoints

### Customers Router (`/customers`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers/` | List all customers (supports pagination) |
| POST | `/customers/` | Create a new customer |
| GET | `/customers/{customer_id}` | Get customer by ID (includes orders/payments) |
| PUT | `/customers/{customer_id}` | Update customer information |
| DELETE | `/customers/{customer_id}` | Delete a customer |
| GET | `/customers/{customer_id}/orders` | Get all orders for a specific customer |
| GET | `/customers/{customer_id}/payments` | Get all payments for a specific customer |

### Employees Router (`/employees`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employees/` | List all employees (supports pagination) |
| POST | `/employees/` | Create a new employee |
| GET | `/employees/{employee_number}` | Get employee by ID |
| PUT | `/employees/{employee_number}` | Update employee information |
| DELETE | `/employees/{employee_number}` | Delete an employee |

### Offices Router (`/offices`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/offices/` | List all offices (supports pagination) |
| POST | `/offices/` | Create a new office |
| GET | `/offices/{office_code}` | Get office by code |
| PUT | `/offices/{office_code}` | Update office information |
| DELETE | `/offices/{office_code}` | Delete an office |

### OrderDetails Router (`/orderdetails`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orderdetails/` | List all order details (supports pagination) |
| POST | `/orderdetails/` | Create a new order detail |
| GET | `/orderdetails/{order_id}/{product_code}` | Get order detail by composite ID |
| PUT | `/orderdetails/{order_id}/{product_code}` | Update order detail information |
| DELETE | `/orderdetails/{order_id}/{product_code}` | Delete an order detail |

### Orders Router (`/orders`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders/` | List all orders (supports pagination) |
| POST | `/orders/` | Create a new order |
| GET | `/orders/{order_id}` | Get order by ID |
| PUT | `/orders/{order_id}` | Update order information |
| DELETE | `/orders/{order_id}` | Delete an order |

### Payments Router (`/payments`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/payments/` | List all payments (supports pagination) |
| POST | `/payments/` | Create a new payment |
| GET | `/payments/{customer_id}/{check_number}` | Get payment by composite ID |
| PUT | `/payments/{customer_id}/{check_number}` | Update payment information |
| DELETE | `/payments/{customer_id}/{check_number}` | Delete a payment |

### ProductLines Router (`/productlines`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/productlines/` | List all product lines (supports pagination) |
| POST | `/productlines/` | Create a new product line |
| GET | `/productlines/{product_line}` | Get product line by name |
| PUT | `/productlines/{product_line}` | Update product line information |
| DELETE | `/productlines/{product_line}` | Delete a product line |

### Products Router (`/products`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | List all products (supports pagination) |
| POST | `/products/` | Create a new product |
| GET | `/products/{product_code}` | Get product by code |
| PUT | `/products/{product_code}` | Update product information |
| DELETE | `/products/{product_code}` | Delete a product |

### Stats Router (`/stats`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stats/` | Concurrent async count of all rows across all tables |
| GET | `/stats/customers` | Count of customers |
| GET | `/stats/payments` | Count of payments |
| GET | `/stats/orders` | Count of orders |
| GET | `/stats/orderdetails` | Count of order details |
| GET | `/stats/productlines` | Count of product lines |
| GET | `/stats/products` | Count of products |
| GET | `/stats/offices` | Count of offices |
| GET | `/stats/employees` | Count of employees |

### General
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Application health check |
| GET | `/` | Welcome message |

## Week 3 (WK3) - Roadmap & Probable Implementations

The following features and enhancements are planned for Week 3:

### Core CRUD Operations
- ✅ Extend CRUD operations to **all tables** (currently limited to customers)
  - Orders, Payments, Products, ProductLines, Employees, Offices, OrderDetails
- ✅ Implement **count operations** across all tables
- ✅ Add **overall count** statistics endpoint for comprehensive data insights

### Query Intelligence
- 🔄 **Query Decomposition**: Parse complex user queries into structured components
  - Break down multi-table queries into logical units
  - Support for `JOIN` operations across related tables
  - Optimize query structure for execution

### Table & Schema Intelligence
- 🔄 **Table Detection**: Automatically identify which tables are needed for a query
- 🔄 **Column Management**: Support dynamic column selection and deletion
- 🔄 **Query Creation**: Generate optimized SQL queries from decomposed components

### Query Execution & LLM Integration
- 🔄 **Query Execution Engine**: Execute complex queries against the PostgreSQL backend
- 🔄 **LLM Response Layer**: 
  - Process query results through an LLM
  - Convert structured data into natural language responses
  - Provide intelligent data insights and summaries

### Architecture Evolution
The application will evolve from a simple CRUD API to an **AI-powered query interface** that understands natural language requests and intelligently queries the database.

## License

See LICENSE file for details.
