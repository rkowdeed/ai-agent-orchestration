import React, {useEffect, useState} from 'react'

export default function App(){
  const [status, setStatus] = useState<string>('loading')

  useEffect(()=>{
    fetch('/api/v1/health')
      .then(r=>r.json())
      .then(d=>setStatus(d.status))
      .catch(()=>setStatus('offline'))
  },[])

  return (
    <div style={{fontFamily: 'system-ui, sans-serif', padding: 24}}>
      <h1>AI Agent Orchestration — MVP</h1>
      <p>Backend status: <strong>{status}</strong></p>
    </div>
  )
}
