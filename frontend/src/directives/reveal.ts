import type { Directive, DirectiveBinding } from 'vue'

type RevealValue = {
  delay?: number
  threshold?: number
  once?: boolean
} | undefined

const REVEAL_CLASS = 'is-revealed'
const PREFERS_REDUCED = typeof window !== 'undefined'
  && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

let observer: IntersectionObserver | null = null
const elementMap = new WeakMap<Element, { once: boolean }>()

function ensureObserver() {
  if (observer || typeof window === 'undefined') return observer
  observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const meta = elementMap.get(entry.target)
      if (!meta) continue
      if (entry.isIntersecting) {
        entry.target.classList.add(REVEAL_CLASS)
        if (meta.once) observer?.unobserve(entry.target)
      } else if (!meta.once) {
        entry.target.classList.remove(REVEAL_CLASS)
      }
    }
  }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' })
  return observer
}

export const vReveal: Directive<HTMLElement, RevealValue> = {
  beforeMount(el: HTMLElement, binding: DirectiveBinding<RevealValue>) {
    const opts = binding.value ?? {}
    el.classList.add('reveal')
    if (opts.delay) el.style.transitionDelay = `${opts.delay}ms`
  },
  mounted(el: HTMLElement, binding: DirectiveBinding<RevealValue>) {
    const opts = binding.value ?? {}

    if (PREFERS_REDUCED) {
      el.classList.add(REVEAL_CLASS)
      return
    }

    elementMap.set(el, { once: opts.once ?? true })
    ensureObserver()?.observe(el)
  },
  unmounted(el: HTMLElement) {
    observer?.unobserve(el)
    elementMap.delete(el)
  },
}
