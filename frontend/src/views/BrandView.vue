<template>
  <div class="brand-page">
    <!-- Hero -->
    <section class="brand-hero">
      <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1920&q=80" alt="Brand" class="hero-bg" />
      <div class="hero-overlay" />
      <div class="hero-content">
        <p class="hero-eyebrow">Since 2024</p>
        <h1 class="hero-title">ATTIQUE DESIGN</h1>
      </div>
    </section>

    <!-- Story -->
    <div class="global-page-container">
      <section class="brand-story">
        <header class="story-header text-center">
          <p class="story-label">Brand Philosophy</p>
          <h2 class="global-eng-subtitle">공간에 깃든 <em>시간의 가치</em></h2>
        </header>
        <div class="story-content">
          <p class="global-kor-desc text-center">
            아띠끄 디자인의 철학은 시선이 닿는 모든 곳이 하나의 흐름으로 이어지는 공간을 만드는 데 있습니다.<br />
            머무는 사람의 일상과 공간 전체가 자연스럽게 어우러지는 밸런스를 고민합니다.<br /><br />
            아띠끄만의 정제된 시선으로 선별한 오브제에 세밀한 맞춤형 인테리어 설계를 더해,<br />
            고객의 고유한 라이프스타일을 섬세하게 엮은 프라이빗 공간을 제안합니다.
          </p>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.brand-page {
  background-color: #F5F0E8;
}

.brand-hero {
  position: relative;
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0,0,0,0.4);
}

.hero-content {
  position: relative;
  text-align: center;
  color: #fff;
  padding: 0 1.5rem;
}

.hero-eyebrow {
  font-family: 'Montserrat', sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.3em;
  opacity: 0.8;
  margin-bottom: 1rem;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 400;
  letter-spacing: 0.05em;
}

.brand-story {
  padding: 4rem 0;
}

.story-header {
  margin-bottom: 4rem;
}

.story-label {
  font-family: 'Montserrat', sans-serif;
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.25em;
  color: #953735;
  margin-bottom: 1.5rem;
}

.story-content {
  max-width: 800px;
  margin: 0 auto;
}

.text-center { text-align: center; }

@media (max-width: 768px) {
  .brand-hero { height: 50vh; }
  .brand-story { padding: 2rem 0; }
}
</style>
