<template>
  <div class="w-full">
    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :class="[
        'w-full px-4 py-3 bg-surface border font-sans text-sm transition-colors duration-200 focus:outline-none focus:border-accent',
        error ? 'border-error' : 'border-transparent',
      ]"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="error" class="mt-1 text-xs text-error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  modelValue: string
  type?: string
  placeholder?: string
  error?: string
}>(), {
  type: 'text',
  placeholder: '',
  error: '',
})

defineEmits<{ 'update:modelValue': [value: string] }>()
</script>
