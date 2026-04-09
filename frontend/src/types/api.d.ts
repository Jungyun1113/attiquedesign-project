// ============================================================
// API 공통 응답 타입 (2_api_spec.md 기반)
// ============================================================

/** 페이징 메타 정보 */
export interface PaginationMeta {
  page: number
  size: number
  total_pages: number
  total_count: number
}

/** 성공 응답 */
export interface ApiSuccessResponse<T> {
  success: true
  data: T
  meta?: PaginationMeta
}

/** 에러 응답 */
export interface ApiErrorResponse {
  success: false
  error: {
    code: string
    message: string
  }
}

/** 통합 API 응답 */
export type ApiResponse<T> = ApiSuccessResponse<T> | ApiErrorResponse

// ============================================================
// 도메인 모델 타입 (1_database_model.md 기반)
// ============================================================

export type UserRole = 'ADMIN' | 'USER'
export type AuthProvider = 'LOCAL' | 'KAKAO' | 'NAVER' | 'APPLE'
export type ProductType = 'FURNITURE' | 'ACCESSORY'
export type ProductStatus = 'ACTIVE' | 'HIDDEN' | 'SOLDOUT'
export type OrderStatus = 'PENDING' | 'PAID' | 'SHIPPED' | 'DELIVERED' | 'CANCELLED'
export type ReservationType = 'INTERIOR' | 'FURNITURE' | 'TOTAL'
export type ReservationStatus = 'RECEIVED' | 'IN_PROGRESS' | 'QUOTED' | 'CONTRACTED' | 'NOSHOW'

export interface User {
  id: string
  email: string
  name: string
  phone: string
  role: UserRole
  auth_provider: AuthProvider
  created_at: string
}

export interface Product {
  id: string
  sku: string
  name: string
  type: ProductType
  price: number | null
  stock_quantity: number
  status: ProductStatus
  category_id: string
  category_name?: string
  thumbnail_url: string
  hover_image_url?: string
  images?: ProductImage[]
  description?: string
  designer_story?: string
}

export interface ProductImage {
  id: string
  product_id: string
  image_url: string
  display_order: number
  is_primary: boolean
}

export interface Category {
  id: string
  name: string
  slug: string
  parent_type: ProductType
}

export interface Order {
  id: string
  user_id: string | null
  guest_email: string | null
  guest_phone: string | null
  guest_name: string | null
  total_amount: number
  status: OrderStatus
  pg_transaction_id: string
  items: OrderItem[]
  created_at: string
}

export interface OrderItem {
  id: string
  order_id: string
  product_id: string
  product_name?: string
  quantity: number
  unit_price: number
}

export interface CartItem {
  product: Product
  quantity: number
}

export interface Reservation {
  id: string
  user_id: string | null
  guest_info: Record<string, string> | null
  reservation_type: ReservationType
  status: ReservationStatus
  expected_date: string
  dynamic_data: Record<string, unknown>
  created_at: string
}

export interface WaitlistEntry {
  id: string
  product_id: string
  user_id: string | null
  contact_method: string
  status: 'PENDING' | 'NOTIFIED'
}

// ============================================================
// Auth 관련 타입
// ============================================================

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  user: User
}

export interface RegisterRequest {
  email: string
  password: string
  name: string
  phone: string
}

// ============================================================
// 예약 폼 타입
// ============================================================

export interface ReservationRequest {
  type: ReservationType
  expected_date: string
  guest_info?: {
    name: string
    phone: string
    email: string
  }
  dynamic_data: Record<string, unknown>
}
