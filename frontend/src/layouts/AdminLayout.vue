<template>
  <div class="min-h-screen flex bg-surface">
    <aside class="w-64 bg-primary text-white hidden md:flex flex-col">
      <div class="p-6 border-b border-white/10">
        <router-link to="/" class="font-serif text-xl tracking-wide">ATTIQUE</router-link>
        <p class="text-[10px] text-white/50 mt-1 uppercase tracking-widest">Admin Panel</p>
      </div>
      <nav class="flex-1 p-4 flex flex-col gap-1">
        <router-link to="/admin" class="px-4 py-2.5 text-xs uppercase tracking-wider text-white/70 hover:text-white hover:bg-white/10 transition-colors rounded">
          대시보드
        </router-link>
        <router-link to="/admin/portfolio" class="px-4 py-2.5 text-xs uppercase tracking-wider text-white/70 hover:text-white hover:bg-white/10 transition-colors rounded">
          포트폴리오 관리
        </router-link>
        <router-link to="/admin/selection" class="px-4 py-2.5 text-xs uppercase tracking-wider text-white/70 hover:text-white hover:bg-white/10 transition-colors rounded">
          셀렉션 관리
        </router-link>
        <router-link to="/admin/products" class="px-4 py-2.5 text-xs uppercase tracking-wider text-white/70 hover:text-white hover:bg-white/10 transition-colors rounded">
          상품 관리
        </router-link>
      </nav>
      <div class="p-4 border-t border-white/10">
        <button class="w-full text-left px-4 py-2 text-xs text-white/50 hover:text-white transition-colors" @click="logout">
          로그아웃
        </button>
      </div>
    </aside>
    <main class="flex-1 p-6 md:p-10 overflow-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>
