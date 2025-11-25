import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function DetectionsTable(){
  const [rows, setRows] = useState([])

  async function load(){
    try{
      const res = await axios.get('/api/detections?limit=50')
      setRows(res.data.detections || [])
    }catch(err){
      console.error('Failed loading detections', err)
    }
  }

  useEffect(()=>{
    load()
    const id = setInterval(load, 4000)
    return ()=> clearInterval(id)
  },[])

  return (
    <div className="card">
      <h3>Recent Detections</h3>
      <table className="table" style={{marginTop:8}}>
        <thead>
          <tr><th>Time</th><th>Camera</th><th>Class</th><th>Violation</th><th>Image</th></tr>
        </thead>
        <tbody>
          {rows.length === 0 && <tr><td colSpan={5} style={{color:'#999'}}>No detections yet</td></tr>}
          {rows.map(r => (
            <tr key={r.id}>
              <td style={{whiteSpace:'nowrap'}}>{r.ts}</td>
              <td>{r.camera}</td>
              <td>{r.class}</td>
              <td>{r.violation_type || '-'}</td>
              <td>
                {r.image_path ? (
                  // image_path from backend might be an absolute path; if the backend serves media files,
                  // the dev environment should provide a URL. This anchor will try to open the given path.
                  <a href={r.image_path} target="_blank" rel="noreferrer">view</a>
                ) : '-'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
