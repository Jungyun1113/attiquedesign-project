import axios from 'axios'
import { useToast } from '@/composables/useToast'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

// Request Interceptor — JWT 토큰 자동 첨부
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response Interceptor — 표준 에러 처리 + useToast 연동
api.interceptors.response.use(
  (response) => {
    if (response.data && response.data.success === false) {
      const message = response.data.error?.message || '요청 처리 중 오류가 발생했습니다.'
      const { showError } = useToast()
      showError(message)
      return Promise.reject(new Error(message))
    }
    return response
  },
  (error) => {
    const message = error.response?.data?.error?.message || '요청 처리 중 오류가 발생했습니다.'
    const { showError } = useToast()
    showError(message)
    return Promise.reject(error)
  },
)

export default api
