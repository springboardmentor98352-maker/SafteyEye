import React from 'react'
const PROJECT_BRIEF_URL = "/mnt/data/Saftey_Eye.pdf"

export default function Header(){
  return (
    <header>
      <div className="header-inner">
        <div style={{display:'flex', alignItems:'center', gap:12}}>
          <div style={{width:40, height:40, borderRadius:10, background:'#fff', display:'flex', alignItems:'center', justifyContent:'center', color:'#0b5cff', fontWeight:800}}>SE</div>
          <div>
            <h1 className="header-title">SafetyEye Dashboard</h1>
            <div style={{fontSize:12, color:'#dbeafe'}}>Realtime site safety monitoring</div>
          </div>
        </div>

        <div style={{display:'flex', gap:12, alignItems:'center'}}>
          <a className="small-btn" href={PROJECT_BRIEF_URL} target="_blank" rel="noreferrer">Project Brief</a>
        </div>
      </div>
    </header>
  )
}
