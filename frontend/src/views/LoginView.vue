<template>
  <div class="container-page section-gap max-w-md mx-auto">
    <div class="text-center mb-10">
      <h1 class="font-serif text-3xl mb-2">로그인</h1>
      <p class="text-sm text-secondary">아띠끄디자인에 오신 것을 환영합니다.</p>
    </div>

    <form @submit.prevent="handleLogin" class="space-y-1">
      <FormItem label="이메일">
        <BaseInput v-model="email" type="email" placeholder="email@example.com" :error="errors.email" />
      </FormItem>
      <FormItem label="비밀번호">
        <BaseInput v-model="password" type="password" placeholder="비밀번호를 입력하세요" :error="errors.password" />
      </FormItem>
      <div class="pt-4 md:static fixed bottom-0 left-0 right-0 md:p-0 p-4 bg-white md:bg-transparent border-t md:border-0 border-surface z-40">
        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>
      </div>
    </form>

    <!-- 데모 안내 -->
    <div class="mt-8 p-4 bg-surface text-center">
      <p class="text-xs text-secondary mb-2">🔑 데모 계정</p>
      <p class="text-xs text-primary">demo@attique.co.kr / 아무 비밀번호</p>
    </div>

    <!-- 회원가입 유도 -->
    <div class="mt-6 text-center">
      <p class="text-xs text-secondary mb-1">아직 회원이 아니신가요?</p>
      <p class="text-xs text-accent mb-3">회원가입 시 더 원활한 혜택을 제공합니다.</p>
      <router-link to="/register" class="btn-outline text-xs">회원가입</router-link>
    </div>

    <!-- 소셜 로그인 (UI만) -->
    <div class="mt-8 space-y-3">
      <button class="w-full py-3 border border-surface text-sm text-secondary hover:border-accent transition-colors">
        카카오로 시작하기
      </button>
      <button class="w-full py-3 border border-surface text-sm text-secondary hover:border-accent transition-colors">
        네이버로 시작하기
      </button>
      <button class="w-full py-3 border border-surface text-sm text-secondary hover:border-accent transition-colors">
        Apple로 시작하기
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useToast } from '@/composables/useToast'
import FormItem from '@/components/common/FormItem.vue'
import BaseInput from '@/components/common/BaseInput.vue'

const router = useRouter()
const authStore = useAuthStore()
const { showSuccess, showError } = useToast()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errors = reactive({ email: '', password: '' })

async function handleLogin() {
  errors.email = email.value ? '' : '이메일을 입력해주세요.'
  errors.password = password.value ? '' : '비밀번호를 입력해주세요.'
  if (errors.email || errors.password) return

  loading.value = true
  try {
    await authStore.login(email.value, password.value)
    showSuccess('로그인되었습니다.')
    router.push('/')
  } catch {
    showError('로그인에 실패했습니다.')
  } finally {
    loading.value = false
  }
}
</script>
