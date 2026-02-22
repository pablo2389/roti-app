import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Generador from './pages/Generador'
import Productos from './pages/Productos'
import Ventas from './pages/Ventas'

export default function App(){
  return (
    <BrowserRouter>
      <div className="p-4">
        <nav className="mb-4">
          <Link to="/" className="mr-4">Dashboard</Link>
          <Link to="/productos" className="mr-4">Productos</Link>
          <Link to="/ventas" className="mr-4">Ventas</Link>
          <Link to="/generador">Generador</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard/>} />
          <Route path="/productos" element={<Productos/>} />
          <Route path="/ventas" element={<Ventas/>} />
          <Route path="/generador" element={<Generador/>} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
