import { useEffect, useState } from 'react'
import api from '../services/api'

export default function useVentas(){
  const [ventas, setVentas] = useState([])
  const fetch = async ()=>{
    const res = await api.get('/ventas')
    setVentas(res.data)
  }
  useEffect(()=>{fetch()}, [])
  return {ventas, refresh: fetch}
}
