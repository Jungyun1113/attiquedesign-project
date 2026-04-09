// ============================================================
// Toast Composable — 전역 알림 시스템
// ============================================================
import { ref } from 'vue'

export interface ToastItem {
  id: number
  type: 'success' | 'error' | 'info'
  message: string
}

const toasts = ref<ToastItem[]>([])
let nextId = 0

export function useToast() {
  function show(type: ToastItem['type'], message: string, duration = 3000) {
    const id = nextId++
    toasts.value.push({ id, type, message })
    setTimeout(() => {
      toasts.value = toasts.value.filter((t) => t.id !== id)
    }, duration)
  }

  return {
    toasts,
    showSuccess: (msg: string) => show('success', msg),
    showError: (msg: string) => show('error', msg),
    showInfo: (msg: string) => show('info', msg),
  }
}
