from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.entities import Hold, Schedule


DEFAULT_HOLD_MINUTES = 10


def create_hold(db: Session, schedule_id: str, pax_count: int, minutes: int = DEFAULT_HOLD_MINUTES) -> Hold:
    expires_at = datetime.utcnow() + timedelta(minutes=minutes)
    hold = Hold(schedule_id=schedule_id, pax_count=pax_count, expires_at=expires_at)
    db.add(hold)
    db.commit()
    db.refresh(hold)
    return hold


def consume_hold(db: Session, hold_id: str) -> bool:
    hold = db.query(Hold).filter(
        and_(Hold.id == hold_id, Hold.consumed == False, Hold.expires_at > datetime.utcnow())
    ).with_for_update().first()
    if not hold:
        return False
    hold.consumed = True
    db.add(hold)
    db.commit()
    return True


def release_expired_holds(db: Session) -> int:
    now = datetime.utcnow()
    expired = db.query(Hold).filter(and_(Hold.expires_at <= now, Hold.consumed == False)).all()
    count = len(expired)
    for h in expired:
        db.delete(h)
    db.commit()
    return count


