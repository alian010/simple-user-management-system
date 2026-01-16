Here is a **clean, professional `README.md`** you can directly copy–paste into your GitHub repository.
It’s written in **team-lead / reviewer-friendly** style and matches your API Test Documentation exactly.

````md
# User Management System API  
**Django REST Framework + JWT Authentication**

---

## 📌 Project Overview

This project is a **User Management REST API** built using:

- **Django**
- **Django REST Framework (DRF)**
- **JWT (JSON Web Token) Authentication**

The API provides secure user authentication and profile management following **backend best practices** and **REST standards**.

### ✨ Features

- User Registration
- User Login
- JWT Token Refresh
- Secure Logout
- View User Profile
- Update User Profile
- Change Password
- Clean error handling
- Production-ready API structure

---

## 🚀 Technology Stack

- **Backend:** Django, Django REST Framework  
- **Authentication:** JWT (SimpleJWT)  
- **Database:** SQLite  (configurable)  
- **Testing:** Postman 

---

## 🌐 Base URL

```text
http://127.0.0.1:8000/users/
````

---

## 🔐 Authentication

Authentication is handled using **JWT**.

### Authorization Header Format

```http
Authorization: Bearer <ACCESS_TOKEN>
```

Protected endpoints **require** a valid access token.

---

## 📦 Common Request Headers

| Header        | Value                                    |
| ------------- | ---------------------------------------- |
| Content-Type  | application/json                         |
| Authorization | Bearer `<ACCESS_TOKEN>` (protected APIs) |

---

## 📘 API Endpoints Documentation

---

### 1️⃣ User Registration

**Endpoint**

```http
POST /users/register/
```

**Description**
Creates a new user and returns JWT tokens.

**Request Body**

```json
{
  "email": "test@example.com",
  "full_name": "Test User",
  "password": "StrongPass123",
  "password2": "StrongPass123"
}
```

**Success Response (201)**

```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "test@example.com",
      "full_name": "Test User"
    },
    "tokens": {
      "access": "<access_token>",
      "refresh": "<refresh_token>"
    }
  }
}
```

---

### 2️⃣ User Login

**Endpoint**

```http
POST /users/login/
```

**Request Body**

```json
{
  "email": "test@example.com",
  "password": "StrongPass123"
}
```

**Success Response (200)**

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "test@example.com",
      "full_name": "Test User"
    },
    "tokens": {
      "access": "<access_token>",
      "refresh": "<refresh_token>"
    }
  }
}
```

---

### 3️⃣ Get User Profile

**Endpoint**

```http
GET /users/profile/
```

**Headers**

```http
Authorization: Bearer <ACCESS_TOKEN>
```

**Success Response (200)**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "test@example.com",
    "full_name": "Test User",
    "is_active": true,
    "created_at": "2026-01-16T08:30:10Z",
    "updated_at": "2026-01-16T08:30:10Z"
  }
}
```

---

### 4️⃣ Update User Profile

**Endpoint**

```http
PATCH /users/profile/
```

**Request Body**

```json
{
  "full_name": "Updated Name"
}
```

**Success Response (200)**

```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": 1,
    "email": "test@example.com",
    "full_name": "Updated Name",
    "is_active": true,
    "created_at": "2026-01-16T08:30:10Z",
    "updated_at": "2026-01-16T08:40:00Z"
  }
}
```

---

### 5️⃣ Change Password

**Endpoint**

```http
POST /users/profile/change-password/
```

**Request Body**

```json
{
  "old_password": "StrongPass123",
  "new_password": "NewStrongPass456",
  "new_password2": "NewStrongPass456"
}
```

**Success Response (200)**

```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

---

### 6️⃣ Token Refresh

**Endpoint**

```http
POST /users/token/refresh/
```

**Request Body**

```json
{
  "refresh": "<refresh_token>"
}
```

**Success Response**

```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "access": "<new_access_token>",
    "refresh": "<new_refresh_token>"
  }
}
```

---

### 7️⃣ Logout

**Endpoint**

```http
POST /users/logout/
```

**Request Body**

```json
{
  "refresh": "<refresh_token>"
}
```

**Success Response**

```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

## 📊 HTTP Status Codes

| Code | Meaning                |
| ---- | ---------------------- |
| 200  | Success                |
| 201  | Created                |
| 400  | Bad Request            |
| 401  | Unauthorized           |
| 403  | Forbidden              |
| 404  | Not Found              |
| 415  | Unsupported Media Type |

---

## 🧪 Testing Tools

* Postman ✅ (Recommended)

---

---
```
