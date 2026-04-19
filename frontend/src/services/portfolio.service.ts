import api from './api'

export interface PortfolioImage {
  id: string
  image_url: string
  display_order: number
}

export interface Portfolio {
  id: string
  category: string
  title: string
  description: string | null
  cover_image_url: string | null
  images: PortfolioImage[]
}

export interface PortfolioCategory {
  id: string
  name: string
  description: string
  portfolios: Portfolio[]
}

const CATEGORY_NAMES: Record<string, string> = {
  residential: '주거',
  commercial: '상업',
  drama: '드라마',
  magazine: '매거진',
}

const CATEGORY_DESCRIPTIONS: Record<string, string> = {
  residential: '클래식과 모던, 색과 소재의 균형 속에서 완성한 주거 공간.',
  commercial: '브랜드의 성격을 공간으로 풀어낸 아띠끄의 상업 프로젝트.',
  drama: '도깨비, 상속자들, 괜찮아 사랑이야.\n극 중 인물이 살아 숨쉬는 공간을 스타일링해온 아띠끄의 작업.',
  magazine: '메종, 까사리빙, 리빙센스와 함께해온 아띠끄의 리빙 스타일링 아카이브.',
}

export const portfolioService = {
  async getPortfolios(category?: string): Promise<Portfolio[]> {
    const params: Record<string, unknown> = { limit: 100 }
    if (category) params.category = category
    const { data } = await api.get('/portfolios', { params })
    return data.data as Portfolio[]
  },

  async getPortfolioById(id: string): Promise<Portfolio> {
    const { data } = await api.get(`/portfolios/${id}`)
    return data.data as Portfolio
  },

  async getGroupedByCategory(): Promise<PortfolioCategory[]> {
    const portfolios = await portfolioService.getPortfolios()
    const map = new Map<string, Portfolio[]>()
    for (const p of portfolios) {
      if (!map.has(p.category)) map.set(p.category, [])
      map.get(p.category)!.push(p)
    }

    const order = ['residential', 'commercial', 'drama', 'magazine']
    
    return Array.from(map.entries())
      .map(([cat, items]) => {
        const key = cat.toLowerCase().replace(/\s+/g, '-')
        return {
          id: key,
          name: CATEGORY_NAMES[key] ?? cat,
          description: CATEGORY_DESCRIPTIONS[key] ?? '',
          portfolios: items,
        }
      })
      .sort((a, b) => order.indexOf(a.id) - order.indexOf(b.id))
  },
}
