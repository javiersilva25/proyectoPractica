import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import Login from './components/Login'
import Dashboard from './pages/Dashboard'
import RutaPrivada from './components/RutaPrivada'
import Registro from './components/Register'
import DocumentosCliente from './components/DocumentoCliente'
import { Toaster } from 'react-hot-toast'
import DashboardGerente from './pages/DashboardGerente'



export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route
          path="/dashboard"
          element={
            <RutaPrivada>
              <Dashboard />
            </RutaPrivada>
          }
        />
        <Route
          path="/cliente/documentos"
          element={
            <RutaPrivada>
              <DocumentosCliente />
            </RutaPrivada>
          }
        />
        <Route
          path="/dashboard/gerente"
          element={
            <RutaPrivada>
              <DashboardGerente />
            </RutaPrivada>
          }
        />
      </Routes>
      <Toaster position="top-right" reverseOrder={false} />
    </Router>
  )
}
