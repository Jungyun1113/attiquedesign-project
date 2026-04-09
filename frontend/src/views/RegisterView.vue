<template>
  <div class="container-page section-gap max-w-md mx-auto">
    <div class="text-center mb-10">
      <h1 class="font-serif text-3xl mb-2">회원가입</h1>
      <p class="text-sm text-secondary">아띠끄디자인의 특별한 혜택을 누려보세요.</p>
    </div>

    <form @submit.prevent="handleRegister" class="space-y-1">
      <FormItem label="이름" :required="true">
        <BaseInput v-model="form.name" placeholder="이름을 입력하세요" :error="errors.name" />
      </FormItem>
      <FormItem label="이메일" :required="true">
        <BaseInput v-model="form.email" type="email" placeholder="email@example.com" :error="errors.email" />
      </FormItem>
      <FormItem label="전화번호" :required="true">
        <BaseInput v-model="form.phone" placeholder="010-0000-0000" :error="errors.phone" />
      </FormItem>
      <FormItem label="비밀번호" :required="true">
        <BaseInput v-model="form.password" type="password" placeholder="비밀번호 (8자 이상)" :error="errors.password" />
      </FormItem>
      <FormItem label="비밀번호 확인" :required="true">
        <BaseInput v-model="form.passwordConfirm" type="password" placeholder="비밀번호를 다시 입력하세요" :error="errors.passwordConfirm" />
      </FormItem>
      <div class="pt-4">
        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? '가입 중...' : '회원가입' }}
        </button>
      </div>
    </form>

    <div class="mt-6 text-center">
      <p class="text-xs text-secondary">이미 회원이신가요? <router-link to="/login" class="text-accent hover:underline">로그인</router-link></p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '@/composables/useToast'
import { authService } from '@/services/auth.service'
import FormItem from '@/components/common/FormItem.vue'
import BaseInput from '@/components/common/BaseInput.vue'

const router = useRouter()
const { showSuccess, showError } = useToast()
const loading = ref(false)

const form = reactive({ name: '', email: '', phone: '', password: '', passwordConfirm: '' })
const errors = reactive({ name: '', email: '', phone: '', password: '', passwordConfirm: '' })

async function handleRegister() {
  errors.name = form.name ? '' : '이름을 입력해주세요.'
  errors.email = form.email ? '' : '이메일을 입력해주세요.'
  errors.phone = form.phone ? '' : '전화번호를 입력해주세요.'
  errors.password = form.password.length >= 8 ? '' : '비밀번호는 8자 이상이어야 합니다.'
  errors.passwordConfirm = form.password === form.passwordConfirm ? '' : '비밀번호가 일치하지 않습니다.'
  if (Object.values(errors).some(e => e)) return

  loading.value = true
  try {
    await authService.register({ email: form.email, password: form.password, name: form.name, phone: form.phone })
    showSuccess('회원가입이 완료되었습니다. 로그인해주세요.')
    router.push('/login')
  } catch {
    showError('회원가입에 실패했습니다.')
  } finally {
    loading.value = false
  }
}
</script>
