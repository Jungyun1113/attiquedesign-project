<template>
  <div class="admin-page">
    <h1 class="page-title">상품 관리</h1>

    <div class="main-layout">
      <!-- 상품 목록 -->
      <aside class="project-list">
        <div class="list-header">
          <span class="list-title">상품</span>
          <button class="btn-new" @click="openCreateModal">+ 새 상품</button>
        </div>
        <div v-if="loading" class="list-loading">불러오는 중...</div>
        <ul v-else class="project-items">
          <li
            v-for="p in products"
            :key="p.id"
            class="project-item"
            :class="{ active: selected?.id === p.id }"
            @click="selectProduct(p)"
          >
            <div class="item-thumb">
              <img v-if="p.thumbnail_url" :src="p.thumbnail_url" />
              <span v-else class="no-thumb">📷</span>
            </div>
            <div class="item-info">
              <span class="project-name">{{ p.name }}</span>
              <span class="project-sub">{{ p.sku }} · {{ p.category }}</span>
            </div>
            <div class="item-actions">
              <span class="status-badge" :class="p.status.toLowerCase()">{{ statusLabel(p.status) }}</span>
              <button class="btn-icon btn-icon-del" @click.stop="deleteProduct(p.id)" title="삭제">🗑</button>
            </div>
          </li>
        </ul>
      </aside>

      <!-- 상품 상세 -->
      <section class="detail-panel">
        <template v-if="selected">
          <div class="detail-header">
            <h2 class="detail-title">{{ selected.name }}</h2>
            <button class="btn-edit" @click="openEditModal">수정</button>
          </div>

          <div class="detail-meta">
            <div class="meta-item"><span class="meta-label">SKU</span><span>{{ selected.sku }}</span></div>
            <div class="meta-item"><span class="meta-label">카테고리</span><span>{{ selected.category }}</span></div>
            <div class="meta-item"><span class="meta-label">가격</span><span>{{ selected.price ? Number(selected.price).toLocaleString() + '원' : '가격 문의' }}</span></div>
            <div class="meta-item"><span class="meta-label">재고</span><span>{{ selected.stock_quantity }}</span></div>
            <div class="meta-item"><span class="meta-label">상태</span><span class="status-badge" :class="selected.status.toLowerCase()">{{ statusLabel(selected.status) }}</span></div>
          </div>

          <!-- 썸네일 -->
          <div class="thumbnail-section">
            <h3 class="section-label">썸네일</h3>
            <div class="thumbnail-wrap">
              <img v-if="selected.thumbnail_url" :src="selected.thumbnail_url" class="thumb-preview" />
              <div v-else class="thumb-placeholder">썸네일 없음</div>
            </div>
            <div class="thumb-upload">
              <input type="file" ref="thumbInput" accept="image/*" @change="uploadThumbnail" style="display:none" />
              <button class="btn-upload-thumb" @click="($refs.thumbInput as HTMLInputElement)?.click()">
                {{ selected.thumbnail_url ? '썸네일 변경' : '썸네일 업로드' }}
              </button>
            </div>
          </div>
        </template>

        <div v-else class="panel-empty">
          왼쪽에서 상품을 선택하세요.
        </div>
      </section>
    </div>

    <!-- 생성/수정 모달 -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h2 class="modal-title">{{ modalMode === 'create' ? '새 상품 등록' : '상품 수정' }}</h2>
        <div class="field"><label>SKU *</label><input v-model="form.sku" :disabled="modalMode === 'edit'" /></div>
        <div class="field"><label>상품명 *</label><input v-model="form.name" /></div>
        <div class="field"><label>카테고리 *</label><input v-model="form.category" placeholder="예: furniture, lighting, decor" /></div>
        <div class="field"><label>가격 (원)</label><input v-model.number="form.price" type="number" placeholder="비워두면 '가격 문의'로 표시" /></div>
        <div class="field"><label>재고 수량</label><input v-model.number="form.stock_quantity" type="number" /></div>
        <div class="field">
          <label>상태</label>
          <select v-model="form.status">
            <option value="ACTIVE">활성</option>
            <option value="HIDDEN">숨김</option>
            <option value="SOLDOUT">품절</option>
          </select>
        </div>
        <p v-if="formError" class="error-msg">{{ formError }}</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showModal = false">취소</button>
          <button class="btn-confirm" @click="saveProduct" :disabled="saving">
            <span v-if="saving" class="spinner"></span>
            {{ saving ? '' : (modalMode === 'create' ? '등록' : '저장') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import api from '@/services/api'

interface Product {
  id: string; sku: string; name: string; category: string
  price: number | null; stock_quantity: number; status: string
  thumbnail_url: string | null; images: { id: string; image_url: string; display_order: number; is_primary: boolean }[]
}

const products = ref<Product[]>([])
const selected = ref<Product | null>(null)
const loading = ref(true)

const showModal = ref(false)
const modalMode = ref<'create' | 'edit'>('create')
const saving = ref(false)
const formError = ref('')
const form = ref({ sku: '', name: '', category: '', price: null as number | null, stock_quantity: 0, status: 'ACTIVE' })

function statusLabel(status: string) {
  return { ACTIVE: '활성', HIDDEN: '숨김', SOLDOUT: '품절' }[status] ?? status
}

async function loadProducts() {
  loading.value = true
  try {
    const { data } = await api.get('/products', { params: { limit: 100 } })
    products.value = data.data ?? []
  } catch { products.value = [] }
  finally { loading.value = false }
}

async function selectProduct(p: Product) {
  try {
    const { data } = await api.get(`/products/${p.id}`)
    selected.value = data.data
  } catch {
    selected.value = p
  }
}

function openCreateModal() {
  modalMode.value = 'create'
  form.value = { sku: '', name: '', category: '', price: null, stock_quantity: 0, status: 'ACTIVE' }
  formError.value = ''
  showModal.value = true
}

function openEditModal() {
  if (!selected.value) return
  modalMode.value = 'edit'
  form.value = {
    sku: selected.value.sku,
    name: selected.value.name,
    category: selected.value.category,
    price: selected.value.price,
    stock_quantity: selected.value.stock_quantity,
    status: selected.value.status,
  }
  formError.value = ''
  showModal.value = true
}

async function saveProduct() {
  if (!form.value.sku || !form.value.name || !form.value.category) {
    formError.value = 'SKU, 상품명, 카테고리는 필수입니다.'
    return
  }
  saving.value = true
  formError.value = ''
  try {
    if (modalMode.value === 'create') {
      await api.post('/products', form.value)
    } else if (selected.value) {
      await api.patch(`/products/${selected.value.id}`, {
        name: form.value.name,
        category: form.value.category,
        price: form.value.price,
        stock_quantity: form.value.stock_quantity,
        status: form.value.status,
      })
    }
    showModal.value = false
    await loadProducts()
    if (modalMode.value === 'edit' && selected.value) {
      await selectProduct(selected.value)
    }
  } catch {
    formError.value = '저장 중 오류가 발생했습니다.'
  } finally {
    saving.value = false
  }
}

async function deleteProduct(id: string) {
  if (!confirm('이 상품을 삭제하시겠습니까?')) return
  try {
    await api.delete(`/products/${id}`)
    if (selected.value?.id === id) selected.value = null
    await loadProducts()
  } catch { alert('삭제 실패') }
}

async function uploadThumbnail(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file || !selected.value) return

  try {
    const uploadFileType = file.type || 'image/png'
    // 1) presign
    const { data: presignData } = await api.post('/uploads/presign', {
      filename: file.name,
      content_type: uploadFileType,
      target: 'products',
    })
    const { upload_url, object_key } = presignData.data

    // 2) S3 PUT (buffer로 변환하여 자동 헤더 추가 방지)
    const fileBuffer = await file.arrayBuffer()
    const uploadRes = await fetch(upload_url, {
      method: 'PUT',
      body: fileBuffer,
    })
    if (!uploadRes.ok) throw new Error('S3 업로드 실패')

    // 3) 상품 thumbnail_url 업데이트
    await api.patch(`/products/${selected.value.id}`, { thumbnail_url: object_key })
    await selectProduct(selected.value)
    await loadProducts()
  } catch {
    alert('썸네일 업로드 실패')
  }
}

onMounted(loadProducts)
</script>

<style scoped>
.admin-page { padding: 24px 32px; font-family: 'Pretendard', -apple-system, sans-serif; }
.page-title { font-size: 18px; font-weight: 600; margin: 0 0 20px; color: #111; }

.main-layout { display: flex; gap: 24px; min-height: calc(100vh - 140px); }
.project-list { width: 320px; flex-shrink: 0; background: #fff; border-radius: 6px; border: 1px solid #eee; overflow: hidden; }
.detail-panel { flex: 1; background: #fff; border-radius: 6px; border: 1px solid #eee; padding: 24px; overflow-y: auto; }

.list-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid #eee; }
.list-title { font-size: 13px; font-weight: 600; color: #333; }
.btn-new { font-size: 11px; color: #555; background: none; border: 1px solid #ddd; padding: 4px 10px; cursor: pointer; border-radius: 4px; }
.btn-new:hover { background: #f5f5f5; }

.list-loading { padding: 20px 16px; font-size: 13px; color: #999; }
.project-items { list-style: none; padding: 0; margin: 0; }
.project-item { display: flex; align-items: center; gap: 10px; padding: 10px 16px; cursor: pointer; border-bottom: 1px solid #f0f0f0; transition: background 0.12s; }
.project-item:hover { background: #f8f8f8; }
.project-item.active { background: #f0f0f0; }
.item-thumb { width: 36px; height: 36px; flex-shrink: 0; border-radius: 4px; overflow: hidden; background: #f0f0f0; display: flex; align-items: center; justify-content: center; }
.item-thumb img { width: 100%; height: 100%; object-fit: cover; }
.no-thumb { font-size: 14px; color: #ccc; }
.item-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.project-name { font-size: 13px; color: #222; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.project-sub { font-size: 11px; color: #aaa; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.item-actions { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.btn-icon { background: none; border: none; cursor: pointer; font-size: 11px; color: #888; padding: 2px 4px; border-radius: 3px; opacity: 0; transition: opacity 0.15s; }
.btn-icon-del { color: #c0392b; }
.project-item:hover .btn-icon { opacity: 1; }

.status-badge { font-size: 10px; padding: 2px 6px; border-radius: 3px; font-weight: 500; }
.status-badge.active { color: #27ae60; background: #e8f5e9; }
.status-badge.hidden { color: #888; background: #eee; }
.status-badge.soldout { color: #c0392b; background: #fce8e6; }

.detail-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.detail-title { font-size: 18px; font-weight: 500; color: #111; margin: 0; }
.btn-edit { font-size: 11px; color: #555; background: none; border: 1px solid #ddd; padding: 4px 12px; cursor: pointer; border-radius: 4px; }
.btn-edit:hover { background: #f5f5f5; }

.detail-meta { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 24px; }
.meta-item { display: flex; flex-direction: column; gap: 4px; }
.meta-label { font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 0.05em; }

.section-label { font-size: 13px; font-weight: 600; color: #333; margin: 0 0 12px; }
.thumbnail-section { margin-top: 24px; }
.thumbnail-wrap { width: 200px; height: 200px; background: #f5f5f5; border: 1px solid #eee; border-radius: 4px; overflow: hidden; margin-bottom: 8px; }
.thumb-preview { width: 100%; height: 100%; object-fit: cover; }
.thumb-placeholder { display: flex; align-items: center; justify-content: center; height: 100%; font-size: 13px; color: #ccc; }
.btn-upload-thumb { font-size: 11px; color: #555; background: none; border: 1px solid #ddd; padding: 4px 12px; cursor: pointer; border-radius: 4px; }
.btn-upload-thumb:hover { background: #f5f5f5; }

.panel-empty { display: flex; align-items: center; justify-content: center; height: 200px; font-size: 14px; color: #aaa; }

/* 모달 */
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.35); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: #fff; border-radius: 8px; padding: 28px 32px; width: 420px; box-shadow: 0 8px 32px rgba(0,0,0,0.12); }
.modal-title { font-size: 16px; font-weight: 600; margin: 0 0 20px; }
.field { display: flex; flex-direction: column; gap: 4px; margin-bottom: 14px; }
.field label { font-size: 12px; color: #555; }
.field input, .field select { padding: 10px 12px; border: 1px solid #ddd; font-size: 14px; outline: none; border-radius: 3px; font-family: inherit; }
.field input:focus, .field select:focus { border-color: #333; }
.error-msg { font-size: 12px; color: #c0392b; margin: 0 0 12px; }
.modal-actions { display: flex; gap: 8px; justify-content: flex-end; }
.btn-cancel { padding: 9px 20px; border: 1px solid #ddd; background: #fff; font-size: 13px; cursor: pointer; border-radius: 4px; }
.btn-confirm { padding: 9px 20px; background: #1a1a1a; color: #fff; border: none; font-size: 13px; cursor: pointer; border-radius: 4px; }
.btn-confirm:disabled { opacity: 0.6; cursor: not-allowed; }
.spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.4); border-top-color: #fff; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
