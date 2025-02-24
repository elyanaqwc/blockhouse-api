import pytest
from fastapi.testclient import TestClient
from server import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Order
from database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    db = SessionLocal()
    db.query(Order).delete()
    db.commit()
    yield

    db.query(Order).delete()
    db.commit()

def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 404  

def test_create_order():
    order_data = {
        "symbol": "AAPL",
        "price": 150,
        "quantity": 10,
        "status": "open",
        "order_type": "limit",
        "side": "buy",
        "exchange": "NYSE"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    assert response.json()["symbol"] == "AAPL"
    assert response.json()["status"] == "open"

def test_update_order_status():
    order_data = {
        "symbol": "AAPL",
        "price": 150,
        "quantity": 10,
        "status": "open",
        "order_type": "limit",
        "side": "buy",
        "exchange": "NYSE"
    }

    create_response = client.post("/orders", json=order_data)
    order_id = create_response.json()["id"]
    
    update_data = {"status": "completed"}
    response = client.patch(f"/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

def test_delete_order():
    order_data = {
        "symbol": "AAPL",
        "price": 150,
        "quantity": 10,
        "status": "open",
        "order_type": "limit",
        "side": "buy",
        "exchange": "NYSE"
    }

    create_response = client.post("/orders", json=order_data)
    order_id = create_response.json()["id"]
    
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id
    assert response.json()["status"] == "open"  
