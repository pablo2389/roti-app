import { useState } from 'react'
import useProductos from '../hooks/useProductos'
import api from '../services/api'

export default function Generador(){
  const {productos} = useProductos()
  const [selected, setSelected] = useState('')
  const [prompt, setPrompt] = useState('')

  const generar = async ()=>{
    const res = await api.post('/dashboard/generar-contenido-ia', null, {params:{producto_id: selected}})
    setPrompt(res.data.prompt)
  }

  const descargarPdf = async ()=>{
    const res = await api.post('/dashboard/generar-pdf-menu', {}, {responseType: 'blob'})
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a')
    a.href = url; a.download = 'menu.pdf'; a.click()
  }

  return (
    <div className="max-w-4xl mx-auto px-4">
      <h2 className="text-2xl font-bold mb-4">Generadores</h2>
      <div className="mb-6">
        <button className="px-4 py-2 bg-sky-500 text-white rounded" onClick={descargarPdf}>Generar PDF</button>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <select className="p-2 border rounded" value={selected} onChange={e=>setSelected(e.target.value)}>
          <option value="">Seleccionar producto</option>
          {productos.map(p=>(<option key={p.id} value={p.id}>{p.nombre}</option>))}
        </select>
        <button className="px-4 py-2 bg-purple-500 text-white rounded" onClick={generar}>Generar cartilla IA</button>
        <div className="sm:col-span-3 p-2 border rounded bg-gray-50"><pre className="whitespace-pre-wrap">{prompt}</pre></div>
      </div>
    </div>
  )
}
