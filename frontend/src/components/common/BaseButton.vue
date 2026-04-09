<template>
  <button
    :class="[baseClass, variantClass, { 'opacity-50 cursor-not-allowed': disabled }]"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{
  variant?: 'solid' | 'outline' | 'ghost'
  disabled?: boolean
}>(), {
  variant: 'solid',
  disabled: false,
})

defineEmits<{ click: [] }>()

const baseClass = 'inline-flex items-center justify-center font-sans text-sm tracking-wider uppercase transition-all duration-300 ease-out focus:outline-none'

const variantMap: Record<string, string> = {
  solid: 'bg-primary text-white px-6 py-3 hover:bg-accent',
  outline: 'border border-primary text-primary px-6 py-3 hover:bg-primary hover:text-white',
  ghost: 'text-primary px-4 py-2 hover:text-accent',
}

const variantClass = variantMap[props.variant]
</script>
