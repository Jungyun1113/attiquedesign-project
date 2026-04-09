// ============================================================
// Mock 데이터 — 실제 API 연동 시 이 파일 전체를 제거하면 됩니다.
// ============================================================
import type {
  User, Product, Category, Order, Reservation, LoginResponse,
} from '@/types/api.d'

// ---- 사용자 ----
export const MOCK_ADMIN_USER: User = {
  id: 'u-admin-001',
  email: 'admin@attique.co.kr',
  name: '관리자',
  phone: '010-0000-0000',
  role: 'ADMIN',
  auth_provider: 'LOCAL',
  created_at: '2026-01-01T00:00:00Z',
}

export const MOCK_USER: User = {
  id: 'u-user-001',
  email: 'demo@attique.co.kr',
  name: '김아띠',
  phone: '010-1234-5678',
  role: 'USER',
  auth_provider: 'LOCAL',
  created_at: '2026-02-15T00:00:00Z',
}

export const MOCK_LOGIN_RESPONSE: LoginResponse = {
  access_token: 'mock-access-token-xyz',
  refresh_token: 'mock-refresh-token-xyz',
  user: MOCK_USER,
}

// ---- 카테고리 ----
export const MOCK_CATEGORIES: Category[] = [
  { id: 'cat-01', name: 'Sofa', slug: 'sofa', parent_type: 'FURNITURE' },
  { id: 'cat-02', name: 'Chair / Stool', slug: 'chair-stool', parent_type: 'FURNITURE' },
  { id: 'cat-03', name: 'Table / Desk', slug: 'table-desk', parent_type: 'FURNITURE' },
  { id: 'cat-04', name: 'Cabinet / Storage', slug: 'cabinet-storage', parent_type: 'FURNITURE' },
  { id: 'cat-05', name: 'Bed', slug: 'bed', parent_type: 'FURNITURE' },
  { id: 'cat-06', name: 'Lighting', slug: 'lighting', parent_type: 'ACCESSORY' },
  { id: 'cat-07', name: 'Fabric', slug: 'fabric', parent_type: 'ACCESSORY' },
  { id: 'cat-08', name: 'Object / Decor', slug: 'object-decor', parent_type: 'ACCESSORY' },
  { id: 'cat-09', name: 'Kitchen / Dining', slug: 'kitchen-dining', parent_type: 'ACCESSORY' },
]

// ---- 상품 ----
export const MOCK_PRODUCTS: Product[] = [
  {
    id: 'p-001', sku: 'SOFA-001', name: 'Brera 3인 소파', type: 'FURNITURE',
    price: null, stock_quantity: 1, status: 'ACTIVE', category_id: 'cat-01',
    category_name: 'Sofa',
    thumbnail_url: 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80',
    hover_image_url: 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=800&q=80',
    description: '이탈리아 장인의 핸드메이드 소파. 최상급 가죽과 단단한 프레임이 조화를 이룹니다.',
    designer_story: 'Brera 컬렉션은 밀라노 가구박람회에서 영감을 받아 탄생했습니다.',
  },
  {
    id: 'p-002', sku: 'CHAIR-001', name: 'Eames 라운지 체어', type: 'FURNITURE',
    price: null, stock_quantity: 2, status: 'ACTIVE', category_id: 'cat-02',
    category_name: 'Chair / Stool',
    thumbnail_url: 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=800&q=80',
    hover_image_url: 'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=800&q=80',
    description: '클래식한 디자인의 라운지 체어입니다.',
  },
  {
    id: 'p-003', sku: 'TABLE-001', name: '오크 다이닝 테이블', type: 'FURNITURE',
    price: null, stock_quantity: 1, status: 'ACTIVE', category_id: 'cat-03',
    category_name: 'Table / Desk',
    thumbnail_url: 'https://images.unsplash.com/photo-1611269154421-4e27233ac5c7?w=800&q=80',
    hover_image_url: 'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=800&q=80',
    description: '유럽산 오크 원목으로 제작된 넉넉한 6인용 다이닝 테이블입니다.',
  },
  {
    id: 'p-004', sku: 'LIGHT-001', name: 'Arco 플로어 램프', type: 'ACCESSORY',
    price: 890000, stock_quantity: 5, status: 'ACTIVE', category_id: 'cat-06',
    category_name: 'Lighting',
    thumbnail_url: 'https://images.unsplash.com/photo-1507473885765-e6ed057ab6fe?w=800&q=80',
    hover_image_url: 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=800&q=80',
    description: '모던 클래식 무드의 아크 스탠드 조명입니다.',
  },
  {
    id: 'p-005', sku: 'DECO-001', name: '핸드메이드 세라믹 화병', type: 'ACCESSORY',
    price: 320000, stock_quantity: 8, status: 'ACTIVE', category_id: 'cat-08',
    category_name: 'Object / Decor',
    thumbnail_url: 'https://images.unsplash.com/photo-1612196808214-b7e239e5f6a2?w=800&q=80',
    description: '도예 작가의 핸드메이드 화병. 미세한 유약 변화가 자연스러운 아름다움을 만듭니다.',
  },
  {
    id: 'p-006', sku: 'FABRIC-001', name: '캐시미어 블랑켓', type: 'ACCESSORY',
    price: 450000, stock_quantity: 3, status: 'ACTIVE', category_id: 'cat-07',
    category_name: 'Fabric',
    thumbnail_url: 'https://images.unsplash.com/photo-1629949009765-62c1075e0594?w=800&q=80',
    description: '최고급 몽골리안 캐시미어로 직조한 블랑켓입니다.',
  },
  {
    id: 'p-007', sku: 'KITCHEN-001', name: '쉐프 나이프 세트', type: 'ACCESSORY',
    price: 680000, stock_quantity: 0, status: 'SOLDOUT', category_id: 'cat-09',
    category_name: 'Kitchen / Dining',
    thumbnail_url: 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=800&q=80',
    description: '일본 사카이 제작 프리미엄 쉐프 나이프 5종 세트입니다.',
  },
  {
    id: 'p-008', sku: 'BED-001', name: 'Grand Canopy 킹 베드', type: 'FURNITURE',
    price: null, stock_quantity: 1, status: 'ACTIVE', category_id: 'cat-05',
    category_name: 'Bed',
    thumbnail_url: 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&q=80',
    description: '캐노피 디자인의 프리미엄 킹사이즈 베드 프레임입니다.',
  },
]

// ---- 포트폴리오 ----
export const MOCK_PORTFOLIO = [
  {
    id: 'pf-01',
    title: '한남동 타운하우스 68평',
    subtitle: '토탈 인테리어 설계 및 시공',
    image: 'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1200&q=80',
    tags: ['주거', '68평', '토탈'],
  },
  {
    id: 'pf-02',
    title: '압구정 펜트하우스 42평',
    subtitle: '홈스타일링 & 가구 컨설팅',
    image: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1200&q=80',
    tags: ['주거', '42평', '스타일링'],
  },
  {
    id: 'pf-03',
    title: '성수동 카페 인테리어',
    subtitle: '상업 공간 토탈 디자인',
    image: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200&q=80',
    tags: ['상업', '카페', '토탈'],
  },
]

// ---- 주문 ----
export const MOCK_ORDERS: Order[] = [
  {
    id: 'ord-001',
    user_id: 'u-user-001',
    guest_email: null, guest_phone: null, guest_name: null,
    total_amount: 1210000,
    status: 'DELIVERED',
    pg_transaction_id: 'pg-tr-001',
    items: [
      { id: 'oi-01', order_id: 'ord-001', product_id: 'p-004', product_name: 'Arco 플로어 램프', quantity: 1, unit_price: 890000 },
      { id: 'oi-02', order_id: 'ord-001', product_id: 'p-005', product_name: '핸드메이드 세라믹 화병', quantity: 1, unit_price: 320000 },
    ],
    created_at: '2026-03-10T14:23:00Z',
  },
]

// ---- 예약 ----
export const MOCK_RESERVATIONS: Reservation[] = [
  {
    id: 'res-001',
    user_id: 'u-user-001',
    guest_info: null,
    reservation_type: 'INTERIOR',
    status: 'IN_PROGRESS',
    expected_date: '2026-04-01T14:00:00Z',
    dynamic_data: { space_type: 'APT', size: '42평', budget: '1억 ~ 1.5억', address: '서울시 강남구 압구정동' },
    created_at: '2026-03-18T10:00:00Z',
  },
]
