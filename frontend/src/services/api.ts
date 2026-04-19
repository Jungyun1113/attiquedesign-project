import axios from 'axios'
import { useToast } from '@/composables/useToast'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

// Request Interceptor — JWT 토큰 자동 첨부 + GET 캐시 버스팅
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  // GET 요청에 cache-busting 파라미터 추가 (브라우저 캐시 방지)
  if (config.method === 'get') {
    config.params = {
      ...config.params,
      _t: Date.now(),
    }
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
    if (error.response?.status === 401) {
      // 401 에러(토큰 만료/권한 없음) 발생 시 자동 로그아웃 처리
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      if (window.location.pathname.startsWith('/admin') && window.location.pathname !== '/admin/login') {
        window.location.href = '/admin/login'
      }
    }
    
    const message = error.response?.data?.error?.message || '요청 처리 중 오류가 발생했습니다.'
    const { showError } = useToast()
    showError(message)
    return Promise.reject(error)
  },
)

export default api
