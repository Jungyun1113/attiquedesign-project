<template>
  <div>
    <!-- Map/Image section -->
    <section class="relative h-[60vh] flex items-center justify-center overflow-hidden bg-surface">
      <img src="https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?w=1920&q=80" alt="Hannam Showroom" class="absolute inset-0 w-full h-full object-cover" />
      <div class="absolute inset-0 bg-black/30" />
      <div class="relative text-center text-white px-4">
        <p class="text-xs uppercase tracking-[0.3em] mb-3 opacity-70">Hannam-dong, Seoul</p>
        <h1 class="font-serif text-4xl md:text-5xl">Showroom</h1>
      </div>
    </section>
    <section class="section-gap">
      <div class="container-page max-w-2xl text-center">
        <h2 class="font-serif text-2xl md:text-3xl mb-6">한남동 쇼룸 안내</h2>
        <div class="text-sm text-secondary leading-loose mb-10">
          <p>서울특별시 용산구 한남동 000-00</p>
          <p>월–토 11:00 – 19:00 (일요일 예약제, 공휴일 휴무)</p>
          <p>Tel. 02-000-0000</p>
        </div>
        <router-link to="/reservation" class="btn-primary">1:1 프라이빗 방문 상담 예약</router-link>
      </div>
    </section>
  </div>
</template>
