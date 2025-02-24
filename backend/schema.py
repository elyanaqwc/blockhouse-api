from pydantic import BaseModel, Field
from typing import Literal
from decimal import Decimal
from typing_extensions import Annotated

class OrderBase(BaseModel):
    symbol: str
    price: Annotated[Decimal, Field(gt=0)]
    quantity: Annotated[int, Field(strict=True,gt=0)]
    order_type: Literal["market", "limit", "stop"] = "market"
    side: Literal["buy","sell"]
    status: Literal["pending","filled","cancelled"] = "pending"
    exchange: str

    class Config:
        from_attributes = True

class CreateOrder(OrderBase):
    pass

class OrderStatusUpdate(BaseModel):
    order_id: int     
    status: str        
    
