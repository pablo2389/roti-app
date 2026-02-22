import { useState } from 'react'
import Modal from '../components/Modal'
import useProductos from '../hooks/useProductos'
import api from '../services/api'

export default function Productos(){
  const {productos, refresh} = useProductos()
  const [form, setForm] = useState({nombre:'', descripcion:'', precio:0, stock:0, stock_minimo:0, imagen: null})
  const [editing, setEditing] = useState(false)
  const [editProduct, setEditProduct] = useState(null)
  const [preview, setPreview] = useState(null)

  const submit = async (e)=>{
    e.preventDefault()
    const data = new FormData()
    data.append('nombre', form.nombre)
    data.append('descripcion', form.descripcion || '')
    data.append('precio', String(form.precio))
    data.append('stock', String(form.stock))
    data.append('stock_minimo', String(form.stock_minimo))
    if (form.imagen) data.append('imagen', form.imagen)
    await api.post('/productos', data)
    setForm({nombre:'', descripcion:'', precio:0, stock:0, stock_minimo:0, imagen: null})
    refresh()
  }

  const openEdit = (p)=>{
    setEditProduct(p)
    setPreview(p.imagen_path ? (p.imagen_path.startsWith('http') ? p.imagen_path : api.defaults.baseURL + p.imagen_path) : null)
    setEditing(true)
  }

  const closeEdit = ()=>{
    setEditProduct(null)
    setPreview(null)
    setEditing(false)
  }

  const onEditFile = (file)=>{
    if(!file) { setPreview(null); return }
    setEditProduct({...editProduct, imagen: file})
    const url = URL.createObjectURL(file)
    setPreview(url)
  }

  const submitEdit = async (e)=>{
    e.preventDefault()
    if(!editProduct) return
    const data = new FormData()
    data.append('nombre', editProduct.nombre)
    data.append('descripcion', editProduct.descripcion || '')
    data.append('precio', String(editProduct.precio))
    data.append('stock', String(editProduct.stock))
    data.append('stock_minimo', String(editProduct.stock_minimo))
    if(editProduct.imagen) data.append('imagen', editProduct.imagen)
    await api.put(`/productos/${editProduct.id}`, data)
    refresh()
    closeEdit()
  }

  return (
    <>
    <div className="max-w-4xl mx-auto px-4">
      <h2 className="text-2xl font-bold mb-4">Productos</h2>
      <form onSubmit={submit} className="mb-6 grid grid-cols-1 sm:grid-cols-2 gap-3">
        <input className="p-2 border rounded" placeholder="Nombre" value={form.nombre} onChange={e=>setForm({...form, nombre:e.target.value})} />
        <input className="p-2 border rounded" placeholder="Precio" type="number" value={form.precio} onChange={e=>setForm({...form, precio:parseFloat(e.target.value)})} />
        <input className="p-2 border rounded" placeholder="Stock" type="number" value={form.stock} onChange={e=>setForm({...form, stock:parseInt(e.target.value)})} />
        <input className="p-2 border rounded" placeholder="Stock mínimo" type="number" value={form.stock_minimo} onChange={e=>setForm({...form, stock_minimo:parseInt(e.target.value)})} />
        <textarea className="p-2 border rounded col-span-1 sm:col-span-2" placeholder="Descripción" value={form.descripcion} onChange={e=>setForm({...form, descripcion:e.target.value})} />
        <input className="p-2" type="file" name="imagen" onChange={e=>setForm({...form, imagen:e.target.files[0]})} />
        <button className="col-span-1 sm:col-span-2 px-4 py-2 bg-emerald-500 text-white rounded" type="submit">Crear</button>
      </form>

      <div className="overflow-x-auto">
        <table className="w-full table-auto">
          <thead className="bg-gray-100"><tr><th className="p-2">Nombre</th><th className="p-2">Precio</th><th className="p-2">Stock</th><th className="p-2">Acciones</th></tr></thead>
          <tbody>
            {productos.map(p=> (
              <tr key={p.id} className={p.stock<=p.stock_minimo? 'text-red-600': ''}>
                <td className="p-2 flex items-center">
                  {p.imagen_path && (
                    <img src={(p.imagen_path.startsWith('http')? p.imagen_path : api.defaults.baseURL + p.imagen_path)} alt={p.nombre} className="w-12 h-12 object-cover mr-3 rounded" />
                  )}
                  <span>{p.nombre}</span>
                </td>
                <td className="p-2">${p.precio}</td>
                <td className="p-2">{p.stock}</td>
                <td className="p-2">
                  <button className="mr-2 px-3 py-1 bg-yellow-400 text-white rounded" onClick={()=>openEdit(p)}>Editar</button>
                  <button className="px-3 py-1 bg-red-500 text-white rounded" onClick={async ()=>{await api.delete(`/productos/${p.id}`); refresh()}}>Borrar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
    <Modal open={editing} onClose={closeEdit}>
      {editProduct && (
        <form onSubmit={submitEdit} className="grid gap-2">
          <input className="p-2 border rounded" value={editProduct.nombre} onChange={e=>setEditProduct({...editProduct, nombre: e.target.value})} />
          <input className="p-2 border rounded" type="number" value={editProduct.precio} onChange={e=>setEditProduct({...editProduct, precio: parseFloat(e.target.value)})} />
          <input className="p-2 border rounded" type="number" value={editProduct.stock} onChange={e=>setEditProduct({...editProduct, stock: parseInt(e.target.value)})} />
          <input className="p-2 border rounded" type="number" value={editProduct.stock_minimo} onChange={e=>setEditProduct({...editProduct, stock_minimo: parseInt(e.target.value)})} />
          <textarea className="p-2 border rounded" value={editProduct.descripcion} onChange={e=>setEditProduct({...editProduct, descripcion: e.target.value})} />
          <input type="file" onChange={e=>onEditFile(e.target.files[0])} />
          {preview && <img src={preview} className="w-24 h-24 object-cover rounded" alt="preview" />}
          <div className="flex gap-2">
            <button className="px-4 py-2 bg-emerald-500 text-white rounded" type="submit">Guardar</button>
            <button className="px-4 py-2 bg-gray-300 rounded" type="button" onClick={closeEdit}>Cancelar</button>
          </div>
        </form>
      )}
    </Modal>
    </>
  )
}
