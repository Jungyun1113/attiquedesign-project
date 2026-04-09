<template>
  <div>
    <section class="relative h-[70vh] flex items-center justify-center overflow-hidden">
      <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1920&q=80" alt="Interior" class="absolute inset-0 w-full h-full object-cover" />
      <div class="absolute inset-0 bg-black/40" />
      <div class="relative text-center text-white px-4">
        <p class="text-xs uppercase tracking-[0.3em] mb-3 opacity-70">Interior Design</p>
        <h1 class="font-serif text-4xl md:text-6xl">공간, 다시 설계하다</h1>
      </div>
    </section>
    <section class="section-gap">
      <div class="container-page max-w-3xl text-center">
        <p class="text-xs uppercase tracking-[0.2em] text-accent mb-4">Process</p>
        <h2 class="font-serif text-3xl md:text-4xl mb-12">프리미엄 인테리어 프로세스</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div v-for="(step, i) in steps" :key="i" class="text-center">
            <div class="w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center mx-auto mb-4">
              <span class="text-accent font-serif text-lg">{{ i + 1 }}</span>
            </div>
            <h3 class="font-sans text-sm font-medium mb-2">{{ step.title }}</h3>
            <p class="text-xs text-secondary leading-relaxed">{{ step.desc }}</p>
          </div>
        </div>
        <div class="mt-12">
          <router-link to="/reservation" class="btn-primary">1:1 상담 예약하기</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const steps = [
  { title: '프라이빗 상담', desc: '한남 쇼룸에서 1:1 맞춤 상담으로 고객의 라이프스타일과 공간을 깊이 이해합니다.' },
  { title: '컨셉 설계 & 견적', desc: '공간 콘셉트 보드와 3D 시뮬레이션을 통해 완성될 공간을 미리 경험합니다.' },
  { title: '시공 & 스타일링', desc: '전문 시공팀의 꼼꼼한 시공과 가구·소품 배치까지 원스톱으로 완성합니다.' },
]
</script>
