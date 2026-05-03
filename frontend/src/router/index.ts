import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const routes: RouteRecordRaw[] = [
  // ---- 초기 진입 시 /selection으로 리다이렉트 ----
  {
    path: '/',
    redirect: '/selection?view=hero'
  },

  // ---- 메인 서비스 페이지 (DefaultLayout — 전역 헤더 + 푸터 포함) ----
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      { path: 'selection', name: 'Selection', component: () => import('@/views/SelectionView.vue') },
      { path: 'philosophy', name: 'Philosophy', component: () => import('@/views/PhilosophyView.vue') },
      { path: 'interior', redirect: '/contact' },
      { path: 'portfolio', name: 'Portfolio', component: () => import('@/views/PortfolioView.vue') },
      { path: 'contact', name: 'Contact', component: () => import('@/views/ContactView.vue') },
      
      {
        path: 'products',
        name: 'ProductList',
        component: () => import('@/views/products/ProductListView.vue'),
      },
      {
        path: 'products/:id',
        name: 'ProductDetail',
        component: () => import('@/views/products/ProductDetailView.vue'),
        props: true,
      },
      {
        path: 'portfolio/:id',
        name: 'PortfolioDetail',
        component: () => import('@/views/PortfolioDetailView.vue'),
      },
      {
        path: 'selection/:id',
        name: 'SelectionDetail',
        component: () => import('@/views/SelectionDetailView.vue'),
      },
      { path: 'notice', name: 'Notice', component: () => import('@/views/NoticeView.vue') },
      { path: 'showroom', name: 'Showroom', component: () => import('@/views/ShowroomView.vue') },
      { path: 'reservation', name: 'Reservation', component: () => import('@/views/ReservationView.vue') },
      { path: 'cart', name: 'Cart', component: () => import('@/views/CartView.vue') },
      { path: 'login', name: 'Login', component: () => import('@/views/LoginView.vue') },
      { path: 'register', name: 'Register', component: () => import('@/views/RegisterView.vue') },
      { path: 'mypage', name: 'MyPage', component: () => import('@/views/MyPageView.vue') },
      { path: 'brand', name: 'Brand', component: () => import('@/views/BrandView.vue') },
    ],
  },

  // ---- 관리자 로그인 (레이아웃 없음) ----
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('@/views/admin/AdminLoginView.vue'),
  },

  // ---- 관리자 페이지 (AdminLayout) ----
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAdmin: true },
    children: [
      { path: '', name: 'AdminDashboard', component: () => import('@/views/admin/DashboardView.vue') },
      { path: 'portfolio', name: 'AdminPortfolio', component: () => import('@/views/admin/PortfolioAdminView.vue') },
      { path: 'selection', name: 'AdminSelection', component: () => import('@/views/admin/SelectionAdminView.vue') },
      { path: 'slider', name: 'AdminSlider', component: () => import('@/views/admin/SliderAdminView.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    // 랜딩 페이지 내 앵커 이동은 ScrollSnapContainer에서 담당하므로 기본 스크롤 복원 제외
    if (to.hash) return false
    return { top: 0 }
  },
})

// Navigation Guard
router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAdmin) {
    if (!auth.isLoggedIn) {
      return { name: 'AdminLogin' }
    }
    if (!auth.user) {
      try {
        await auth.init()
      } catch {
        return { name: 'AdminLogin' }
      }
    }
    if (!auth.isAdmin) {
      return { name: 'AdminLogin' }
    }
  }
})

export default router
