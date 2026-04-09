// ============================================================
// Auth Service — 로그인 / 회원가입 API
// Mock 모드: MOCK_LOGIN_RESPONSE를 즉시 반환
// ============================================================
// import api from './api'
import type { LoginRequest, LoginResponse } from '@/types/api.d'
import { MOCK_LOGIN_RESPONSE } from '@/mocks/data'

const USE_MOCK = true // TODO: 실제 API 연동 시 false로 변경

export const authService = {
  async login(payload: LoginRequest): Promise<LoginResponse> {
    if (USE_MOCK) {
      return new Promise((resolve) =>
        setTimeout(() => resolve(MOCK_LOGIN_RESPONSE), 500),
      )
    }
    // const { data } = await api.post('/auth/login', payload)
    // return data.data as LoginResponse
    throw new Error('Real API not implemented')
  },

  async register(payload: { email: string; password: string; name: string; phone: string }) {
    if (USE_MOCK) {
      return new Promise((resolve) => setTimeout(() => resolve({ success: true }), 500))
    }
    // const { data } = await api.post('/auth/register', payload)
    // return data
    throw new Error('Real API not implemented')
  },
}
