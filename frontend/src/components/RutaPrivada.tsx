import { Navigate } from 'react-router-dom'
import type { ReactNode } from 'react'

interface RutaPrivadaProps {
  children: ReactNode
}

export default function RutaPrivada({ children }: RutaPrivadaProps) {
  const token = localStorage.getItem('access')
  return token ? children : <Navigate to="/login" />
}
