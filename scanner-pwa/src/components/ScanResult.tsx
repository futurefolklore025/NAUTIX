import React from 'react'
import { ScanData } from '../App'

interface ScanResultProps {
  result: ScanData
  onNewScan: () => void
}

const ScanResult: React.FC<ScanResultProps> = ({ result, onNewScan }) => {
  const { valid, ticket_id, booking_id, reason } = result

  return (
    <div className="scan-result">
      <div className={`result-header ${valid ? 'valid' : 'invalid'}`}>
        {valid ? (
          <>
            <h2>✅ Ticket Valid</h2>
            <p>This ticket is valid for boarding</p>
          </>
        ) : (
          <>
            <h2>❌ Ticket Invalid</h2>
            <p>{reason || 'This ticket cannot be used'}</p>
          </>
        )}
      </div>

      {valid && (
        <div className="ticket-details">
          <h3>Ticket Information</h3>
          <div className="detail-row">
            <span className="label">Ticket ID:</span>
            <span className="value">{ticket_id}</span>
          </div>
          <div className="detail-row">
            <span className="label">Booking ID:</span>
            <span className="value">{booking_id}</span>
          </div>
          <div className="detail-row">
            <span className="label">Status:</span>
            <span className="value status-confirmed">Confirmed</span>
          </div>
        </div>
      )}

      {!valid && reason && (
        <div className="error-details">
          <h3>Error Details</h3>
          <div className="error-message">
            <strong>Reason:</strong> {reason}
          </div>
          {ticket_id && (
            <div className="detail-row">
              <span className="label">Ticket ID:</span>
              <span className="value">{ticket_id}</span>
            </div>
          )}
          {booking_id && (
            <div className="detail-row">
              <span className="label">Booking ID:</span>
              <span className="value">{booking_id}</span>
            </div>
          )}
        </div>
      )}

      <div className="actions">
        <button onClick={onNewScan} className="scan-again-btn">
          🔄 Scan Another Ticket
        </button>
      </div>

      <div className="help-text">
        <p>
          <strong>Note:</strong> Valid tickets are automatically marked as used in the system.
          {!valid && ' Please contact support if you believe this is an error.'}
        </p>
      </div>
    </div>
  )
}

export default ScanResult 