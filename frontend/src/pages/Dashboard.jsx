import { useEffect, useState } from 'react'
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import Card from '../components/Card'
import api from '../services/api'

export default function Dashboard(){
  const [data, setData] = useState(null)
  useEffect(()=>{
    api.get('/dashboard/resumen').then(r=>setData(r.data)).catch(()=>{})
  }, [])
  return (
    <div className="max-w-6xl mx-auto px-4">
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        <Card>
          <div className="text-sm text-gray-500">Total ventas día</div>
          <div className="text-2xl font-semibold">${data?.total_ventas_dia ?? 0}</div>
        </Card>
        <Card>
          <div className="text-sm text-gray-500">Producto más vendido</div>
          <div className="text-2xl font-semibold">{data?.producto_mas_vendido?.producto_id ?? '—'}</div>
        </Card>
        <Card>
          <div className="text-sm text-gray-500">Productos bajo stock</div>
          <div className="text-2xl font-semibold">{data?.productos_bajo_stock ?? 0}</div>
        </Card>
      </div>

      <div className="w-full" style={{height: 320}}>
        <ResponsiveContainer>
          <BarChart data={data?.ventas_por_producto || []}>
            <XAxis dataKey="producto_id" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="cantidad" fill="#0ea5a4" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
