# DushimeMart API

A cloud-ready REST API for an online grocery store, built as the final project for the **Introduction to Cloud Technologies** course at Vistula University.

- **Author:** Cleonide Dushime
- **Student ID:** 70871
- **Grade target:** MAX 4 (mature API + layered architecture + authentication)

---

## What it does

DushimeMart is a simple e-commerce backend that lets customers register, log in, browse a catalogue of grocery products, and place orders. It demonstrates a clean three-layer architecture (HTTP routers → business services → database models) with JWT-based authentication protecting write operations.

## Tech stack

- **FastAPI** — modern Python web framework with automatic OpenAPI/Swagger docs
- **SQLAlchemy 2.0** — ORM for database access
- **SQLite** — file-based database, zero setup required
- **JWT (python-jose)** — stateless authentication tokens
- **Bcrypt (passlib)** — secure password hashing
- **Pydantic v2** — request/response validation

## Project structure

```
dushimemart/
├── app/
│   ├── main.py              # FastAPI app + router registration
│   ├── config.py            # Settings loaded from .env
│   ├── database.py          # SQLAlchemy engine + session factory
│   ├── models.py            # ORM models (User, Product, Order)
│   ├── schemas.py           # Pydantic schemas (validation)
│   ├── security.py          # Password hashing + JWT helpers
│   ├── dependencies.py      # Reusable auth dependency
│   ├── routers/             # HTTP layer (controllers)
│   │   ├── auth_router.py
│   │   ├── products_router.py
│   │   └── orders_router.py
│   └── services/            # Business logic layer
│       ├── user_service.py
│       ├── product_service.py
│       └── order_service.py
├── requirements.txt
├── .env                     # Environment variables (secret key, DB URL)
├── seed.py                  # Optional: populate sample products
└── README.md
```

## How to run

1. Open a PowerShell terminal in the project folder.
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. (Optional) Populate sample products:
   ```powershell
   python seed.py
   ```
4. Start the server:
   ```powershell
   uvicorn app.main:app --reload
   ```
5. Open `http://localhost:8000/docs` in your browser to see the interactive Swagger UI.

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET    | `/`                  | —   | Health check |
| POST   | `/auth/register`     | —   | Register a new customer |
| POST   | `/auth/login`        | —   | Log in and receive JWT |
| GET    | `/products`          | —   | List all products |
| GET    | `/products/{id}`     | —   | Get one product |
| POST   | `/products`          | ✅  | Create a product |
| PUT    | `/products/{id}`     | ✅  | Update a product |
| DELETE | `/products/{id}`     | ✅  | Delete a product |
| GET    | `/orders`            | ✅  | List my orders |
| GET    | `/orders/{id}`       | ✅  | Get one of my orders |
| POST   | `/orders`            | ✅  | Place a new order |
| DELETE | `/orders/{id}`       | ✅  | Cancel an order |

## How error handling works

| HTTP code | When it triggers |
|-----------|------------------|
| **201**   | Resource successfully created |
| **204**   | Resource successfully deleted |
| **400**   | Business rule violation (e.g. duplicate email on register) |
| **401**   | Missing or invalid JWT token |
| **404**   | Requested resource does not exist |
| **422**   | Input validation failed (Pydantic) |

## Architectural notes

The project intentionally separates the HTTP layer (`routers/`) from business logic (`services/`). Routers know only about FastAPI, request shapes, and HTTP status codes. Services know only about the database and business rules. This makes the business logic easy to unit-test and easy to reuse if the project ever grows a second interface (CLI, GraphQL, etc.).

## License

This project was created for educational purposes as part of the Introduction to Cloud Technologies course at Vistula University.
