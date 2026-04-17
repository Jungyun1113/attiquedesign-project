export interface Project {
  id: string
  slug: string
  caseNumber: string
  title: string
  description: string
  year: string
  beforeImage?: string
  images: string[]
  furnitureTags?: string[]
}

export interface PortfolioCategory {
  id: string
  name: string
  description: string
  projects: Project[]
}

export const portfolioData: PortfolioCategory[] = [
  {
    id: 'residential',
    name: '주거',
    description: '클래식과 모던, 색과 소재의 균형 속에서 완성한 주거 공간.',
    projects: [
      {
        id: 'R-001',
        slug: 'hannam-townhouse-68p',
        caseNumber: '#R-001',
        title: 'Hannam Townhouse 68P',
        description: '다크 월넛의 깊이감과 버건디 텍스타일이 조화를 이루는 고품격 주거 공간 스타일링.',
        year: '2025',
        beforeImage: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1400&q=85',
        images: [
          'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1400&q=85',
          'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1400&q=85',
          'https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?w=1400&q=85'
        ],
        furnitureTags: ['Minotti Morgan Sofa', 'B&B Italia Armchair', 'Flexform Dining Table']
      },
      {
        id: 'R-002',
        slug: 'apgujeong-penthouse-42p',
        caseNumber: '#R-002',
        title: 'Apgujeong Penthouse 42P',
        description: '미니멀한 직선미와 따뜻한 톤의 머티리얼이 만나 완성된 도심 속 안식처.',
        year: '2024',
        images: [
          'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1400&q=85',
          'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1400&q=85'
        ],
        furnitureTags: ['Cassina LC4 Chaise', 'Knoll Florence Sofa']
      }
    ]
  },
  {
    id: 'commercial',
    name: '상업',
    description: '브랜드의 성격을 공간으로 풀어낸 아띠끄의 상업 프로젝트.',
    projects: [
      {
        id: 'C-001',
        slug: 'seongsu-creative-lounge',
        caseNumber: '#C-001',
        title: 'Seongsu Creative Lounge',
        description: '자유로운 협업이 가능한 개방형 레이아웃과 감도 높은 퍼니처 셀렉션.',
        year: '2025',
        images: [
          'https://images.unsplash.com/photo-1497366216548-37526070297c?w=1400&q=85',
          'https://images.unsplash.com/photo-1497366811353-6870744d04b2?w=1400&q=85'
        ],
        furnitureTags: ['Vitra Eames DSW', 'HAY About A Chair', 'Muuto Stacked Shelf']
      },
      {
        id: 'C-002',
        slug: 'hannam-boutique-hotel',
        caseNumber: '#C-002',
        title: 'Hannam Boutique Hotel',
        description: '클래식한 몰딩 디테일과 현대적인 조명이 어우러진 프리미엄 부티크 로비.',
        year: '2024',
        images: [
          'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1400&q=85',
          'https://images.unsplash.com/photo-1582719478237-c26ad0d60c41?w=1400&q=85'
        ],
        furnitureTags: ['Poltrona Frau Vanity Fair', 'Giorgetti Nuvola Sofa']
      }
    ]
  },
  {
    id: 'drama',
    name: '방송',
    description: '도깨비, 상속자들, 시카고 타자기.\n극 중 인물이 살아 숨쉬는 공간을 스타일링해온 아띠끄의 작업.',
    projects: [
      {
        id: 'D-001',
        slug: 'luxury-villa-set',
        caseNumber: '#D-001',
        title: 'Luxury Villa Set',
        description: '흥행 드라마 속 주인공의 취향을 반영한 런웨이 스타일의 럭셔리 빌라 세트 연출.',
        year: '2024',
        images: [
          'https://images.unsplash.com/photo-1600121848594-d8644e57abab?w=1400&q=85',
          'https://images.unsplash.com/photo-1600566752355-33792cb0f8cb?w=1400&q=85'
        ],
        furnitureTags: ['Minotti Lawson Sofa', 'Flexform Romeo Lamp']
      }
    ]
  },
  {
    id: 'magazine',
    name: '매거진',
    description: '메종, 까사리빙, 리빙센스와 함께해온 아띠끄의 리빙 스타일링 아카이브.',
    projects: [
      {
        id: 'M-001',
        slug: 'editorial-highlight',
        caseNumber: '#M-001',
        title: 'Editorial Highlight',
        description: 'Cereal Magazine 및 Kinfolk에서 주목한 아띠끄의 에디토리얼 레이아웃.',
        year: '2023',
        images: [
          'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=1400&q=85',
          'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=1400&q=85'
        ]
      }
    ]
  }
]

/** slug 또는 id로 프로젝트를 찾아 반환 */
export function findProjectBySlug(slugOrId: string): Project | undefined {
  for (const category of portfolioData) {
    const project = category.projects.find(
      p => p.slug === slugOrId || p.id === slugOrId
    )
    if (project) return project
  }
  return undefined
}
