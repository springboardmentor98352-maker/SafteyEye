import React, { useState, useEffect, useCallback } from 'react'
import { 
  AlertTriangle, Shield, HardHat, Eye, Bell, TrendingUp, 
  Clock, Camera, CheckCircle, XCircle, Activity, 
  RefreshCw, Wifi, WifiOff, ExternalLink 
} from 'lucide-react'

// Class names from classes.txt
const CLASS_NAMES = [
  'person', 'helmet', 'vest', 'no_helmet', 'face_mask',
  'boot', 'gloves', 'vehicle', 'sign', 'other_equipment'
]

// API Functions
const api = {
  async getDetections(limit = 50) {
    const res = await fetch(`/api/detections?limit=${limit}`)
    if (!res.ok) throw new Error('Failed to fetch detections')
    return res.json()
  },
  async getHourlyStats() {
    const res = await fetch('/api/stats/hourly')
    if (!res.ok) throw new Error('Failed to fetch hourly stats')
    return res.json()
  },
  async getViolationStats() {
    const res = await fetch('/api/stats/violations')
    if (!res.ok) throw new Error('Failed to fetch violation stats')
    return res.json()
  },
  getLastFrameUrl() {
    return `/media/last_frame?t=${Date.now()}`
  },
  getMediaUrl(path) {
    if (!path) return null
    if (path.startsWith('http')) return path
    if (path.startsWith('/media/')) return path
    return `/media/${path}`
  }
}

// Stat Card Component
function StatCard({ icon: Icon, title, value, subtitle, color, loading }) {
  return (
    <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className={`p-2.5 rounded-lg ${color}`}>
          <Icon size={20} className="text-white" />
        </div>
      </div>
      <div className="mt-3">
        {loading ? (
          <div className="h-8 w-20 bg-gray-200 rounded animate-pulse"></div>
        ) : (
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        )}
        <p className="text-sm text-gray-500 mt-1">{title}</p>
        {subtitle && <p className="text-xs text-gray-400 mt-0.5">{subtitle}</p>}
      </div>
    </div>
  )
}

// Live Feed Component
function LiveFeed({ isLive, connected }) {
  const [imgSrc, setImgSrc] = useState(api.getLastFrameUrl())
  const [hasError, setHasError] = useState(false)

  useEffect(() => {
    if (!isLive) return
    const interval = setInterval(() => {
      setImgSrc(api.getLastFrameUrl())
    }, 1000)
    return () => clearInterval(interval)
  }, [isLive])

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Camera size={18} className="text-gray-600" />
          <span className="font-semibold text-gray-800">Live Feed - Camera 01</span>
        </div>
        <div className="flex items-center gap-2">
          {connected ? <Wifi size={16} className="text-green-500" /> : <WifiOff size={16} className="text-red-500" />}
          {isLive && connected && (
            <span className="flex items-center gap-1.5 text-xs bg-red-500 text-white px-2.5 py-1 rounded-full">
              <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
              LIVE
            </span>
          )}
        </div>
      </div>
      <div className="relative bg-gray-900" style={{ minHeight: '340px' }}>
        {hasError ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-400">
            <Camera size={48} className="mb-3 opacity-50" />
            <p className="font-medium">No frame available</p>
            <p className="text-sm mt-1 text-gray-500">Make sure detect_realtime.py is running</p>
          </div>
        ) : (
          <img src={imgSrc} alt="Live camera feed" className="w-full h-auto"
            onError={() => setHasError(true)} onLoad={() => setHasError(false)} />
        )}
        <div className="absolute bottom-3 right-3 bg-black/70 backdrop-blur-sm rounded-lg px-3 py-2 text-white text-xs">
          {new Date().toLocaleString()}
        </div>
      </div>
    </div>
  )
}

// Detections Table Component
function DetectionsTable({ detections, loading }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Eye size={18} className="text-gray-600" />
          <span className="font-semibold text-gray-800">Recent Detections</span>
        </div>
        <span className="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded-full">{detections.length} records</span>
      </div>
      <div className="overflow-x-auto max-h-80">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 sticky top-0">
            <tr>
              <th className="text-left p-3 font-semibold text-gray-600">Time</th>
              <th className="text-left p-3 font-semibold text-gray-600">Camera</th>
              <th className="text-left p-3 font-semibold text-gray-600">Class</th>
              <th className="text-left p-3 font-semibold text-gray-600">Conf</th>
              <th className="text-left p-3 font-semibold text-gray-600">Status</th>
              <th className="text-left p-3 font-semibold text-gray-600">Image</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={6} className="p-8 text-center text-gray-400">
                <RefreshCw size={24} className="animate-spin mx-auto mb-2" />Loading...
              </td></tr>
            ) : detections.length === 0 ? (
              <tr><td colSpan={6} className="p-8 text-center text-gray-400">
                <Eye size={24} className="mx-auto mb-2 opacity-50" />No detections yet
              </td></tr>
            ) : (
              detections.map((d, i) => (
                <tr key={d.id || i} className={`border-t border-gray-50 hover:bg-gray-50 ${d.violation_type ? 'bg-red-50/30' : ''}`}>
                  <td className="p-3 text-gray-600 whitespace-nowrap text-xs font-mono">{d.ts}</td>
                  <td className="p-3 text-gray-800">{d.camera || 'cam1'}</td>
                  <td className="p-3">
                    <span className="flex items-center gap-1.5">
                      {d.violation_type ? <XCircle size={14} className="text-red-500" /> : <CheckCircle size={14} className="text-green-500" />}
                      {d.class_name || CLASS_NAMES[parseInt(d.class)] || d.class}
                    </span>
                  </td>
                  <td className="p-3 text-gray-600">{d.conf ? `${(d.conf * 100).toFixed(0)}%` : '-'}</td>
                  <td className="p-3">
                    {d.violation_type ? (
                      <span className="bg-red-100 text-red-700 px-2 py-1 rounded-full text-xs font-medium">{d.violation_type.replace('_', ' ')}</span>
                    ) : (
                      <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-medium">Compliant</span>
                    )}
                  </td>
                  <td className="p-3">
                    {d.image_url ? (
                      <a href={api.getMediaUrl(d.image_url)} target="_blank" rel="noreferrer"
                        className="text-blue-600 hover:underline inline-flex items-center gap-1 text-xs">
                        View <ExternalLink size={12} />
                      </a>
                    ) : '-'}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

// Violation Stats Component
function ViolationStats({ violations, loading }) {
  const colors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-pink-500']
  const maxCount = Math.max(...violations.map(v => v.cnt), 1)

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle size={18} className="text-red-500" />
        <span className="font-semibold text-gray-800">Violations by Type</span>
      </div>
      {loading ? (
        <div className="space-y-3">{[1,2,3].map(i => <div key={i} className="h-10 bg-gray-100 rounded animate-pulse"></div>)}</div>
      ) : violations.length === 0 ? (
        <div className="text-center py-6 text-gray-400">
          <CheckCircle size={32} className="mx-auto mb-2 text-green-400" />
          <p className="text-sm">No violations recorded</p>
        </div>
      ) : (
        <div className="space-y-4">
          {violations.map((v, i) => (
            <div key={i}>
              <div className="flex justify-between text-sm mb-1.5">
                <span className="text-gray-700 capitalize">{(v.violation_type || 'Unknown').replace('_', ' ')}</span>
                <span className="font-semibold text-gray-900">{v.cnt}</span>
              </div>
              <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
                <div className={`h-full ${colors[i % colors.length]} rounded-full transition-all duration-500`}
                  style={{ width: `${(v.cnt / maxCount) * 100}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// Hourly Chart Component
function HourlyChart({ data, loading }) {
  const maxCount = Math.max(...data.map(d => d.cnt), 1)

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Activity size={18} className="text-blue-500" />
          <span className="font-semibold text-gray-800">Hourly Activity</span>
        </div>
      </div>
      {loading ? (
        <div className="h-28 bg-gray-100 rounded animate-pulse"></div>
      ) : data.length === 0 ? (
        <div className="h-28 flex items-center justify-center text-gray-400 text-sm">No activity data yet</div>
      ) : (
        <>
          <div className="flex items-end gap-1 h-28">
            {data.slice(-12).map((d, i) => (
              <div key={i} className="flex-1 flex flex-col items-center">
                <div className="w-full flex flex-col justify-end" style={{ height: '80px' }}>
                  <div className="w-full bg-gradient-to-t from-blue-600 to-blue-400 rounded-t transition-all duration-300"
                    style={{ height: `${Math.max((d.cnt / maxCount) * 100, 4)}%` }} title={`${d.hour}: ${d.cnt}`}></div>
                </div>
                <span className="text-xs text-gray-400 mt-1.5">{d.hour?.slice(-5) || ''}</span>
              </div>
            ))}
          </div>
          <div className="flex justify-between mt-3 pt-3 border-t border-gray-100 text-xs text-gray-500">
            <span>Total: {data.reduce((a, b) => a + b.cnt, 0)}</span>
            <span>Avg: {Math.round(data.reduce((a, b) => a + b.cnt, 0) / Math.max(data.length, 1))}</span>
          </div>
        </>
      )}
    </div>
  )
}

// Main App Component
export default function App() {
  const [isLive, setIsLive] = useState(true)
  const [connected, setConnected] = useState(false)
  const [loading, setLoading] = useState(true)
  const [detections, setDetections] = useState([])
  const [hourlyStats, setHourlyStats] = useState([])
  const [violationStats, setViolationStats] = useState([])
  const [lastUpdated, setLastUpdated] = useState(null)

  const fetchData = useCallback(async () => {
    try {
      const [detectRes, hourlyRes, violationRes] = await Promise.all([
        api.getDetections(50), api.getHourlyStats(), api.getViolationStats()
      ])
      setDetections(detectRes.detections || [])
      setHourlyStats(hourlyRes.data || [])
      setViolationStats(violationRes.data || [])
      setConnected(true)
      setLoading(false)
      setLastUpdated(new Date())
    } catch (err) {
      console.error('API Error:', err)
      setConnected(false)
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 4000)
    return () => clearInterval(interval)
  }, [fetchData])

  const totalDetections = detections.length
  const totalViolations = detections.filter(d => d.violation_type).length
  const complianceRate = totalDetections > 0 ? ((totalDetections - totalViolations) / totalDetections * 100).toFixed(1) : '100'
  const hourlyAvg = hourlyStats.length > 0 ? Math.round(hourlyStats.reduce((a, b) => a + b.cnt, 0) / hourlyStats.length) : 0

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 via-blue-600 to-blue-700 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-11 h-11 bg-white rounded-xl flex items-center justify-center shadow-md">
                <Shield className="text-blue-600" size={26} />
              </div>
              <div>
                <h1 className="text-xl font-bold tracking-tight">SafetyEye</h1>
                <p className="text-blue-200 text-sm">AI-Powered Workplace Safety Monitor</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium ${connected ? 'bg-green-500/20 text-green-100' : 'bg-red-500/20 text-red-100'}`}>
                {connected ? <Wifi size={14} /> : <WifiOff size={14} />}
                {connected ? 'Connected' : 'Disconnected'}
              </div>
              <button onClick={fetchData} className="p-2 hover:bg-white/10 rounded-lg transition-colors" title="Refresh">
                <RefreshCw size={18} />
              </button>
              <button onClick={() => setIsLive(!isLive)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${isLive ? 'bg-white text-blue-600 shadow-md' : 'bg-blue-500/50 text-white'}`}>
                {isLive ? '⏸ Pause' : '▶ Resume'}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Connection Warning */}
      {!connected && !loading && (
        <div className="max-w-7xl mx-auto px-4 mt-4">
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex items-start gap-3">
            <AlertTriangle className="text-amber-600 flex-shrink-0 mt-0.5" size={20} />
            <div>
              <p className="font-medium text-amber-800">Backend not connected</p>
              <p className="text-sm text-amber-700 mt-1">
                Start your backend: <code className="bg-amber-100 px-2 py-0.5 rounded text-xs">uvicorn api:app --reload --port 8000</code>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {/* Stats Row */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatCard icon={Eye} title="Total Detections" value={totalDetections} subtitle="Recent records" color="bg-blue-500" loading={loading} />
          <StatCard icon={AlertTriangle} title="Violations" value={totalViolations} subtitle="Requires attention" color="bg-red-500" loading={loading} />
          <StatCard icon={HardHat} title="Compliance Rate" value={`${complianceRate}%`} subtitle="PPE compliance" color="bg-green-500" loading={loading} />
          <StatCard icon={TrendingUp} title="Hourly Average" value={hourlyAvg} subtitle="Detections/hour" color="bg-purple-500" loading={loading} />
        </div>

        {/* Main Grid */}
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <LiveFeed isLive={isLive} connected={connected} />
            <DetectionsTable detections={detections} loading={loading} />
          </div>
          <div className="space-y-6">
            <ViolationStats violations={violationStats} loading={loading} />
            <HourlyChart data={hourlyStats} loading={loading} />
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <div className="flex items-center gap-2 mb-3">
                <Clock size={18} className="text-gray-500" />
                <span className="font-semibold text-gray-800">System Info</span>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span className="text-gray-500">Last Updated</span><span className="text-gray-700">{lastUpdated ? lastUpdated.toLocaleTimeString() : '-'}</span></div>
                <div className="flex justify-between"><span className="text-gray-500">Refresh Rate</span><span className="text-gray-700">4 seconds</span></div>
                <div className="flex justify-between"><span className="text-gray-500">Classes</span><span className="text-gray-700">{CLASS_NAMES.length}</span></div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto px-4 py-6 mt-8 border-t border-gray-200">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-2 text-sm text-gray-400">
          <span>SafetyEye Dashboard v1.0</span>
          <span>AI-Powered Workplace Safety Monitoring</span>
        </div>
      </footer>
    </div>
  )
}