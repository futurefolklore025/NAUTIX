from fastapi import APIRouter, Header, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import PaymentEvent, Booking


router = APIRouter()


@router.post("/payments/stripe/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None), db: Session = Depends(get_db)):
    # NOTE: For MVP, we skip signature verification. In production, verify with STRIPE_WEBHOOK_SECRET.
    payload = await request.body()
    try:
        event = request.json()  # FastAPI already parsed JSON in most cases
    except Exception:
        event = None

    if event is None or "id" not in event:
        raise HTTPException(status_code=400, detail="Invalid webhook payload")

    event_id = event["id"]
    if db.query(PaymentEvent).get(event_id):
        # Already processed
        return {"status": "ok"}

    # Persist event idempotently
    rec = PaymentEvent(id=event_id, type=event.get("type", "unknown"))
    db.add(rec)

    # Very basic state transition
    data = event.get("data", {}).get("object", {})
    booking_id = data.get("metadata", {}).get("booking_id")
    if booking_id:
        rec.booking_id = booking_id
        booking = db.query(Booking).get(booking_id)
        if booking and event.get("type") in {"payment_intent.succeeded", "checkout.session.completed"}:
            booking.status = "confirmed"
            db.add(booking)

    db.commit()
    return {"status": "ok"}


