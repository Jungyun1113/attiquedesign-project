<template>
  <div class="admin-page">
    <h1 class="page-title">포트폴리오 이미지 관리</h1>

    <!-- 카테고리 탭 -->
    <div class="category-tabs">
      <button
        v-for="cat in CATEGORIES"
        :key="cat.value"
        class="cat-tab"
        :class="{ active: selectedCategory === cat.value }"
        @click="selectCategory(cat.value)"
      >
        {{ cat.label }}
      </button>
    </div>

    <div class="main-layout">
      <!-- 프로젝트 목록 -->
      <aside class="project-list">
        <div class="list-header">
          <span class="list-title">프로젝트</span>
          <button class="btn-new" @click="openCreateModal">+ 새 프로젝트</button>
        </div>
        <div v-if="loadingProjects" class="list-loading">불러오는 중...</div>
        <ul v-else class="project-items">
          <li
            v-for="p in portfolios"
            :key="p.id"
            class="project-item"
            :class="{ active: selectedPortfolio?.id === p.id }"
            @click="selectPortfolio(p)"
          >
            <span class="project-name">{{ p.title }}</span>
            <div class="item-actions">
              <span class="image-count">{{ p.images.length }}장</span>
              <button class="btn-icon" title="수정" @click.stop="openEditModal(p)">✏</button>
              <button class="btn-icon btn-icon-del" title="삭제" @click.stop="confirmDeletePortfolio(p)">✕</button>
            </div>
          </li>
          <li v-if="portfolios.length === 0" class="empty-item">프로젝트 없음</li>
        </ul>
      </aside>

      <!-- 이미지 관리 패널 -->
      <section class="image-panel">
        <template v-if="selectedPortfolio">
          <h2 class="panel-title">{{ selectedPortfolio.title }}</h2>

          <!-- 업로드 영역 -->
          <div
            class="drop-zone"
            :class="{ 'drag-over': isDragging }"
            @dragover.prevent="isDragging = true"
            @dragleave="isDragging = false"
            @drop.prevent="onDrop"
            @click="fileInput?.click()"
          >
            <input ref="fileInput" type="file" accept="image/*" multiple hidden @change="onFileChange" />
            <div v-if="pendingFiles.length === 0" class="drop-hint">
              <span class="drop-icon">↑</span>
              <p>이미지를 드래그하거나 클릭해서 선택</p>
              <p class="drop-sub">여러 장 선택 가능 · 순서대로 업로드됨</p>
            </div>
            <div v-else class="pending-preview">
              <div v-for="(f, i) in pendingFiles" :key="i" class="preview-item">
                <img :src="f.preview" :alt="f.file.name" />
                <span class="preview-order">{{ i + 1 }}</span>
                <button class="preview-remove" @click.stop="removePending(i)">✕</button>
              </div>
            </div>
          </div>

          <!-- 업로드 버튼 -->
          <div class="upload-actions">
            <button
              v-if="pendingFiles.length > 0"
              class="btn-upload"
              :disabled="uploading"
              @click="uploadImages"
            >
              <span v-if="uploading">
                <span class="spinner" /> 업로드 중 {{ uploadProgress }}/{{ pendingFiles.length }}
              </span>
              <span v-else>{{ pendingFiles.length }}장 업로드</span>
            </button>
            <p v-if="uploadMsg" :class="['upload-msg', uploadMsgType]">{{ uploadMsg }}</p>
          </div>

          <!-- 등록된 이미지 목록 (드래그앤드롭 순서 변경) -->
          <div class="registered-images">
            <div class="section-header">
              <h3 class="section-label">등록된 이미지 ({{ orderedImages.length }}장)</h3>
              <div class="order-actions">
                <span class="drag-hint">드래그해서 순서 변경</span>
                <button
                  v-if="orderChanged"
                  class="btn-save-order"
                  :disabled="savingOrder"
                  @click="saveOrder"
                >
                  {{ savingOrder ? '저장 중...' : '순서 저장' }}
                </button>
                <span v-if="orderSaveMsg" :class="['order-msg', orderSaveMsgType]">{{ orderSaveMsg }}</span>
              </div>
            </div>
            <div v-if="orderedImages.length === 0" class="no-images">등록된 이미지가 없습니다.</div>
            <div v-else class="image-grid">
              <div
                v-for="(img, idx) in orderedImages"
                :key="img.id"
                class="image-card"
                :class="{ dragging: dragIdx === idx }"
                draggable="true"
                @dragstart="onDragStart(idx)"
                @dragover.prevent="onDragOver(idx)"
                @dragend="onDragEnd"
              >
                <span v-if="idx === 0" class="main-badge">메인</span>
                <span class="order-badge">{{ idx + 1 }}</span>
                <img :src="img.image_url" :alt="`이미지 ${idx + 1}`" />
                <button class="btn-delete-img" @click="deleteImage(img.id)" title="삭제">✕</button>
              </div>
            </div>
          </div>
        </template>

        <div v-else class="panel-empty">
          왼쪽에서 프로젝트를 선택하세요.
        </div>
      </section>
    </div>

    <!-- 새 프로젝트 모달 -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal">
        <h2 class="modal-title">새 프로젝트 만들기</h2>
        <div class="field">
          <label>프로젝트 이름</label>
          <input v-model="newTitle" type="text" placeholder="예: 한남동 주거 프로젝트" />
        </div>
        <div class="field">
          <label>설명 (선택)</label>
          <textarea v-model="newDescription" rows="3" placeholder="프로젝트 설명"></textarea>
        </div>
        <p v-if="createError" class="error-msg">{{ createError }}</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showCreateModal = false">취소</button>
          <button class="btn-confirm" :disabled="creating" @click="createPortfolio">
            {{ creating ? '생성 중...' : '생성' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 프로젝트 수정 모달 -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal">
        <h2 class="modal-title">프로젝트 수정</h2>
        <div class="field">
          <label>카테고리</label>
          <select v-model="editCategory">
            <option v-for="cat in CATEGORIES" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
          </select>
        </div>
        <div class="field">
          <label>프로젝트 이름</label>
          <input v-model="editTitle" type="text" />
        </div>
        <div class="field">
          <label>설명 (선택)</label>
          <textarea v-model="editDescription" rows="3"></textarea>
        </div>
        <p v-if="editError" class="error-msg">{{ editError }}</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showEditModal = false">취소</button>
          <button class="btn-confirm" :disabled="editing" @click="patchPortfolio">
            {{ editing ? '저장 중...' : '저장' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'
import api from '@/services/api'

const CATEGORIES = [
  { value: 'residential', label: '주거' },
  { value: 'commercial', label: '상업' },
  { value: 'drama', label: '드라마' },
  { value: 'magazine', label: '매거진' },
]

interface PortfolioImage { id: string; image_url: string; display_order: number }
interface Portfolio { id: string; title: string; category: string; description: string | null; cover_image_url: string | null; images: PortfolioImage[] }

const selectedCategory = ref('residential')
const portfolios = ref<Portfolio[]>([])
const selectedPortfolio = ref<Portfolio | null>(null)
const loadingProjects = ref(false)

const fileInput = ref<HTMLInputElement | null>(null)
const pendingFiles = ref<{ file: File; preview: string }[]>([])
const isDragging = ref(false)

const uploading = ref(false)
const uploadProgress = ref(0)
const uploadMsg = ref('')
const uploadMsgType = ref<'success' | 'error'>('success')

// 드래그앤드롭 순서 변경
const orderedImages = ref<PortfolioImage[]>([])
const dragIdx = ref<number | null>(null)
const orderChanged = ref(false)
const savingOrder = ref(false)
const orderSaveMsg = ref('')
const orderSaveMsgType = ref<'success' | 'error'>('success')

watch(() => selectedPortfolio.value?.images, (imgs) => {
  orderedImages.value = imgs ? [...imgs] : []
  orderChanged.value = false
  orderSaveMsg.value = ''
}, { immediate: true })

function onDragStart(idx: number) {
  dragIdx.value = idx
}

function onDragOver(idx: number) {
  if (dragIdx.value === null || dragIdx.value === idx) return
  const imgs = [...orderedImages.value]
  const [moved] = imgs.splice(dragIdx.value, 1)
  imgs.splice(idx, 0, moved)
  orderedImages.value = imgs
  dragIdx.value = idx
  orderChanged.value = true
}

function onDragEnd() {
  dragIdx.value = null
}

async function saveOrder() {
  if (!selectedPortfolio.value) return
  savingOrder.value = true
  orderSaveMsg.value = ''
  try {
    const orders = orderedImages.value.map((img, i) => ({ id: img.id, display_order: i }))
    await api.post(`/portfolios/${selectedPortfolio.value.id}/reorder`, { orders })
    orderSaveMsg.value = '순서 저장 완료!'
    orderSaveMsgType.value = 'success'
    orderChanged.value = false
    await selectPortfolio(selectedPortfolio.value!)
  } catch {
    orderSaveMsg.value = '저장 실패'
    orderSaveMsgType.value = 'error'
  } finally {
    savingOrder.value = false
  }
}

// 생성 모달
const showCreateModal = ref(false)
const newTitle = ref('')
const newDescription = ref('')
const creating = ref(false)
const createError = ref('')

// 수정 모달
const showEditModal = ref(false)
const editingPortfolio = ref<Portfolio | null>(null)
const editTitle = ref('')
const editDescription = ref('')
const editCategory = ref('')
const editing = ref(false)
const editError = ref('')

async function loadPortfolios(category: string) {
  loadingProjects.value = true
  selectedPortfolio.value = null
  try {
    const { data } = await api.get('/portfolios', { params: { category, limit: 100 } })
    portfolios.value = data.data as Portfolio[]
  } finally {
    loadingProjects.value = false
  }
}

function selectCategory(cat: string) {
  selectedCategory.value = cat
  loadPortfolios(cat)
}

async function selectPortfolio(p: Portfolio) {
  const { data } = await api.get(`/portfolios/${p.id}`)
  selectedPortfolio.value = data.data as Portfolio
}

function onFileChange(e: Event) {
  const files = (e.target as HTMLInputElement).files
  if (files) addFiles(Array.from(files))
}

function onDrop(e: DragEvent) {
  isDragging.value = false
  if (e.dataTransfer?.files) addFiles(Array.from(e.dataTransfer.files))
}

function addFiles(files: File[]) {
  for (const file of files) {
    if (!file.type.startsWith('image/')) continue
    const preview = URL.createObjectURL(file)
    pendingFiles.value.push({ file, preview })
  }
}

function removePending(idx: number) {
  URL.revokeObjectURL(pendingFiles.value[idx].preview)
  pendingFiles.value.splice(idx, 1)
}

async function uploadImages() {
  if (!selectedPortfolio.value || pendingFiles.value.length === 0) return
  uploading.value = true
  uploadProgress.value = 0
  uploadMsg.value = ''

  const startOrder = selectedPortfolio.value.images.length

  try {
    for (let i = 0; i < pendingFiles.value.length; i++) {
      const { file } = pendingFiles.value[i]

      const uploadFileType = file.type || 'image/png'
      // 1) presign
      const { data: presignData } = await api.post('/uploads/presign', {
        filename: file.name,
        content_type: uploadFileType,
        target: 'portfolios',
      })
      const { upload_url, object_key } = presignData.data

      // 2) S3 PUT (file을 buffer로 변환하여 브라우저의 자동 Content-Type 삽입을 방지합니다.)
      const fileBuffer = await file.arrayBuffer()
      const uploadRes = await fetch(upload_url, {
        method: 'PUT',
        body: fileBuffer,
        headers: {
          'Content-Type': uploadFileType,
        },
      })
      if (!uploadRes.ok) throw new Error('S3 업로드 실패')

      // 3) DB 등록 — object_key를 저장하면 백엔드가 올바른 public URL로 변환
      await api.post(`/portfolios/${selectedPortfolio.value!.id}/images`, {
        image_url: object_key,
        display_order: startOrder + i,
      })

      uploadProgress.value = i + 1
    }

    uploadMsg.value = `${pendingFiles.value.length}장 업로드 완료!`
    uploadMsgType.value = 'success'
    pendingFiles.value.forEach(f => URL.revokeObjectURL(f.preview))
    pendingFiles.value = []

    await selectPortfolio(selectedPortfolio.value!)
  } catch {
    uploadMsg.value = '업로드 중 오류가 발생했습니다.'
    uploadMsgType.value = 'error'
  } finally {
    uploading.value = false
  }
}

async function deleteImage(imageId: string) {
  if (!selectedPortfolio.value) return
  if (!confirm('이미지를 삭제하시겠습니까?')) return
  try {
    await api.delete(`/portfolios/${selectedPortfolio.value.id}/images/${imageId}`)
    await selectPortfolio(selectedPortfolio.value!)
  } catch {
    alert('삭제 실패')
  }
}

function openCreateModal() {
  newTitle.value = ''
  newDescription.value = ''
  createError.value = ''
  showCreateModal.value = true
}

async function createPortfolio() {
  if (!newTitle.value.trim()) { createError.value = '이름을 입력해주세요.'; return }
  creating.value = true
  createError.value = ''
  try {
    await api.post('/portfolios', {
      category: selectedCategory.value,
      title: newTitle.value.trim(),
      description: newDescription.value.trim() || null,
    })
    showCreateModal.value = false
    await loadPortfolios(selectedCategory.value)
  } catch {
    createError.value = '생성 실패'
  } finally {
    creating.value = false
  }
}

function openEditModal(p: Portfolio) {
  editingPortfolio.value = p
  editTitle.value = p.title
  editDescription.value = p.description ?? ''
  editCategory.value = p.category
  editError.value = ''
  showEditModal.value = true
}

async function patchPortfolio() {
  if (!editingPortfolio.value) return
  if (!editTitle.value.trim()) { editError.value = '이름을 입력해주세요.'; return }
  editing.value = true
  editError.value = ''
  try {
    await api.patch(`/portfolios/${editingPortfolio.value.id}`, {
      title: editTitle.value.trim(),
      description: editDescription.value.trim() || null,
      category: editCategory.value,
    })
    showEditModal.value = false
    await loadPortfolios(selectedCategory.value)
    // 현재 선택된 포트폴리오였으면 다시 로드
    if (selectedPortfolio.value?.id === editingPortfolio.value.id) {
      const updated = portfolios.value.find(p => p.id === editingPortfolio.value!.id)
      if (updated) await selectPortfolio(updated)
    }
  } catch {
    editError.value = '수정 실패'
  } finally {
    editing.value = false
  }
}

async function confirmDeletePortfolio(p: Portfolio) {
  if (!confirm(`"${p.title}" 프로젝트를 삭제하시겠습니까?\n이미지도 모두 삭제됩니다.`)) return
  try {
    await api.delete(`/portfolios/${p.id}`)
    if (selectedPortfolio.value?.id === p.id) selectedPortfolio.value = null
    await loadPortfolios(selectedCategory.value)
  } catch {
    alert('삭제 실패')
  }
}

onMounted(() => loadPortfolios('residential'))
</script>

<style scoped>
.admin-page { max-width: 1100px; }
.page-title { font-size: 20px; font-weight: 600; margin: 0 0 24px; color: #111; }

.category-tabs { display: flex; gap: 8px; margin-bottom: 24px; }
.cat-tab { padding: 8px 18px; border: 1px solid #ddd; background: #fff; font-size: 13px; cursor: pointer; border-radius: 4px; color: #555; transition: all 0.15s; }
.cat-tab:hover { border-color: #888; color: #111; }
.cat-tab.active { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }

.main-layout { display: grid; grid-template-columns: 220px 1fr; gap: 24px; }

.project-list { background: #fff; border: 1px solid #e8e8e8; border-radius: 6px; overflow: hidden; }
.list-header { display: flex; align-items: center; justify-content: space-between; padding: 14px 16px; border-bottom: 1px solid #e8e8e8; }
.list-title { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #666; }
.btn-new { font-size: 11px; color: #555; background: none; border: 1px solid #ddd; padding: 4px 10px; cursor: pointer; border-radius: 4px; }
.btn-new:hover { background: #f5f5f5; }

.list-loading { padding: 20px 16px; font-size: 13px; color: #999; }
.project-items { list-style: none; padding: 0; margin: 0; }
.project-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 16px; cursor: pointer; border-bottom: 1px solid #f0f0f0; transition: background 0.12s; }
.project-item:last-child { border-bottom: none; }
.project-item:hover { background: #f8f8f8; }
.project-item.active { background: #f0f0f0; }
.project-name { font-size: 13px; color: #222; flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.item-actions { display: flex; align-items: center; gap: 4px; flex-shrink: 0; }
.image-count { font-size: 11px; color: #aaa; margin-right: 4px; }
.btn-icon { background: none; border: none; cursor: pointer; font-size: 11px; color: #888; padding: 2px 4px; border-radius: 3px; opacity: 0; transition: opacity 0.15s, background 0.12s; }
.btn-icon-del { color: #c0392b; }
.project-item:hover .btn-icon { opacity: 1; }
.btn-icon:hover { background: #eee; }
.btn-icon-del:hover { background: #fce8e6; }
.empty-item { padding: 16px; font-size: 13px; color: #bbb; text-align: center; }

.image-panel { background: #fff; border: 1px solid #e8e8e8; border-radius: 6px; padding: 24px; }
.panel-title { font-size: 16px; font-weight: 600; margin: 0 0 20px; }
.panel-empty { display: flex; align-items: center; justify-content: center; height: 200px; color: #bbb; font-size: 14px; }

.drop-zone { border: 2px dashed #ddd; border-radius: 6px; min-height: 160px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: border-color 0.2s, background 0.2s; padding: 16px; }
.drop-zone:hover, .drop-zone.drag-over { border-color: #888; background: #fafafa; }
.drop-hint { text-align: center; color: #aaa; }
.drop-icon { font-size: 28px; display: block; margin-bottom: 8px; }
.drop-hint p { margin: 4px 0; font-size: 13px; }
.drop-sub { font-size: 11px; color: #ccc; }

.pending-preview { display: flex; flex-wrap: wrap; gap: 8px; width: 100%; }
.preview-item { position: relative; width: 80px; height: 80px; }
.preview-item img { width: 100%; height: 100%; object-fit: cover; border-radius: 4px; }
.preview-order { position: absolute; top: 4px; left: 4px; background: rgba(0,0,0,0.6); color: #fff; font-size: 10px; width: 18px; height: 18px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.preview-remove { position: absolute; top: 2px; right: 2px; background: rgba(0,0,0,0.55); color: #fff; border: none; width: 18px; height: 18px; border-radius: 50%; cursor: pointer; font-size: 9px; display: flex; align-items: center; justify-content: center; padding: 0; }

.upload-actions { margin-top: 16px; display: flex; align-items: center; gap: 16px; }
.btn-upload { padding: 10px 24px; background: #1a1a1a; color: #fff; border: none; font-size: 13px; cursor: pointer; border-radius: 4px; display: flex; align-items: center; gap: 8px; }
.btn-upload:hover:not(:disabled) { background: #333; }
.btn-upload:disabled { opacity: 0.6; cursor: not-allowed; }
.upload-msg { font-size: 13px; margin: 0; }
.upload-msg.success { color: #27ae60; }
.upload-msg.error { color: #c0392b; }

.registered-images { margin-top: 32px; }
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; flex-wrap: wrap; gap: 8px; }
.section-label { font-size: 13px; font-weight: 600; color: #555; margin: 0; }
.order-actions { display: flex; align-items: center; gap: 10px; }
.drag-hint { font-size: 11px; color: #bbb; }
.btn-save-order { padding: 6px 16px; background: #1a1a1a; color: #fff; border: none; font-size: 12px; cursor: pointer; border-radius: 4px; }
.btn-save-order:disabled { opacity: 0.6; cursor: not-allowed; }
.order-msg { font-size: 12px; }
.order-msg.success { color: #27ae60; }
.order-msg.error { color: #c0392b; }
.no-images { font-size: 13px; color: #bbb; padding: 20px 0; }
.image-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 10px; }
.image-card { position: relative; aspect-ratio: 4/3; background: #f0f0f0; border-radius: 4px; overflow: hidden; cursor: grab; }
.image-card.dragging { opacity: 0.4; outline: 2px dashed #888; }
.image-card img { width: 100%; height: 100%; object-fit: cover; pointer-events: none; }
.main-badge { position: absolute; top: 6px; left: 6px; background: #953735; color: #fff; font-size: 10px; padding: 2px 6px; border-radius: 3px; z-index: 1; }
.order-badge { position: absolute; bottom: 6px; left: 6px; background: rgba(0,0,0,0.55); color: #fff; font-size: 10px; width: 18px; height: 18px; border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 1; }
.btn-delete-img { position: absolute; top: 4px; right: 4px; background: rgba(0,0,0,0.55); color: #fff; border: none; width: 22px; height: 22px; border-radius: 50%; cursor: pointer; font-size: 10px; display: flex; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.15s; }
.image-card:hover .btn-delete-img { opacity: 1; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; padding: 32px; width: 400px; border-radius: 8px; }
.modal-title { font-size: 16px; font-weight: 600; margin: 0 0 24px; }
.field { display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }
.field label { font-size: 12px; font-weight: 500; color: #444; }
.field input, .field textarea, .field select { padding: 10px 12px; border: 1px solid #ddd; font-size: 14px; outline: none; resize: vertical; font-family: inherit; border-radius: 3px; }
.field input:focus, .field textarea:focus, .field select:focus { border-color: #333; }
.error-msg { font-size: 12px; color: #c0392b; margin: 0 0 12px; }
.modal-actions { display: flex; gap: 8px; justify-content: flex-end; }
.btn-cancel { padding: 9px 20px; border: 1px solid #ddd; background: #fff; font-size: 13px; cursor: pointer; border-radius: 4px; }
.btn-confirm { padding: 9px 20px; background: #1a1a1a; color: #fff; border: none; font-size: 13px; cursor: pointer; border-radius: 4px; }
.btn-confirm:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.4); border-top-color: #fff; border-radius: 50%; animation: spin 0.7s linear infinite; vertical-align: middle; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
