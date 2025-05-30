## 🛍️ E-commerce Django REST API

This project is an e-commerce system built with Django REST Framework. Users can register either as *sellers* or *customers*. Sellers can add products, and customers can add products to their basket and view the total price. The project also includes a category system, search functionality, pagination, and slug-based URLs.

---

### 📌 Key Features

* ✅ User registration (with seller or customer role)
* ✅ Login functionality
* ✅ Product addition by sellers
* ✅ Category management by admin only
* ✅ Product basket system for customers
* ✅ Total basket price calculation
* ✅ Search by product name and category
* ✅ Pagination
* ✅ Slug-based product URLs
* ✅ Automatic assignment of the logged-in seller to the product

---

### 🛠️ Technologies Used

* Python 3.x
* Django
* Django REST Framework
* SQLite (default, but can be replaced with PostgreSQL or other databases)

---

### 🚀 Setup and Run Instructions

#### 1. Clone the repository:

```bash
git clone https://github.com/VafaKhanim/ecommerce-django-api.git
cd ecommerce-django-api
```

#### 2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

#### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

#### 4. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Create a superuser for admin panel access:

```bash
python manage.py createsuperuser
```

#### 6. Run the development server:

```bash
python manage.py runserver
```

---

### 📂 API Endpoints (Examples)

| Method | URL                | Description                          |
| ------ | ------------------ | ------------------------------------ |
| `POST` | `/api/register/`   | Register a new user with a role      |
| `POST` | `/api/login/`      | Token-based login                    |
| `GET`  | `/api/products/`   | List of products                     |
| `POST` | `/api/products/`   | Add a new product (only for sellers) |
| `GET`  | `/api/categories/` | List of categories                   |
| `POST` | `/api/basket/add/` | Add a product to the basket          |
| `GET`  | `/api/basket/`     | View basket items and total price    |

> Note: Some endpoints are restricted to authenticated users or specific roles such as seller or admin.

---

### 🧪 Testing the API

* You can test the endpoints using Postman or cURL.
* Token authentication is enabled — after logging in, include the token in the header as `Authorization: Token <token>`.

---

### ✨ Coming Soon

* ✅ Order management
* ✅ Payment integration
* ✅ Customer reviews
* ✅ Email verification
* ✅ Enhanced admin panel UI

---

### 👩‍💻 Author

Project developed by [VafaKhanim](https://github.com/VafaKhanim)
