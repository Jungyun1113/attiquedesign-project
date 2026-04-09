/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2B1D1B',     // 메인 텍스트 (완전한 블랙보다 부드럽고 따뜻한 차콜브라운)
        secondary: '#6D6059',   // 서브 텍스트 및 안내 문구
        brand: '#522B29',       // 브랜드 컬러 (첨부 이미지의 우아한 브릭-버건디 컬러)
        accent: '#6A3735',      // 강조/호버(Hover) 시 사용할 톤온톤 버건디
        background: '#FDFBF8',  // 전체 배경 (따뜻하고 우아한 아이보리)
        surface: '#F7F4EE',     // 카드나 섹션 배경 (약간 더 톤다운된 베이지)
        border: '#E8E2D7',      // 은은한 구분선 색상
      },
      fontFamily: {
        sans: ['Pretendard', 'Inter', 'sans-serif'],
        serif: ['Playfair Display', 'Nanum Myeongjo', 'serif'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      transitionDuration: {
        '400': '400ms',
      },
    },
  },
  plugins: [],
}
