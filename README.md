
# 🛒 Uniblox – Nth Order Coupon Simulator Assesment

## Overview

This project implements a simple ecommerce backend where users can:

* Add items to a cart
* Checkout to place an order
* Receive a **10% discount coupon on every global nth order**
* Apply a valid coupon during checkout

The system also exposes **admin APIs** to view aggregated statistics such as total purchases, revenue, and discounts.

The implementation focuses on **clean business logic, clarity, and testability**, using an **in-memory database** as allowed by the assignment.

---

## Tech Stack

* **FastAPI** – API framework
* **SQLAlchemy** – ORM
* **SQLite (in-memory)** – datastore
* **Pydantic** – request/response schemas
* **Uvicorn** – ASGI server

---

## Core Assumptions (Important)

> These assumptions are explicitly documented as allowed by the problem statement.

### 1. Nth Order Scope

* The **nth order is evaluated globally across the entire system**, not per user.
* A single global order counter is maintained.

### 2. Coupon Ownership

* Coupons are **per user**.
* A coupon is issued **only to the user who places the global nth order**.
* Coupons are **not shared** between users.

### 3. Coupon Validity & Replacement

* A coupon is **single-use**.
* A coupon is valid **only until the next global nth order occurs**.
* When the next nth order is reached:

  * Any unused coupons from the previous cycle are **automatically invalidated**
  * A new coupon cycle begins

### 4. No Blocking Behavior

* An unused coupon does **not** block the generation of future coupons.
* Coupon replacement happens strictly based on nth-order milestones.

### 5. Authentication & Authorization

* Authentication and RBAC are **intentionally out of scope**, as they were not required.
* Admin APIs are exposed without auth for demonstration purposes only.

---

## High-Level Control Flow

### User Journey (Happy Path)

1. **User adds items to cart**
2. **User checks out**
3. All cart items are converted into **one single order**
4. If a valid coupon is provided, it is applied to the entire order
5. Cart is cleared after successful checkout

---

## Detailed Checkout Flow

### Step 1: Add Items to Cart

```
POST /cart/{user_id}/add
```

Multiple products can be added.
Cart items are **accumulated**, not ordered yet.

---

### Step 2: Checkout (With or Without Coupon)

```
POST /checkout/{user_id}
```

Request body:

```json
{
  "coupon_code": ""
}
```

* `coupon_code` is optional
* Empty string (`""`) means no coupon applied

---

### Step 3: Order Creation

At checkout:

* All cart items are grouped into **one order**
* Total amount is calculated
* Discount is applied if:

  * Coupon belongs to the user
  * Coupon is unused
  * Coupon was generated in the **current nth-order cycle**

---

### Step 4: Nth Order Evaluation

After incrementing the global order counter:

* If `global_order_count % NTH_ORDER == 0`:

  * Old unused coupons are invalidated
  * A new coupon is generated for the current user

---

## Example Scenario

Assume:

```
NTH_ORDER = 5
```

### Orders Timeline

| Global Order # | User   | Coupon Action                                                     |
| -------------- | ------ | ----------------------------------------------------------------- |
| 1              | User A | ❌                                                                 |
| 2              | User B | ❌                                                                 |
| 3              | User A | ❌                                                                 |
| 4              | User B | ❌                                                                 |
| 5              | User B | 🎉 User B gets coupon                                             |
| 6              | User A | ❌                                                                 |
| 7              | User A | ❌                                                                 |
| 8              | User B | ❌                                                                 |
| 9              | User A | ❌                                                                 |
| 10             | User A | 🎉 User A gets new coupon (User B’s unused coupon is invalidated) |

---

## Coupon Validation Rules (At Checkout)

A coupon is accepted **only if all conditions pass**:

1. Coupon belongs to the user
2. Coupon is unused
3. Coupon was generated in the current nth-order cycle

Otherwise, checkout fails with an error.

---

## Admin APIs

### Get System Statistics

```
GET /admin/stats
```

Returns:

* Total orders
* Total revenue
* Total discount amount
* Total coupons generated
* Used vs unused coupons

---

## Available GET APIs (Frontend Friendly)

| Endpoint                          | Purpose         |
| --------------------------------- | --------------- |
| `GET /users`                      | List users      |
| `GET /products`                   | List products   |
| `GET /cart/{user_id}`             | View cart       |
| `GET /checkout/orders/{user_id}`  | Order history   |
| `GET /checkout/coupons/{user_id}` | User coupons    |
| `GET /admin/stats`                | Admin dashboard |

---

## In-Memory Database Behavior

* The application uses an **in-memory SQLite database**
* All data is reset when the app restarts
* Seed data is automatically loaded at startup
* Critical system state (like global order count) is **self-healing**

This choice keeps the system simple and aligned with assignment constraints.

---

## Running the Application

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Server

```bash
uvicorn app.main:app --reload
```

### 4. Open Swagger Docs

```
http://localhost:8000/docs
```

---

## Future Enhancements (Not Implemented Intentionally)

These ideas were consciously left out to avoid over-engineering:

* Authentication & RBAC (JWT)
* Persistent database (Postgres/MySQL)
* Pagination & filtering
* Background jobs for coupon expiry
* Activity-based or loyalty-based coupon eligibility
* Frontend UI (can be easily added)

All of the above can be layered on top without changing core logic.

---

## Final Notes

This implementation prioritizes:

* Correctness
* Clear assumptions
* Deterministic behavior
* Ease of explanation and testing

The design choices are **explicitly documented** to avoid ambiguity and demonstrate engineering judgment.

---
