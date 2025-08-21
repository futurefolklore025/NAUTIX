from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import Booking, Schedule, Ticket, Hold
from app.schemas.api import (
    BookingCreate,
    BookingCreated,
    HealthResponse,
    ScanRequest,
    ScanResponse,
    ScheduleOut,
    TicketOut,
)
from app.services.qr import sign_qr_token, verify_qr_token
from app.services.holds import create_hold, consume_hold
from sqlalchemy import and_


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.utcnow())


@router.get("/search", response_model=List[ScheduleOut])
def search(
    origin_port_id: str = Query(...),
    dest_port_id: str = Query(...),
    date: datetime = Query(...),
    pax: int = Query(..., ge=1),
    db: Session = Depends(get_db),
) -> List[ScheduleOut]:
    # Very simple example: return schedules on same day between ports
    start = datetime(date.year, date.month, date.day)
    end = datetime(date.year, date.month, date.day, 23, 59, 59)
    schedules = (
        db.query(Schedule)
        .filter(
            Schedule.origin_port_id == origin_port_id,
            Schedule.dest_port_id == dest_port_id,
            Schedule.departure_time >= start,
            Schedule.departure_time <= end,
        )
        .all()
    )
    results: List[ScheduleOut] = []
    for s in schedules:
        out = ScheduleOut(
            id=str(s.id),
            departure_time=s.departure_time,
            arrival_time=s.arrival_time,
            capacity=s.capacity,
        )
        results.append(out)
    return results


@router.post("/bookings", response_model=BookingCreated, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)) -> BookingCreated:
    schedule: Schedule | None = db.query(Schedule).get(payload.schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    # Optional: require a hold id to be consumed for atomicity (MVP: auto-create/consume)
    hold = create_hold(db, schedule_id=str(schedule.id), pax_count=len(payload.passengers or []))
    if not consume_hold(db, hold.id):
        raise HTTPException(status_code=409, detail="Unable to secure seats (hold failed)")

    booking = Booking(
        schedule_id=str(schedule.id),
        status="confirmed",  # For MVP, confirm immediately; integrate Stripe later
        pax_count=len(payload.passengers or []),
        vehicle_type=(payload.vehicle or {}).get("type") if payload.vehicle else None,
    )
    db.add(booking)
    db.flush()

    tickets: List[Ticket] = []
    for passenger in payload.passengers:
        token = sign_qr_token({"booking_id": str(booking.id), "passenger": passenger.name})
        ticket = Ticket(
            booking_id=str(booking.id),
            passenger_name=passenger.name,
            qr_token=token,
        )
        db.add(ticket)
        tickets.append(ticket)

    db.commit()

    return BookingCreated(booking_id=str(booking.id), client_secret=None)


@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)) -> TicketOut:
    ticket: Ticket | None = db.query(Ticket).get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketOut(
        id=str(ticket.id),
        booking_id=str(ticket.booking_id),
        passenger_name=ticket.passenger_name,
        qr_token=ticket.qr_token or "",
    )


@router.post("/scan", response_model=ScanResponse)
def scan_ticket(payload: ScanRequest, db: Session = Depends(get_db)) -> ScanResponse:
    try:
        data = verify_qr_token(payload.qr_token)
    except Exception as exc:  # pragma: no cover - simplified error handling for MVP
        return ScanResponse(valid=False, reason=str(exc))

    booking_id = data.get("booking_id")
    passenger_name = data.get("passenger")

    ticket: Ticket | None = (
        db.query(Ticket)
        .filter(Ticket.booking_id == booking_id, Ticket.passenger_name == passenger_name)
        .first()
    )
    if not ticket:
        return ScanResponse(valid=False, reason="Ticket not found for booking")

    if ticket.used:
        return ScanResponse(valid=False, reason="Ticket already used", ticket_id=str(ticket.id), booking_id=str(ticket.booking_id))

    # Atomic mark-as-used via conditional update
    updated = (
        db.query(Ticket)
        .filter(Ticket.id == ticket.id, Ticket.used == False)
        .update({Ticket.used: True, Ticket.used_at: datetime.utcnow()})
    )
    db.commit()
    if updated == 0:
        return ScanResponse(valid=False, reason="Ticket already used", ticket_id=str(ticket.id), booking_id=str(ticket.booking_id))

    return ScanResponse(valid=True, ticket_id=str(ticket.id), booking_id=str(ticket.booking_id))

