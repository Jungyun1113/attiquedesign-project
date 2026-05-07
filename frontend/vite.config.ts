import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import Sitemap from 'vite-plugin-sitemap'

const staticRoutes = [
  '/',
  '/selection',
  '/philosophy',
  '/interior',
  '/portfolio',
  '/contact',
  '/products',
  '/notice',
  '/showroom',
  '/reservation',
  '/cart',
  '/login',
  '/register',
  '/mypage',
  '/brand',
  '/privacy',
  '/terms',
]

export default defineConfig({
  plugins: [
    vue(),
    Sitemap({
      hostname: 'https://attiquedesign.com/',
      dynamicRoutes: staticRoutes,
      exclude: ['/admin', '/admin/login', '/admin/portfolio', '/admin/selection', '/admin/slider'],
    }),
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    host: true,
    port: 5173,
  },
})
