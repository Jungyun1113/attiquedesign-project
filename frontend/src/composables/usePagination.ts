// ============================================================
// Pagination Composable — 공통 페이징 로직
// ============================================================
import { ref, computed } from 'vue'

export function usePagination(initialPageSize = 12) {
  const currentPage = ref(1)
  const pageSize = ref(initialPageSize)
  const totalCount = ref(0)

  const totalPages = computed(() => Math.ceil(totalCount.value / pageSize.value))
  const hasNext = computed(() => currentPage.value < totalPages.value)
  const hasPrev = computed(() => currentPage.value > 1)

  function nextPage() {
    if (hasNext.value) currentPage.value++
  }
  function prevPage() {
    if (hasPrev.value) currentPage.value--
  }
  function goToPage(page: number) {
    currentPage.value = Math.max(1, Math.min(page, totalPages.value))
  }

  return { currentPage, pageSize, totalCount, totalPages, hasNext, hasPrev, nextPage, prevPage, goToPage }
}
