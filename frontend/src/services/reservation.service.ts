import api from './api'
import type { ReservationRequest } from '@/types/api.d'

export const reservationService = {
  async createReservation(payload: ReservationRequest) {
    const { data } = await api.post('/reservations', {
      reservation_type: payload.type,
      expected_date: payload.expected_date,
      guest_info: payload.guest_info,
      dynamic_data: payload.dynamic_data,
    })
    return data
  },
}
