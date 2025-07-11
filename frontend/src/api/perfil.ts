import api from './axios'

export const obtenerPerfil = () =>
  api.get('perfil/', { withCredentials: true })
