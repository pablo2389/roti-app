import { useEffect, useState } from 'react'
import api from '../services/api'

export default function useProductos(){
  const [productos, setProductos] = useState([])
  const fetch = async ()=>{
    const res = await api.get('/productos')
    setProductos(res.data)
  }
  useEffect(()=>{fetch()}, [])
  return {productos, refresh: fetch}
}
