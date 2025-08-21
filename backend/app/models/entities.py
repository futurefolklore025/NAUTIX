from datetime import datetime
import uuid
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, String, Boolean,
    Numeric, Text, CheckConstraint, Index
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property

from app.db.session import Base


def _uuid_column() -> Column:
    return Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Port(Base):
    __tablename__ = "ports"

    id = _uuid_column()
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=True)
    code = Column(String(10), unique=True, nullable=True, index=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    origin_schedules = relationship("Schedule", foreign_keys="[Schedule.origin_port_id]", back_populates="origin_port")
    dest_schedules = relationship("Schedule", foreign_keys="[Schedule.dest_port_id]", back_populates="dest_port")

    __table_args__ = (
        Index('idx_port_country', 'country'),
        Index('idx_port_active', 'is_active'),
    )


class Operator(Base):
    __tablename__ = "operators"

    id = _uuid_column()
    name = Column(String(100), nullable=False)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    schedules = relationship("Schedule", back_populates="operator")


class Schedule(Base):
    __tablename__ = "schedules"

    id = _uuid_column()
    operator_id = Column(String, ForeignKey("operators.id", ondelete="CASCADE"), nullable=False)
    origin_port_id = Column(String, ForeignKey("ports.id", ondelete="CASCADE"), nullable=False)
    dest_port_id = Column(String, ForeignKey("ports.id", ondelete="CASCADE"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=True)
    capacity = Column(Integer, nullable=False, default=100)
    base_price = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    vehicle_capacity = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True, nullable=False)
    status = Column(String(20), default="on_time", nullable=False)  # on_time, delayed, cancelled
    status_reason = Column(Text, nullable=True)
    status_updated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    operator = relationship("Operator", back_populates="schedules")
    origin_port = relationship("Port", foreign_keys=[origin_port_id], back_populates="origin_schedules")
    dest_port = relationship("Port", foreign_keys=[dest_port_id], back_populates="dest_schedules")
    bookings = relationship("Booking", back_populates="schedule")

    @hybrid_property
    def available_capacity(self):
        """Calculate remaining capacity based on confirmed bookings"""
        confirmed_bookings = sum(
            booking.pax_count for booking in self.bookings 
            if booking.status == BookingStatus.CONFIRMED
        )
        return self.capacity - confirmed_bookings

    @validates('departure_time', 'arrival_time')
    def validate_times(self, key, value):
        if key == 'arrival_time' and value and self.departure_time:
            if value <= self.departure_time:
                raise ValueError("Arrival time must be after departure time")
        return value

    @validates('origin_port_id', 'dest_port_id')
    def validate_ports(self, key, value):
        if key == 'dest_port_id' and value and value == self.origin_port_id:
            raise ValueError("Origin and destination ports cannot be the same")
        return value

    __table_args__ = (
        CheckConstraint('capacity > 0', name='positive_capacity'),
        CheckConstraint('base_price >= 0', name='non_negative_price'),
        CheckConstraint('vehicle_capacity >= 0', name='non_negative_vehicle_capacity'),
        CheckConstraint('origin_port_id != dest_port_id', name='different_ports'),
        Index('idx_schedule_route_time', 'origin_port_id', 'dest_port_id', 'departure_time'),
        Index('idx_schedule_departure', 'departure_time'),
        Index('idx_schedule_active', 'is_active'),
        Index('idx_schedule_status', 'status'),
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = _uuid_column()
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    schedule_id = Column(String, ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False, default=BookingStatus.PENDING)
    pax_count = Column(Integer, nullable=False, default=1)
    vehicle_type = Column(String(50), nullable=True)
    total_price = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    payment_intent_id = Column(String, nullable=True)
    client_secret = Column(String, nullable=True)
    booking_reference = Column(String(20), unique=True, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    cancelled_at = Column(DateTime, nullable=True)
    confirmed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="bookings")
    schedule = relationship("Schedule", back_populates="bookings")
    tickets = relationship("Ticket", back_populates="booking", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.booking_reference:
            self.booking_reference = self._generate_booking_reference()

    @staticmethod
    def _generate_booking_reference() -> str:
        """Generate a unique booking reference like NTX-AB123CD"""
        import random
        import string
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=3))
        letters2 = ''.join(random.choices(string.ascii_uppercase, k=2))
        return f"NTX-{letters}{numbers}{letters2}"

    @validates('pax_count')
    def validate_pax_count(self, key, value):
        if value <= 0:
            raise ValueError("Passenger count must be positive")
        if value > 20:
            raise ValueError("Maximum 20 passengers per booking")
        return value

    __table_args__ = (
        CheckConstraint('pax_count > 0', name='positive_pax_count'),
        CheckConstraint('total_price >= 0', name='non_negative_price'),
        Index('idx_booking_user', 'user_id'),
        Index('idx_booking_schedule', 'schedule_id'),
        Index('idx_booking_status', 'status'),
        Index('idx_booking_reference', 'booking_reference'),
    )


class Ticket(Base):
    __tablename__ = "tickets"

    id = _uuid_column()
    booking_id = Column(String, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    passenger_name = Column(String(100), nullable=False)
    passenger_email = Column(String(255), nullable=True)
    seat_number = Column(String(10), nullable=True)
    used = Column(Boolean, default=False, nullable=False)
    used_at = Column(DateTime, nullable=True)
    scanned_by = Column(String, nullable=True)
    qr_token = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    booking = relationship("Booking", back_populates="tickets")

    @validates('passenger_name')
    def validate_passenger_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("Passenger name must be at least 2 characters")
        return value.strip().title()

    __table_args__ = (
        Index('idx_ticket_booking', 'booking_id'),
        Index('idx_ticket_used', 'used'),
        Index('idx_ticket_qr', 'qr_token'),
    )


class Hold(Base):
    __tablename__ = "holds"

    id = _uuid_column()
    schedule_id = Column(String, ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False)
    pax_count = Column(Integer, nullable=False, default=1)
    expires_at = Column(DateTime, nullable=False)
    consumed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    schedule = relationship("Schedule")

    __table_args__ = (
        CheckConstraint('pax_count > 0', name='positive_hold_pax'),
        Index('idx_hold_schedule', 'schedule_id'),
        Index('idx_hold_expires', 'expires_at'),
        Index('idx_hold_consumed', 'consumed'),
    )


class PaymentEvent(Base):
    __tablename__ = "payment_events"

    id = Column(String, primary_key=True)  # webhook event id
    type = Column(String, nullable=False)
    booking_id = Column(String, ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True)
    processed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

