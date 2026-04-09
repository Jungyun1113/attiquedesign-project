import { ref, onMounted, onUnmounted } from 'vue'

/**
 * Intersection Observer 기반으로 현재 뷰포트에 보이는 섹션의 인덱스를 실시간 반환하는 Composable.
 *
 * 핵심 수정:
 * - ScrollSnapContainer(.scroll-snap-container)가 실제 스크롤 root이므로,
 *   document.querySelector로 해당 컨테이너를 찾아 root로 지정한다.
 * - threshold를 [0.4, 0.5]로 복수 지정해 섹션이 50% 진입하는 순간을 정확히 포착한다.
 * - 여러 entry가 동시에 isIntersecting일 때, intersectionRatio가 가장 높은 것을 활성 섹션으로 선택한다.
 *
 * @param sectionIds - 감지할 섹션 ID 배열 (순서 보장)
 */
export function useActiveSection(sectionIds: string[]) {
  const activeSectionIndex = ref(0)
  let observer: IntersectionObserver | null = null

  onMounted(() => {
    // 실제 스크롤이 발생하는 컨테이너
    const scrollRoot = document.querySelector('.scroll-snap-container') as HTMLElement | null

    observer = new IntersectionObserver(
      (entries) => {
        // isIntersecting 중 ratio가 가장 높은 entry를 active로 선택
        let bestEntry: IntersectionObserverEntry | null = null

        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            if (!bestEntry || entry.intersectionRatio > bestEntry.intersectionRatio) {
              bestEntry = entry
            }
          }
        })

        if (bestEntry) {
          const index = sectionIds.indexOf((bestEntry as IntersectionObserverEntry).target.id)
          if (index !== -1) {
            activeSectionIndex.value = index
          }
        }
      },
      {
        root: scrollRoot,          // ← 핵심: window 대신 스크롤 컨테이너를 root로 지정
        threshold: [0.4, 0.5, 0.6], // 40%~60% 진입 시 감지 (스냅 특성상 여유 있게)
        rootMargin: '0px',
      }
    )

    sectionIds.forEach((id) => {
      const el = document.getElementById(id)
      if (el) observer?.observe(el)
    })
  })

  onUnmounted(() => {
    observer?.disconnect()
  })

  function scrollToSection(id: string) {
    const scrollRoot = document.querySelector('.scroll-snap-container') as HTMLElement | null
    const el = document.getElementById(id)

    if (!el) return

    if (scrollRoot) {
      // 스냅 컨테이너 내부에서 부드럽게 스크롤
      scrollRoot.scrollTo({
        top: el.offsetTop,
        behavior: 'smooth',
      })
    } else {
      el.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return { activeSectionIndex, scrollToSection }
}
