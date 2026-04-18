import api from './api'
import type { LoginRequest, LoginResponse } from '@/types/api.d'

export const authService = {
  async login(payload: LoginRequest): Promise<LoginResponse> {
    const { data } = await api.post('/auth/login', payload)
    const tokens = data.data as { access_token: string; refresh_token: string; token_type: string }
    const meRes = await api.get('/auth/me', {
      headers: { Authorization: `Bearer ${tokens.access_token}` },
    })
    return {
      access_token: tokens.access_token,
      refresh_token: tokens.refresh_token,
      user: meRes.data.data,
    }
  },

  async register(payload: { email: string; password: string; name: string; phone: string }) {
    const { data } = await api.post('/auth/register', payload)
    return data
  },

  async getMe() {
    const { data } = await api.get('/auth/me')
    return data.data
  },
}
