
# 🏥 FastAPI Demo

> A lightweight and production-ready RESTful API for managing hospital records using **FastAPI** and **SQLite**.

---

## 🚀 Live Demo

This API is live and hosted on Render:

🌐 **Base URL**: [`https://fastapi-demo-5p0z.onrender.com/`](https://fastapi-demo-5p0z.onrender.com/)
📄 **Swagger API Docs**: [`https://fastapi-demo-5p0z.onrender.com/docs/`](https://fastapi-demo-5p0z.onrender.com/docs/)
📄 **ReDoc**: [`https://fastapi-demo-5p0z.onrender.com/redoc/`](https://fastapi-demo-5p0z.onrender.com/redoc/)


> ⚠️ **Important Note about Render & SQLite**
>
> This application uses a SQLite database stored at `/tmp/hospitals.db`, which resides in a **temporary filesystem** provided by Render.
>
> Render **clears the `/tmp` directory after periods of inactivity** (typically around 10 minutes on the free tier), causing the database file to be **deleted automatically**.
>
> - As a result, any `GET` requests immediately after inactivity may return a **500 Internal Server Error** because the database no longer exists.
> - You must perform a `POST` request to insert data and recreate the SQLite file before any `GET`, `PUT`, or `DELETE` operations can work again.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Local Setup](#-local-setup-linux)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Logging](#-logging)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Project Overview

This FastAPI project is designed to:

- Manage hospital records (Add, View, Update, Delete).
- Use SQLite as the backend database.
- Follow RESTful principles.
- Be easily deployable and beginner-friendly.

It's a good starter project for understanding FastAPI, working with Pydantic models, and connecting to a lightweight DB without using an ORM.

---

## 🧰 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python 3.10+
- **Database**: SQLite
- **Data Validation**: Pydantic
- **Deployment**: [Render](https://render.com)
- **Logging**: Python's `logging` module

---

## 🧪 Features

- Add a hospital with basic details
- Retrieve all hospitals or a specific one by `id`
- Update hospital information
- Delete a hospital
- UUID-based unique hospital identification
- Auto timestamping
- Input validation and error logging
- Web service live on Render

---

## 🛠️ Local Setup (Linux)

### Prerequisites

- Python 3.10+
- `pip`

### 1. Clone the Repo

```bash
git clone https://github.com/enja-2001/FastAPI-Demo.git
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server Locally

```bash
python server.py
```

This will start the server at:  
📍 `http://localhost:8191`

---

## 🔌 API Endpoints

Base URL (Production): `https://fastapi-demo-5p0z.onrender.com/`

> ⚠️ **Important Note about Render & SQLite**
>
> This application uses a SQLite database stored at `/tmp/hospitals.db`, which resides in a **temporary filesystem** provided by Render.
>
> Render **clears the `/tmp` directory after periods of inactivity** (typically around 10 minutes on the free tier), causing the database file to be **deleted automatically**.
>
> - As a result, any `GET` requests immediately after inactivity may return a **500 Internal Server Error** because the database no longer exists.
> - You must perform a `POST` request to insert data and recreate the SQLite file before any `GET`, `PUT`, or `DELETE` operations can work again.

---

### 1. ➕ Add a Hospital

**POST** `/`

#### Request Body (JSON):

```json
{
  "name": "Apollo Hospital",
  "address": "123 Main Road, Bangalore",
  "phone": "9876543210"
}
```

#### Response:

```json
{
  "message": "Hospital added",
  "id": "3c1f9b1e-9a88-4a0c-b6f5-1f8f6d8a2ab5"
}
```

---

### 2. 📄 Get All Hospitals

**GET** `/`

#### Response:

```json
[
  {
    "id": "3c1f9b1e-9a88-4a0c-b6f5-1f8f6d8a2ab5",
    "name": "Apollo Hospital",
    "address": "123 Main Road, Bangalore",
    "phone": "9876543210",
    "created_at": "2025-07-10 22:00:00"
  }
]
```

---

### 3. 🔍 Get a Hospital by ID

**GET** `/{id}`

#### Example:
```
GET /3c1f9b1e-9a88-4a0c-b6f5-1f8f6d8a2ab5
```

#### Response:

```json
{
  "id": "3c1f9b1e-9a88-4a0c-b6f5-1f8f6d8a2ab5",
  "name": "Apollo Hospital",
  "address": "123 Main Road, Bangalore",
  "phone": "9876543210",
  "created_at": "2025-07-10 22:00:00"
}
```

---

### 4. ✏️ Update a Hospital

**PUT** `/{id}`

#### Request Body:

```json
{
  "name": "Apollo Super Speciality",
  "address": "123 Main Road, Bangalore",
  "phone": "8888888888"
}
```

#### Response:

```json
{
  "message": "Hospital updated successfully"
}
```

---

### 5. ❌ Delete a Hospital

**DELETE** `/{id}`

#### Response:

```json
{
  "message": "Hospital deleted successfully"
}
```

---

## 🗃️ Database Schema

Table: `hospitals`

| Column       | Type      | Description                          |
|--------------|-----------|--------------------------------------|
| `id`         | TEXT      | Unique UUID                          |
| `name`       | TEXT      | Name of the hospital (Required)      |
| `address`    | TEXT      | Address of the hospital (Required)   |
| `phone`      | TEXT      | Optional, only digits allowed        |
| `created_at` | TIMESTAMP | Auto-generated on insert             |

Primary key is a combination of `(name, address)` to prevent duplicates.

---

## 📜 Logging

All requests and failures are logged using the standard `logging` library with timestamps and log levels.

Example logs:
```
2025-07-10 22:34:12 - INFO - POST Request Received: name='Apollo' address='Bangalore' phone='98765'
2025-07-10 22:34:20 - ERROR - Failed to update hospital with id = abc123
```

---

## 🤝 Contributing

New contributors are welcome! Start by:

1. Forking the repo
2. Creating a new branch
3. Making changes
4. Submitting a Pull Request

---
