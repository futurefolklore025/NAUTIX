#!/usr/bin/env python3
"""
Nautix Production Upgrade Script for Cursor
============================================

This script automatically upgrades your Nautix project to production-ready architecture.

Usage:
1. Save this file as 'upgrade_nautix.py' in your project root
2. Run in Cursor terminal: python upgrade_nautix.py
3. Follow the prompts
4. Commit and push your changes

The script will:
- Backup existing files
- Create new directory structure
- Install enhanced models, services, and middleware
- Update configuration and dependencies
- Generate environment templates
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


class NautixUpgrader:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backup_dir = self.project_root / "backup_original"
        
    def run(self):
        """Main upgrade process"""
        print("🌊 Nautix Production Upgrade")
        print("=" * 40)
        
        # Verify we're in the right place
        if not self._verify_project():
            print("❌ This doesn't appear to be a Nautix project. Exiting.")
            return
        
        # Create backup
        self._create_backup()
        
        # Create directory structure
        self._create_directories()
        
        # Install enhanced files
        self._install_enhanced_backend()
        self._install_middleware()
        self._install_schemas()
        self._install_production_configs()
        self._install_testing_framework()
        self._install_deployment_configs()
        
        # Update existing files
        self._update_requirements()
        self._update_docker_configs()
        
        # Generate templates
        self._generate_env_template()
        self._generate_setup_script()
        
        print("\n🎉 Upgrade completed successfully!")
        print("\nNext steps:")
        print("1. Copy .env.template to .env and configure your values")
        print("2. Run: chmod +x setup_production.sh && ./setup_production.sh")
        print("3. Test: cd backend && python -m pytest tests/")
        print("4. Commit: git add -A && git commit -m 'Upgrade to production architecture'")
    
    def _verify_project(self) -> bool:
        """Verify this is a Nautix project"""
        required_dirs = ["backend", "scanner-pwa", "mobile"]
        required_files = ["docker-compose.yml", "README.md"]
        
        for dir_name in required_dirs:
            if not (self.project_root / dir_name).exists():
                return False
        
        for file_name in required_files:
            if not (self.project_root / file_name).exists():
                return False
        
        return True
    
    def _create_backup(self):
        """Create backup of existing files"""
        print("📦 Creating backup...")
        
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        
        # Backup key files
        backup_files = [
            "backend/app/main.py",
            "backend/app/models/entities.py",
            "backend/requirements.txt",
            "docker-compose.yml"
        ]
        
        self.backup_dir.mkdir()
        for file_path in backup_files:
            source = self.project_root / file_path
            if source.exists():
                dest = self.backup_dir / file_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
        
        print("✅ Backup created in backup_original/")
    
    def _create_directories(self):
        """Create new directory structure"""
        print("📁 Creating directory structure...")
        
        directories = [
            "backend/app/models",
            "backend/app/services", 
            "backend/app/core",
            "backend/app/middleware",
            "backend/app/schemas",
            "backend/app/api/v1",
            "backend/tests",
            "backend/migrations/versions",
            "backend/keys",
            ".github/workflows",
            "kubernetes",
            "nginx",
            "monitoring/prometheus",
            "monitoring/grafana"
        ]
        
        for directory in directories:
            (self.project_root / directory).mkdir(parents=True, exist_ok=True)
        
        print("✅ Directory structure created")
    
    def _install_enhanced_backend(self):
        """Install enhanced backend models and services"""
        print("🔧 Installing enhanced backend...")
        
        # Enhanced entities model
        entities_content = '''from datetime import datetime
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
'''
        
        self._write_file("backend/app/models/entities.py", entities_content)
        
        # Authentication models
        auth_content = '''from datetime import datetime
import uuid
from enum import Enum

from sqlalchemy import Column, DateTime, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from app.db.session import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(str, Enum):
    PASSENGER = "passenger"
    OPERATOR = "operator"
    SCANNER = "scanner"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.PASSENGER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    bookings = relationship("Booking", back_populates="user")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
'''
        
        self._write_file("backend/app/models/auth.py", auth_content)
        
        print("✅ Enhanced backend models installed")
    
    def _install_middleware(self):
        """Install middleware files"""
        print("🛡️ Installing middleware...")
        
        # Error handling middleware
        error_middleware_content = '''import logging
import time
import traceback
from typing import Union

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.core.exceptions import NautixException


logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return await self.handle_exception(request, exc)
    
    async def handle_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """Handle different types of exceptions"""
        
        if isinstance(exc, NautixException):
            return self.create_error_response(
                status_code=exc.status_code,
                message=exc.message,
                details=exc.details,
                request_id=getattr(request.state, 'request_id', None)
            )
        
        elif isinstance(exc, HTTPException):
            return self.create_error_response(
                status_code=exc.status_code,
                message=exc.detail,
                request_id=getattr(request.state, 'request_id', None)
            )
        
        elif isinstance(exc, RequestValidationError):
            return self.create_error_response(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message="Validation error",
                details={"validation_errors": exc.errors()},
                request_id=getattr(request.state, 'request_id', None)
            )
        
        elif isinstance(exc, SQLAlchemyError):
            logger.error(f"Database error: {str(exc)}", exc_info=True)
            return self.create_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Database error occurred",
                request_id=getattr(request.state, 'request_id', None)
            )
        
        else:
            logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
            return self.create_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error",
                request_id=getattr(request.state, 'request_id', None)
            )
    
    def create_error_response(
        self,
        status_code: int,
        message: str,
        details: dict = None,
        request_id: str = None
    ) -> JSONResponse:
        """Create standardized error response"""
        
        error_response = {
            "error": {
                "message": message,
                "status_code": status_code,
                "timestamp": str(int(time.time())),
                "type": self.get_error_type(status_code)
            }
        }
        
        if details:
            error_response["error"]["details"] = details
        
        if request_id:
            error_response["error"]["request_id"] = request_id
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )
    
    @staticmethod
    def get_error_type(status_code: int) -> str:
        """Get error type based on status code"""
        if 400 <= status_code < 500:
            return "client_error"
        elif 500 <= status_code < 600:
            return "server_error"
        else:
            return "unknown_error"
'''
        
        self._write_file("backend/app/middleware/error_handler.py", error_middleware_content)
        
        print("✅ Middleware installed")
    
    def _install_schemas(self):
        """Install Pydantic schemas"""
        print("📝 Installing schemas...")
        
        api_schemas_content = '''from datetime import datetime
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
    operator: OperatorOut
    origin_port: PortOut
    dest_port: PortOut
    departure_time: datetime
    arrival_time: Optional[datetime] = None
    capacity: int
    available_capacity: int
    base_price: Decimal
    
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
    type: str = Field(..., regex="^(car|motorcycle|bicycle)$")
    license_plate: Optional[str] = None


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
'''
        
        self._write_file("backend/app/schemas/api.py", api_schemas_content)
        
        print("✅ Schemas installed")
    
    def _install_production_configs(self):
        """Install production configuration files"""
        print("⚙️ Installing production configs...")
        
        # Enhanced main.py
        main_content = '''import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.api.v1 import endpoints
from app.db.session import create_database_tables


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    
    # Create database tables
    if settings.is_development:
        create_database_tables()
        logger.info("Database tables created")
    
    yield
    
    # Shutdown
    logger.info("Application shutdown")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Maritime travel platform API",
        lifespan=lifespan,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None
    )
    
    # Security middleware
    if settings.is_production:
        app.add_middleware(
            TrustedHostMiddleware, 
            allowed_hosts=["*.nautix.com", "nautix.com"]
        )
    
    # Compression middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"]
    )
    
    # Custom middleware
    app.add_middleware(ErrorHandlerMiddleware)
    
    # Include API routes
    app.include_router(endpoints.router, prefix="/api/v1", tags=["api"])
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "environment": settings.environment,
            "docs_url": "/docs" if not settings.is_production else None
        }
    
    return app


app = create_app()
'''
        
        self._write_file("backend/app/main.py", main_content)
        
        # Enhanced config
        config_content = '''import secrets
from functools import lru_cache
from typing import List, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore",
        case_sensitive=False
    )

    # App settings
    app_name: str = "Nautix API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = Field(default="development", regex="^(development|staging|production)$")

    # Database
    database_url: str = "sqlite:///./nautix.db"

    # Security
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins_raw: str = "*"
    cors_allow_credentials: bool = True

    # JWT keys for QR tokens
    jwt_private_key_path: str = "keys/qr_es256_private.pem"
    jwt_public_key_path: str = "keys/qr_es256_public.pem"

    # External services
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None

    @property
    def cors_origins(self) -> List[str]:
        raw = self.cors_origins_raw
        if not raw or raw.strip() == "*":
            return ["*"]
        return [o.strip() for o in raw.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
'''
        
        self._write_file("backend/app/core/config.py", config_content)
        
        print("✅ Production configs installed")
    
    def _install_testing_framework(self):
        """Install testing framework"""
        print("🧪 Installing testing framework...")
        
        conftest_content = '''import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db
from app.models.auth import User, UserRole
from app.models.entities import Port, Operator, Schedule


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""
    
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db: Session) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=User.hash_password("testpassword123"),
        full_name="Test User",
        role=UserRole.PASSENGER,
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
'''
        
        self._write_file("backend/tests/conftest.py", conftest_content)
        
        test_health_content = '''import pytest
from fastapi.testclient import TestClient


class TestHealth:
    
    def test_health_endpoint(self, client: TestClient):
        """Test basic health endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
'''
        
        self._write_file("backend/tests/test_health.py", test_health_content)
        
        print("✅ Testing framework installed")
    
    def _install_deployment_configs(self):
        """Install deployment configurations"""
        print("🚀 Installing deployment configs...")
        
        # GitHub Actions CI/CD
        github_workflow_content = '''name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: nautix_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Generate test keys
      run: |
        cd backend
        mkdir -p keys
        openssl ecparam -genkey -name prime256v1 -noout -out keys/qr_es256_private.pem
        openssl ec -in keys/qr_es256_private.pem -pubout -out keys/qr_es256_public.pem

    - name: Run tests
      env:
        DATABASE_URL: postgresql+psycopg2://postgres:postgres@localhost:5432/nautix_test
        SECRET_KEY: test-secret-key-for-ci-only
      run: |
        cd backend
        pytest tests/ -v --cov=app
'''
        
        self._write_file(".github/workflows/ci.yml", github_workflow_content)
        
        # Production Docker Compose
        docker_prod_content = '''version: '3.9'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-nautix}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-nautix}
      POSTGRES_DB: ${POSTGRES_DB:-nautix}
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nautix"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      target: production
    environment:
      - DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER:-nautix}:${POSTGRES_PASSWORD:-nautix}@db:5432/${POSTGRES_DB:-nautix}
      - ENVIRONMENT=production
      - SECRET_KEY=${SECRET_KEY}
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
      - STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET}
      - CORS_ORIGINS=${CORS_ORIGINS:-*}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8000:8000"
    restart: unless-stopped

volumes:
  pg_data:
  redis_data:
'''
        
        self._write_file("docker-compose.prod.yml", docker_prod_content)
        
        # Nginx configuration
        nginx_content = '''events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        listen 80;
        
        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /api/v1/health {
            proxy_pass http://backend;
            access_log off;
        }
    }
}
'''
        
        self._write_file("nginx/nginx.conf", nginx_content)
        
        print("✅ Deployment configs installed")
    
    def _update_requirements(self):
        """Update requirements.txt with production dependencies"""
        print("📦 Updating requirements...")
        
        requirements_content = '''# Core FastAPI
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Data validation
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# HTTP & Utilities
httpx==0.25.2
python-dotenv==1.0.0

# Payment processing
stripe==7.8.0

# QR code generation
qrcode[pil]==7.4.2

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Development tools
ruff==0.1.6
black==23.11.0
mypy==1.7.1

# Production monitoring
structlog==23.2.0
prometheus-client==0.19.0
'''
        
        self._write_file("backend/requirements.txt", requirements_content)
        
        print("✅ Requirements updated")
    
    def _update_docker_configs(self):
        """Update Docker configurations"""
        print("🐳 Updating Docker configs...")
        
        dockerfile_content = '''FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Development stage
FROM base as development

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create keys directory
RUN mkdir -p /app/keys && \
    if [ ! -f /app/keys/qr_es256_private.pem ]; then \
        openssl ecparam -genkey -name prime256v1 -noout -out /app/keys/qr_es256_private.pem && \
        openssl ec -in /app/keys/qr_es256_private.pem -pubout -out /app/keys/qr_es256_public.pem; \
    fi

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production

# Create non-root user
RUN groupadd -r nautix and useradd -r -g nautix nautix

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p /app/keys /app/logs && \
    chown -R nautix:nautix /app

# Switch to non-root user
USER nautix

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        
        self._write_file("backend/Dockerfile", dockerfile_content)
        
        print("✅ Docker configs updated")
    
    def _generate_env_template(self):
        """Generate environment template"""
        print("📝 Generating environment template...")
        
        env_template = '''# Nautix Production Environment Template
# Copy to .env and configure your values

# Database
DATABASE_URL=postgresql+psycopg2://nautix:password@localhost:5432/nautix
REDIS_URL=redis://localhost:6379/0

# Security (CHANGE THESE!)
SECRET_KEY=your-super-secret-key-at-least-32-characters-long
ENVIRONMENT=development

# JWT Keys
JWT_PRIVATE_KEY_PATH=keys/qr_es256_private.pem
JWT_PUBLIC_KEY_PATH=keys/qr_es256_public.pem

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Stripe (get from https://dashboard.stripe.com)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@nautix.com

# Monitoring
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Business Rules
BOOKING_CANCELLATION_HOURS=24
MAX_PASSENGERS_PER_BOOKING=20
'''
        
        self._write_file(".env.template", env_template)
        
        print("✅ Environment template generated")
    
    def _generate_setup_script(self):
        """Generate production setup script"""
        print("🔧 Generating setup script...")
        
        setup_script = '''#!/bin/bash

echo "🌊 Setting up Nautix production environment..."

# Generate JWT keys
echo "🔑 Generating JWT keys..."
mkdir -p backend/keys
if [ ! -f "backend/keys/qr_es256_private.pem" ]; then
    openssl ecparam -genkey -name prime256v1 -noout -out backend/keys/qr_es256_private.pem
    openssl ec -in backend/keys/qr_es256_private.pem -pubout -out backend/keys/qr_es256_public.pem
    echo "✅ JWT keys generated"
else
    echo "⚠️  JWT keys already exist"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copy .env.template to .env and configure your values."
    exit 1
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
alembic upgrade head

# Seed data (optional)
read -p "Do you want to seed sample data? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python scripts/seed.py
    echo "✅ Sample data seeded"
fi

echo "🎉 Production setup complete!"
echo ""
echo "Next steps:"
echo "1. Start the application: uvicorn app.main:app --reload"
echo "2. Visit http://localhost:8000/docs for API documentation"
echo "3. Run tests: pytest tests/ -v"
'''
        
        self._write_file("setup_production.sh", setup_script)
        
        # Make script executable
        os.chmod(self.project_root / "setup_production.sh", 0o755)
        
        print("✅ Setup script generated")
    
    def _write_file(self, path: str, content: str):
        """Write content to file"""
        file_path = self.project_root / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)


if __name__ == "__main__":
    upgrader = NautixUpgrader()
    upgrader.run()
