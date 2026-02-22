import { useState } from 'react'
import useProductos from '../hooks/useProductos'
import useVentas from '../hooks/useVentas'
import api from '../services/api'

export default function Ventas(){
  const {productos, refresh} = useProductos()
  const {ventas, refresh: refreshV} = useVentas()
  const [venta, setVenta] = useState({producto_id:'', cantidad:1})

  const submit = async (e)=>{
    e.preventDefault()
    await api.post('/ventas', {producto_id: parseInt(venta.producto_id), cantidad: parseInt(venta.cantidad)})
    setVenta({producto_id:'', cantidad:1})
    refresh(); refreshV()
  }

  return (
    <div className="max-w-4xl mx-auto px-4">
      <h2 className="text-2xl font-bold mb-4">Registrar Venta</h2>
      <form onSubmit={submit} className="mb-6 grid grid-cols-1 sm:grid-cols-3 gap-3">
        <select className="p-2 border rounded" value={venta.producto_id} onChange={e=>setVenta({...venta, producto_id:e.target.value})}>
          <option value="">Seleccionar</option>
          {productos.map(p=>(<option key={p.id} value={p.id}>{p.nombre}</option>))}
        </select>
        <input className="p-2 border rounded" type="number" value={venta.cantidad} onChange={e=>setVenta({...venta, cantidad:e.target.value})} />
        <button className="px-4 py-2 bg-emerald-500 text-white rounded" type="submit">Registrar</button>
      </form>
      <h3 className="text-lg mb-2">Últimas ventas</h3>
      <ul className="space-y-2">
        {ventas.map(v=>(<li key={v.id} className="p-2 border rounded">Producto #{v.producto_id} x {v.cantidad} - ${v.total}</li>))}
      </ul>
    </div>
  )
}
