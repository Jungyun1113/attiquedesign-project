// ============================================================
// Auth Store (Pinia) — 로그인 상태 및 사용자 정보 관리
// ============================================================
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/api.d'
import { authService } from '@/services/auth.service'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))

  const isLoggedIn = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.role === 'ADMIN')

  async function login(email: string, password: string) {
    const res = await authService.login({ email, password })
    accessToken.value = res.access_token
    user.value = res.user
    localStorage.setItem('access_token', res.access_token)
    localStorage.setItem('refresh_token', res.refresh_token)
  }

  function logout() {
    user.value = null
    accessToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async function init() {
    if (accessToken.value && !user.value) {
      try {
        user.value = await authService.getMe()
      } catch {
        logout()
      }
    }
  }

  return { user, accessToken, isLoggedIn, isAdmin, login, logout, init }
})
