import api from './api'
import type { Product, ApiSuccessResponse, PaginationMeta } from '@/types/api.d'

const STATIC_CATEGORIES = [
  { id: 'Sofa', name: 'Sofa' },
  { id: 'Chair / Stool', name: 'Chair / Stool' },
  { id: 'Table / Desk', name: 'Table / Desk' },
  { id: 'Cabinet / Storage', name: 'Cabinet / Storage' },
  { id: 'Bed', name: 'Bed' },
  { id: 'Lighting', name: 'Lighting' },
  { id: 'Fabric', name: 'Fabric' },
  { id: 'Object / Decor', name: 'Object / Decor' },
  { id: 'Kitchen / Dining', name: 'Kitchen / Dining' },
]

function mapProduct(item: Record<string, unknown>): Product {
  return {
    id: item.id as string,
    sku: item.sku as string,
    name: item.name as string,
    price: item.price as number | null,
    stock_quantity: item.stock_quantity as number,
    status: item.status as Product['status'],
    thumbnail_url: item.thumbnail_url as string,
    type: item.type as Product['type'],
    hover_image_url: item.hover_image_url as string | undefined,
    images: item.images as Product['images'],
    description: item.description as string | undefined,
    designer_story: item.designer_story as string | undefined,
    category_id: (item.category_id ?? item.category) as string ?? '',
    category_name: (item.category_name ?? item.category) as string ?? '',
  }
}

export const productService = {
  async getProducts(params?: {
    page?: number
    limit?: number
    category?: string
    sort?: string
  }): Promise<ApiSuccessResponse<Product[]>> {
    const backendParams: Record<string, unknown> = {
      page: params?.page ?? 1,
      limit: params?.limit ?? 20,
    }
    if (params?.category) backendParams.category = params.category
    if (params?.sort === 'price_asc') {
      backendParams.sort = 'price'
      backendParams.order = 'asc'
    } else if (params?.sort === 'price_desc') {
      backendParams.sort = 'price'
      backendParams.order = 'desc'
    } else {
      backendParams.sort = 'created_at'
      backendParams.order = 'desc'
    }

    const { data } = await api.get('/products', { params: backendParams })
    const meta: PaginationMeta = data.meta
    const products: Product[] = (data.data as Record<string, unknown>[]).map(mapProduct)
    return { success: true, data: products, meta }
  },

  async getProductById(id: string): Promise<Product> {
    const { data } = await api.get(`/products/${id}`)
    return mapProduct(data.data as Record<string, unknown>)
  },

  getCategories() {
    return STATIC_CATEGORIES
  },
}
