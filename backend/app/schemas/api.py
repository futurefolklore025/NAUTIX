from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class SearchQuery(BaseModel):
    origin_port_id: str
    dest_port_id: str
    date: datetime
    pax: int


class ScheduleOut(BaseModel):
    id: str
    origin_port_id: str
    dest_port_id: str
    departure_time: datetime
    arrival_time: Optional[datetime] = None
    capacity: int


class BookingPassenger(BaseModel):
    name: Optional[str] = None


class BookingCreate(BaseModel):
    schedule_id: str
    passengers: List[BookingPassenger]
    vehicle: Optional[dict] = None
    addons: Optional[List[str]] = None


class BookingCreated(BaseModel):
    booking_id: str
    client_secret: Optional[str] = None


class TicketOut(BaseModel):
    id: str
    booking_id: str
    passenger_name: Optional[str] = None
    qr_token: str


class ScanRequest(BaseModel):
    qr_token: str


class ScanResponse(BaseModel):
    valid: bool
    ticket_id: Optional[str] = None
    booking_id: Optional[str] = None
    reason: Optional[str] = None

