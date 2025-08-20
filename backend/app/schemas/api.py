from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator, EmailStr

from app.models.entities import BookingStatus


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


class PortOut(BaseModel):
    id: str
    name: str
    country: Optional[str] = None
    code: Optional[str] = None
    
    class Config:
        from_attributes = True


class OperatorOut(BaseModel):
    id: str
    name: str
    
    class Config:
        from_attributes = True


class ScheduleOut(BaseModel):
    id: str
    operator: Optional[OperatorOut] = None
    origin_port: Optional[PortOut] = None
    dest_port: Optional[PortOut] = None
    departure_time: datetime
    arrival_time: Optional[datetime] = None
    capacity: int
    available_capacity: Optional[int] = None
    base_price: Optional[Decimal] = None
    
    class Config:
        from_attributes = True


class PassengerInfo(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip().title()


class VehicleInfo(BaseModel):
    type: Optional[str] = None
    license_plate: Optional[str] = None


class BookingCreated(BaseModel):
    booking_id: str
    client_secret: Optional[str] = None


class TicketOut(BaseModel):
    id: str
    booking_id: str
    passenger_name: Optional[str] = None
    qr_token: str


class BookingCreate(BaseModel):
    schedule_id: str
    passengers: List[PassengerInfo] = Field(..., min_items=1, max_items=20)
    vehicle: Optional[VehicleInfo] = None
    addons: Optional[List[str]] = Field(default_factory=list)
    notes: Optional[str] = Field(None, max_length=500)


class ScanRequest(BaseModel):
    qr_token: str = Field(..., min_length=10)


class ScanResponse(BaseModel):
    valid: bool
    ticket_id: Optional[str] = None
    booking_id: Optional[str] = None
    passenger_name: Optional[str] = None
    reason: Optional[str] = None
    schedule: Optional[Dict[str, Any]] = None
