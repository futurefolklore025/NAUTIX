#!/usr/bin/env python3
"""
Seed script to populate the database with sample data for development.
Run this after setting up the database and running migrations.
"""

import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.entities import Port, Schedule
from datetime import datetime, timedelta


def seed_ports(db: Session) -> None:
    """Seed ports with Croatian ferry ports."""
    ports_data = [
        {"name": "Split", "country": "Croatia"},
        {"name": "Hvar", "country": "Croatia"},
        {"name": "Vis", "country": "Croatia"},
        {"name": "Korčula", "country": "Croatia"},
        {"name": "Dubrovnik", "country": "Croatia"},
        {"name": "Zadar", "country": "Croatia"},
        {"name": "Ancona", "country": "Italy"},
    ]
    
    for port_data in ports_data:
        port = Port(**port_data)
        db.add(port)
    
    db.commit()
    print(f"✅ Seeded {len(ports_data)} ports")


def seed_schedules(db: Session) -> None:
    """Seed schedules with sample ferry routes."""
    # Get port IDs
    split_port = db.query(Port).filter(Port.name == "Split").first()
    hvar_port = db.query(Port).filter(Port.name == "Hvar").first()
    vis_port = db.query(Port).filter(Port.name == "Vis").first()
    korcula_port = db.query(Port).filter(Port.name == "Korčula").first()
    
    if not all([split_port, hvar_port, vis_port, korcula_port]):
        print("❌ Ports not found. Run seed_ports first.")
        return
    
    # Create schedules for next 7 days
    base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    schedules_data = []
    
    # Split -> Hvar (daily, multiple times)
    for day in range(7):
        date = base_date + timedelta(days=day)
        schedules_data.extend([
            {
                "origin_port_id": str(split_port.id),
                "dest_port_id": str(hvar_port.id),
                "departure_time": date.replace(hour=8, minute=0),
                "arrival_time": date.replace(hour=9, minute=30),
                "capacity": 200
            },
            {
                "origin_port_id": str(split_port.id),
                "dest_port_id": str(hvar_port.id),
                "departure_time": date.replace(hour=16, minute=0),
                "arrival_time": date.replace(hour=17, minute=30),
                "capacity": 200
            }
        ])
    
    # Split -> Vis (daily)
    for day in range(7):
        date = base_date + timedelta(days=day)
        schedules_data.append({
            "origin_port_id": str(split_port.id),
            "dest_port_id": str(vis_port.id),
            "departure_time": date.replace(hour=10, minute=0),
            "arrival_time": date.replace(hour=11, minute=30),
            "capacity": 150
        })
    
    # Hvar -> Korčula (daily)
    for day in range(7):
        date = base_date + timedelta(days=day)
        schedules_data.append({
            "origin_port_id": str(hvar_port.id),
            "dest_port_id": str(korcula_port.id),
            "departure_time": date.replace(hour=14, minute=0),
            "arrival_time": date.replace(hour=15, minute=0),
            "capacity": 100
        })
    
    for schedule_data in schedules_data:
        schedule = Schedule(**schedule_data)
        db.add(schedule)
    
    db.commit()
    print(f"✅ Seeded {len(schedules_data)} schedules")


def main() -> None:
    """Main seeding function."""
    print("🌊 Seeding Nautix database...")
    
    # Create tables if they don't exist
    from app.db.session import Base
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_ports(db)
        seed_schedules(db)
        print("🎉 Database seeding completed successfully!")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main() 