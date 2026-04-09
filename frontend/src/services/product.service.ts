// ============================================================
// Product Service — 상품 API
// Mock 모드: MOCK_PRODUCTS를 반환
// ============================================================
// import api from './api'
import type { Product, ApiSuccessResponse, PaginationMeta } from '@/types/api.d'
import { MOCK_PRODUCTS, MOCK_CATEGORIES } from '@/mocks/data'

const USE_MOCK = true // TODO: 실제 API 연동 시 false로 변경

export const productService = {
  async getProducts(params?: {
    page?: number
    limit?: number
    type?: string
    category_id?: string
    sort?: string
  }): Promise<ApiSuccessResponse<Product[]>> {
    if (USE_MOCK) {
      let filtered = [...MOCK_PRODUCTS]
      if (params?.type) filtered = filtered.filter((p) => p.type === params.type)
      if (params?.category_id) filtered = filtered.filter((p) => p.category_id === params.category_id)
      if (params?.sort === 'price_asc') filtered.sort((a, b) => (a.price ?? Infinity) - (b.price ?? Infinity))
      if (params?.sort === 'price_desc') filtered.sort((a, b) => (b.price ?? 0) - (a.price ?? 0))

      const page = params?.page ?? 1
      const limit = params?.limit ?? 12
      const start = (page - 1) * limit
      const paginated = filtered.slice(start, start + limit)
      const meta: PaginationMeta = {
        page,
        size: limit,
        total_pages: Math.ceil(filtered.length / limit),
        total_count: filtered.length,
      }
      return new Promise((resolve) =>
        setTimeout(() => resolve({ success: true, data: paginated, meta }), 300),
      )
    }
    // const { data } = await api.get('/products', { params })
    // return data as ApiSuccessResponse<Product[]>
    throw new Error('Real API not implemented')
  },

  async getProductById(id: string): Promise<Product> {
    if (USE_MOCK) {
      const product = MOCK_PRODUCTS.find((p) => p.id === id)
      if (!product) throw new Error('Product not found')
      return new Promise((resolve) => setTimeout(() => resolve(product), 200))
    }
    // const { data } = await api.get(`/products/${id}`)
    // return data.data as Product
    throw new Error('Real API not implemented')
  },

  getCategories() {
    return MOCK_CATEGORIES
  },
}
