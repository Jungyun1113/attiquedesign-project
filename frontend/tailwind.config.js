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
        brand: '#953735',       // 브랜드 컬러 (변경: #953735)
        accent: '#953735',      // 강조/호버(Hover) 시 사용할 컬러 (변경: #953735)
        background: '#F5F0E8',  // 전체 배경 (크림)
        surface: '#F5F0E8',     // 섹션 배경 (크림 통일)
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
