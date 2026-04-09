<template>
  <div class="mb-5">
    <label v-if="label" class="block mb-1.5 text-xs uppercase tracking-wider text-secondary">
      {{ label }}
      <span v-if="required" class="text-error">*</span>
    </label>
    <slot />
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  label?: string
  required?: boolean
}>(), {
  label: '',
  required: false,
})
</script>
