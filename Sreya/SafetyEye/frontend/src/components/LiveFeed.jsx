import React, { useEffect, useState } from 'react'

export default function LiveFeed(){
  const [tick, setTick] = useState(0)
  useEffect(()=>{
    const id = setInterval(()=> setTick(t => t+1), 1500)
    return ()=> clearInterval(id)
  },[])
  // Cache-busting query param to force reload
  const imgSrc = `/media/last_frame?cache=${tick}`

  return (
    <div className="card">
      <h3>Live feed</h3>
      <img className="live-img" src={imgSrc} alt="Last frame" onError={(e)=>{ e.target.src = 'https://via.placeholder.com/800x450?text=No+Frame+Available' }} />
    </div>
  )
}
