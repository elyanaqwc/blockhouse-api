# Blockhouse API

## Introduction
Blockhouse API is a RESTful API built using **FastAPI** and **Pydantic** to implement CRUD operations on trade orders. Each CRUD operation also triggers a **WebSocket** function for real-time order updates. 

Order data is stored in a **PostgreSQL** database.The API is containerized using **Docker**, utilizing three containers: FastAPI, PostgreSQL, and pgAdmin 4.

---

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/elyanaqwc/blockhouse-api.git
```

### 2. Install Dependencies
Create a virtual environment and install dependencies:
```sh
python -m venv venv
source .venv/bin/activate  # On Windows Powershell use `.venv\Scripts\Activate.ps1`
```
Then, install the required dependencies:
```sh
cd backend
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root and configure the necessary environment variables:
```env
DATABASE_URL=postgresql://user:password@db:5432/orders_db
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=postgres_db
PGADMIN_DEFAULT_EMAIL=pgadmin_default_email
PGADMIN_DEFAULT_PASSWORD=pgadmin_default_password
```

## 4. Docker Setup
### Build and Run the Docker Compose Services
```sh
docker-compose up -d --build
```
The API is now accessible at http://localhost:8000.
---

## API Documentation

You can retrieve the API schema in JSON format via /api.json, or locally via the endpoints listed below. 

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

You can test each endpoint using Postman. 

### Orders CRUD Endpoints
- **Create Order:** `POST /orders`
- **Get All Orders:** `GET /orders`
- **Update Order:** `PATCH /orders/{order_id}`
- **Delete Order:** `DELETE /orders/{order_id}`

### WebSockets
- **Real-time Order Updates:** `ws://localhost:8000/ws`

---

## Deployment
### Deploy to AWS EC2
1. SSH into your EC2 instance:
   ```sh
   ssh -i your-key.pem ec2-user@your-ec2-ip
   ```
2. Pull your latest changes and restart the Docker container:
   ```sh
   git pull origin main
   docker-compose up -d --build
   ```

---

## Notes
1. The API works locally on Docker, but there are configuration issues when deploying on an AWS EC2 instance, specifically related to the database port.
2. There are also configuration issues with pytest in the CI/CD pipeline that need to be resolved.