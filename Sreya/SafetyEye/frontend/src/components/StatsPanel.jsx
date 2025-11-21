import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function StatsPanel(){
  const [hourly, setHourly] = useState([])
  const [violations, setViolations] = useState([])

  async function fetchStats(){
    try{
      const [hRes, vRes] = await Promise.all([
        axios.get('/api/stats/hourly'),
        axios.get('/api/stats/violations')
      ])
      setHourly(hRes.data.data || [])
      setViolations(vRes.data.data || [])
    }catch(err){
      // silent fail - show stale data
      console.error('Failed to load stats', err)
    }
  }

  useEffect(()=>{
    fetchStats()
    const id = setInterval(fetchStats, 5000)
    return ()=> clearInterval(id)
  },[])

  return (
    <div className="card">
      <h3>Metrics</h3>

      <div style={{marginBottom:12}}>
        <strong>Total violation types</strong>
        <ul className="metrics-list">
          {violations.length === 0 ? <li style={{color:'#999'}}>No data</li> : violations.map(v => (
            <li key={v.violation_type}>{v.violation_type || 'unknown'}: {v.cnt}</li>
          ))}
        </ul>
      </div>

      <div>
        <strong>Hourly detections</strong>
        <ul className="metrics-list">
          {hourly.length === 0 ? <li style={{color:'#999'}}>No data</li> :
            hourly.map(h => <li key={h.hour}>{h.hour}: {h.cnt}</li>)
          }
        </ul>
      </div>
    </div>
  )
}
