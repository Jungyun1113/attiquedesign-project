# Frontend Dev Instructions

## Stack
Vue 3 (Composition API) + TypeScript + Pinia + Vue Router + Tailwind CSS + Vanilla CSS  
Path alias: `@/` → `src/`

---

## Project Structure
```
src/
├── assets/index.css       # CSS variables, Tailwind layers, global font imports
├── components/
│   ├── common/            # BaseButton, BaseInput, FormItem, ToastContainer
│   ├── domain/            # ProductCard
│   └── navigation/        # GlobalHeader
├── composables/           # useToast, usePagination, useActiveSection
├── data/portfolioData.ts  # Static portfolio data (not API-driven)
├── layouts/               # DefaultLayout, AdminLayout
├── router/index.ts        # All routes + guards
├── services/              # api.ts (axios), auth/product/reservation.service.ts
├── store/                 # auth.ts, cart.ts (Pinia)
├── types/api.d.ts         # All domain types/interfaces/enums
└── views/                 # Page components (lazy-loaded in router)
```

---

## Existing Reusables — Use Before Creating New

### Components
- **BaseButton** — variants: `solid | outline | ghost`; use `.btn-primary/.btn-outline/.btn-ghost` CSS classes for non-component usage
- **BaseInput** — `v-model` + `:error` prop for validation messages
- **FormItem** — label wrapper with required indicator; wraps BaseInput
- **ToastContainer** — mounted globally in App.vue via Teleport; do not duplicate
- **ProductCard** — hover image swap, badges, router-link; reuse for any product grid

### Composables
- **useToast** — `showSuccess() / showError() / showInfo()`; import anywhere, no store needed
- **usePagination** — `currentPage, totalPages, hasNext, hasPrev, nextPage(), prevPage(), goToPage()`; use for any list with pagination
- **useActiveSection** — IntersectionObserver for scroll-section tracking; use before writing new scroll listeners

### Services (`src/services/`)
- **api.ts** — pre-configured Axios: auto-attaches Bearer token, triggers `toast.showError()` on `success: false` responses; always import this instance, never create new axios instances
- **auth.service.ts** — `login(), register()`
- **product.service.ts** — `getProducts(params), getProductById(id), getCategories()`
- **reservation.service.ts** — `createReservation(payload)`
- All services have `USE_MOCK = true` flag; toggle to connect real API

### Store
- **useAuthStore** — `user, accessToken, isLoggedIn, isAdmin, login(), logout()`; tokens auto-persisted to localStorage
- **useCartStore** — `items, totalCount, totalPrice, addItem(), removeItem(), updateQuantity(), clearCart()`; auto-synced to `localStorage['attique_cart']`

### Types (`src/types/api.d.ts`)
All domain types live here: `User, Product, Category, Order, CartItem, Reservation` etc.  
Key enums: `UserRole, ProductType, ProductStatus, OrderStatus, ReservationType`  
Response wrappers: `ApiResponse<T>, ApiSuccessResponse<T>, ApiErrorResponse, PaginationMeta`

---

## Routing
- `/` → redirect `/selection?view=hero` (GNB active only on `?view=grid` for Selection)
- View modes via query param: `?view=hero | grid`
- `DefaultLayout` wraps all public routes; `AdminLayout` wraps `/admin/*`
- Lazy-load all views: `component: () => import('@/views/...')`
- Router auto scroll-to-top on navigate (except hash anchors)
- Admin guard: `meta: { requiresAdmin: true }` — check `router/index.ts`

---

## CSS / Styling

### Color Tokens (CSS variables in `assets/index.css`, also in `tailwind.config.js`)
| Token | Value | Usage |
|---|---|---|
| `--color-primary` | `#2B1D1B` | Main text |
| `--color-secondary` | `#6D6059` | Subtext |
| `--color-burgundy` | `#953735` | Brand accent, active, CTA |
| `--color-background` | `#F5F0E8` | Site-wide bg |
| `--color-border` | `#E8E2D7` | Dividers |

Use Tailwind color names (`text-brand`, `bg-background`) from tailwind config — see `tailwind.config.js`.

### Tailwind Utility Classes (defined in `@layer components`)
- `.container-page` — max-width 7xl + responsive horizontal padding
- `.section-gap` — `py-16 md:py-24 lg:py-32`
- `.btn-primary / .btn-outline / .btn-ghost / .btn-underline`

### Typography
| Role | Font |
|---|---|
| Brand logo | Raleway 200, letter-spacing 0.3em |
| EN headline | Playfair Display Italic |
| EN catchphrase | Cormorant Garamond |
| GNB labels | Montserrat uppercase |
| KO body | Pretendard |
| KO serif accent | Nanum Myeongjo |

### Component Scoped CSS Conventions
- State classes: `.is-scrolled`, `.is-active`
- BEM-ish naming: `.global-header > .header-inner > .gnb-link`
- Responsive: `@media (max-width: 768px)` in scoped styles

---

## Common Patterns

### Props
```ts
const props = withDefaults(defineProps<{ variant?: 'solid' | 'outline' }>(), { variant: 'solid' })
```

### Data Loading
```ts
const items = ref<Product[]>([])
onMounted(async () => {
  const res = await productService.getProducts(params)
  items.value = res.data
})
```

### Form Error State
```ts
const errors = reactive({ email: '', password: '' })
// display: <BaseInput :error="errors.email" />
```

### Store Access
```ts
const { user, isLoggedIn } = storeToRefs(useAuthStore())
```

### Image Loading
```html
<img :loading="idx === 0 ? 'eager' : 'lazy'" />
```

---

## Design Rules (from PRD/Design System)
- Overlapping editorial layout: `margin-top: -2rem ~ -4rem` on body text below hero
- Fullscreen sections: `100vh`, scroll-driven transitions `ease-in-out`
- Minimal commerce: no price exposure on hero/selection views; use "Enquire" / "View Detail"
- GlobalHeader: `position: sticky`, logo scale `0.65` on scroll (`scrollY > 20` → `.is-scrolled`)
- Selection hero slider: 4 slides, 2000ms interval, crossfade 0.9s, pause-on-hover
- Portfolio grid: asymmetric 4-col PC, 1–2 col mobile; image `aspect-ratio: 4/3`
- Contact page: split layout, left `aspect-ratio: 3/4` image, right typography

---

## Docs Reference
- PRD & UX spec: `docs/PRD.md`
- Design tokens & component hierarchy: `docs/3_design_system.md`
- API contracts: `docs/2_api_spec.md`
