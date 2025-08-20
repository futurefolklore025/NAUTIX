import React, { useState, useRef } from 'react'
import { QrReader } from 'react-qr-reader'
import axios from 'axios'
import { ScanData } from '../App'

interface QRScannerProps {
  onScanResult: (result: ScanData) => void
}

const QRScanner: React.FC<QRScannerProps> = ({ onScanResult }) => {
  const [isScanning, setIsScanning] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  const handleScan = async (result: any) => {
    if (result && !isProcessing) {
      setIsProcessing(true)
      setError(null)
      
      try {
        // Send the QR token to the backend for validation
        const response = await axios.post(`${import.meta.env.VITE_API_BASE || 'http://localhost:8000'}/scan`, {
          qr_token: result?.text
        })
        
        onScanResult(response.data)
      } catch (err: any) {
        console.error('Scan error:', err)
        setError(err.response?.data?.detail || 'Failed to validate ticket')
        
        // Still show result but mark as invalid
        onScanResult({
          valid: false,
          reason: err.response?.data?.detail || 'Failed to validate ticket'
        })
      } finally {
        setIsProcessing(false)
      }
    }
  }

  const handleError = (err: any) => {
    console.error('QR Scanner error:', err)
    setError('Camera access error. Please check permissions.')
  }

  const startScanning = () => {
    setIsScanning(true)
    setError(null)
  }

  const stopScanning = () => {
    setIsScanning(false)
  }

  return (
    <div className="qr-scanner">
      <div className="scanner-controls">
        {!isScanning ? (
          <button onClick={startScanning} className="start-btn">
            📱 Start Scanning
          </button>
        ) : (
          <button onClick={stopScanning} className="stop-btn">
            ⏹️ Stop Scanning
          </button>
        )}
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {isScanning && (
        <div className="camera-container">
          <QrReader
            onResult={handleScan}
            constraints={{ facingMode: 'environment' }}
            className="qr-reader"
          />
          <div className="scan-overlay">
            <div className="scan-frame"></div>
            <p>Position QR code within the frame</p>
          </div>
        </div>
      )}

      {isProcessing && (
        <div className="processing">
          🔄 Processing ticket...
        </div>
      )}

      <div className="instructions">
        <h3>How to use:</h3>
        <ol>
          <li>Click "Start Scanning" to activate camera</li>
          <li>Point camera at a Nautix QR ticket</li>
          <li>Hold steady until ticket is detected</li>
          <li>View validation result</li>
        </ol>
      </div>
    </div>
  )
}

export default QRScanner 