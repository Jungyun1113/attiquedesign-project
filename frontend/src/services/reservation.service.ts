// ============================================================
// Reservation Service — 예약 API
// ============================================================
// import api from './api'
import type { ReservationRequest } from '@/types/api.d'

const USE_MOCK = true

export const reservationService = {
  async createReservation(payload: ReservationRequest) {
    if (USE_MOCK) {
      return new Promise((resolve) =>
        setTimeout(() => resolve({ success: true, data: { id: 'res-mock-' + Date.now() } }), 600),
      )
    }
    // const { data } = await api.post('/reservations', payload)
    // return data
    throw new Error('Real API not implemented')
  },
}
