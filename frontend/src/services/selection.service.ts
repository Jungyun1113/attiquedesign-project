import api from './api'

export interface SelectionImage {
  id: string
  image_url: string
  display_order: number
}

export interface SelectionProduct {
  id: string
  product_id: string
  display_order: number
  name?: string
  thumbnail_url?: string
  price?: number | null
  status?: string
}

export interface Selection {
  id: string
  title: string
  subtitle?: string
  description?: string
  images: SelectionImage[]
  products: SelectionProduct[]
}

export const selectionService = {
  async getSelections(params?: { page?: number; limit?: number }): Promise<Selection[]> {
    const { data } = await api.get('/selections', { params: { page: params?.page ?? 1, limit: params?.limit ?? 50 } })
    return data.data as Selection[]
  },

  async getSelectionById(id: string): Promise<Selection> {
    const { data } = await api.get(`/selections/${id}`)
    return data.data as Selection
  },
}
