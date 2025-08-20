import React, { useState } from 'react'
import QRScanner from './components/QRScanner'
import ScanResult from './components/ScanResult'
import './App.css'

export interface ScanData {
  valid: boolean
  ticket_id?: string
  booking_id?: string
  reason?: string
}

function App() {
  const [scanResult, setScanResult] = useState<ScanData | null>(null)

  const handleScanResult = (result: ScanData) => {
    setScanResult(result)
  }

  const handleNewScan = () => {
    setScanResult(null)
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌊 Nautix Scanner</h1>
        <p>Scan ferry tickets and validate boarding passes</p>
      </header>
      
      <main>
        {!scanResult ? (
          <QRScanner onScanResult={handleScanResult} />
        ) : (
          <ScanResult result={scanResult} onNewScan={handleNewScan} />
        )}
      </main>
    </div>
  )
}

export default App 