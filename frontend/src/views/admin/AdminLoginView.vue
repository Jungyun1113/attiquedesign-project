<template>
  <div class="login-wrap">
    <div class="login-box">
      <div class="login-header">
        <p class="login-brand">ATTIQUE</p>
        <p class="login-sub">Admin</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="field">
          <label>이메일</label>
          <input v-model="email" type="email" placeholder="admin@example.com" autocomplete="username" required />
        </div>
        <div class="field">
          <label>비밀번호</label>
          <input v-model="password" type="password" placeholder="••••••••" autocomplete="current-password" required />
        </div>

        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

        <button type="submit" :disabled="loading" class="submit-btn">
          <span v-if="loading" class="spinner" />
          <span v-else>로그인</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  loading.value = true
  errorMsg.value = ''
  try {
    await authStore.login(email.value, password.value)
    if (!authStore.isAdmin) {
      authStore.logout()
      errorMsg.value = '관리자 계정이 아닙니다.'
      return
    }
    router.push('/admin')
  } catch {
    errorMsg.value = '이메일 또는 비밀번호를 확인해주세요.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f4f4;
}

.login-box {
  background: #fff;
  padding: 48px 40px;
  width: 360px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-brand {
  font-family: serif;
  font-size: 22px;
  letter-spacing: 0.15em;
  color: #1a1a1a;
  margin: 0;
}

.login-sub {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: #999;
  margin: 4px 0 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field label {
  font-size: 12px;
  font-weight: 500;
  color: #444;
}

.field input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.field input:focus {
  border-color: #333;
}

.error-msg {
  font-size: 12px;
  color: #c0392b;
  margin: 0;
}

.submit-btn {
  margin-top: 8px;
  padding: 12px;
  background: #1a1a1a;
  color: #fff;
  border: none;
  font-size: 13px;
  letter-spacing: 0.05em;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 44px;
  transition: background 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #333;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
