// ============================================================
// Cart Store (Pinia) — 장바구니, localStorage 영속성 지원
// ============================================================
import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import type { CartItem, Product } from '@/types/api.d'

const STORAGE_KEY = 'attique_cart'

function loadCart(): CartItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>(loadCart())

  const totalCount = computed(() => items.value.reduce((sum, i) => sum + i.quantity, 0))
  const totalPrice = computed(() =>
    items.value.reduce((sum, i) => sum + (i.product.price ?? 0) * i.quantity, 0),
  )

  function addItem(product: Product, qty = 1) {
    const existing = items.value.find((i) => i.product.id === product.id)
    if (existing) {
      existing.quantity += qty
    } else {
      items.value.push({ product, quantity: qty })
    }
  }

  function removeItem(productId: string) {
    items.value = items.value.filter((i) => i.product.id !== productId)
  }

  function updateQuantity(productId: string, qty: number) {
    const item = items.value.find((i) => i.product.id === productId)
    if (item) item.quantity = Math.max(1, qty)
  }

  function clearCart() {
    items.value = []
  }

  // localStorage 자동 동기화
  watch(items, (val) => localStorage.setItem(STORAGE_KEY, JSON.stringify(val)), { deep: true })

  return { items, totalCount, totalPrice, addItem, removeItem, updateQuantity, clearCart }
})
