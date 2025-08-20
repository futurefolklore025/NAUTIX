from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


def _uuid_column() -> Column:
    return Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))


class Port(Base):
    __tablename__ = "ports"

    id = _uuid_column()
    name = Column(String, nullable=False)
    country = Column(String, nullable=True)


class Schedule(Base):
    __tablename__ = "schedules"

    id = _uuid_column()
    origin_port_id = Column(String, ForeignKey("ports.id"), nullable=False)
    dest_port_id = Column(String, ForeignKey("ports.id"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=True)
    capacity = Column(Integer, nullable=False, default=100)

    origin_port = relationship("Port", foreign_keys=[origin_port_id])
    dest_port = relationship("Port", foreign_keys=[dest_port_id])


class Booking(Base):
    __tablename__ = "bookings"

    id = _uuid_column()
    schedule_id = Column(String, ForeignKey("schedules.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, confirmed, cancelled
    pax_count = Column(Integer, nullable=False, default=1)
    vehicle_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    client_secret = Column(String, nullable=True)  # Stripe client secret when applicable

    schedule = relationship("Schedule")
    tickets = relationship("Ticket", back_populates="booking")


class Ticket(Base):
    __tablename__ = "tickets"

    id = _uuid_column()
    booking_id = Column(String, ForeignKey("bookings.id"), nullable=False)
    passenger_name = Column(String, nullable=True)
    used = Column(Boolean, default=False, nullable=False)
    qr_token = Column(String, nullable=True)

    booking = relationship("Booking", back_populates="tickets")

