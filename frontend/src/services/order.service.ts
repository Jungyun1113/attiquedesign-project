import api from './api'
import type { Order, ApiSuccessResponse, PaginationMeta } from '@/types/api.d'

export const orderService = {
  async getMyOrders(params?: { page?: number; limit?: number }): Promise<ApiSuccessResponse<Order[]>> {
    const { data } = await api.get('/orders/me', { params: { page: params?.page ?? 1, limit: params?.limit ?? 20 } })
    const meta: PaginationMeta = data.meta
    return { success: true, data: data.data as Order[], meta }
  },

  async getOrderById(id: string): Promise<Order> {
    const { data } = await api.get(`/orders/${id}`)
    return data.data as Order
  },
}
