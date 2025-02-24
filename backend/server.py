from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import schema
import models
from database import get_db, Base, engine
from sqlalchemy.exc import SQLAlchemyError
import logging
from websocket import router as websocket_router, send_order_update


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(websocket_router)

@app.get("/orders")
async def get_orders(db: Session = Depends(get_db)):
    try:
        orders = db.query(models.Order).all()
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found")
        
        orders_dict = [
            {
                "id": order.id,
                "symbol": order.symbol,
                "price": order.price,
                "quantity": order.quantity,
                "status": order.status,
                "timestamp": order.timestamp,
                "order_type": order.order_type,
                "side": order.side,
                "exchange": order.exchange
            }
            for order in orders
        ]
        return orders_dict
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred") 

@app.post("/orders")
async def create_order(order: schema.CreateOrder, db:Session = Depends(get_db)):
    try:
        new_order = models.Order(**order.model_dump())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        await send_order_update(new_order.id, new_order.status, "create")

        return new_order
    except SQLAlchemyError as e:
        db.rollback()  
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred") 

@app.patch("/orders/{order_id}", response_model=schema.OrderBase)
async def update_order_status(order_id: int, order_data: schema.OrderStatusUpdate, db: Session = Depends(get_db)):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order.status = order_data.status
        
        db.commit()
        db.refresh(order) 
        
        await send_order_update(order.id, order.status, "update")
        return order
    except SQLAlchemyError as e:
        db.rollback()  
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred") 

@app.delete("/orders/{order_id}", response_model=schema.OrderBase)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        db.delete(order)
        db.commit()
        
        await send_order_update(order.id, "deleted", "delete")
        return order
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
