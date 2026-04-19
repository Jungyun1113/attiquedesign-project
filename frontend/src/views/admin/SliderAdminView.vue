<template>
  <div class="admin-page">
    <h1 class="page-title">메인 슬라이더 관리</h1>
    <p class="page-desc">이곳에서 추가/삭제한 이미지가 메인 페이지 첫 화면 슬라이더에 즉시 반영됩니다.</p>

    <div class="main-layout">
      <!-- 슬라이더 항목 목록 -->
      <aside class="project-list">
        <div class="list-header">
          <span class="list-title">슬라이더 항목</span>
          <button class="btn-new" @click="openCreateModal">+ 새 항목</button>
        </div>
        <div v-if="loadingList" class="list-loading">불러오는 중...</div>
        <ul v-else class="project-items">
          <li
            v-for="s in sliders"
            :key="s.id"
            class="project-item"
            :class="{ active: selected?.id === s.id }"
            @click="selectSlider(s)"
          >
            <div class="item-info">
              <span class="project-name">{{ s.title }}</span>
              <span v-if="s.subtitle" class="project-sub">{{ s.subtitle }}</span>
            </div>
            <div class="item-actions">
              <span class="image-count">{{ s.images.length }}장</span>
              <button class="btn-icon" title="수정" @click.stop="openEditModal(s)">✏</button>
              <button class="btn-icon btn-icon-del" title="삭제" @click.stop="confirmDelete(s)">✕</button>
            </div>
          </li>
          <li v-if="sliders.length === 0" class="empty-item">슬라이더 항목 없음</li>
        </ul>
      </aside>

      <!-- 이미지 관리 패널 -->
      <section class="image-panel">
        <template v-if="selected">
          <div class="panel-header">
            <h2 class="panel-title">{{ selected.title }}</h2>
            <p v-if="selected.subtitle" class="panel-sub">{{ selected.subtitle }}</p>
          </div>

          <!-- 업로드 결과 메시지 (최상단 배치) -->
          <Transition name="fade">
            <div v-if="uploadResultMessage" :class="['upload-result-box', uploadResultType]">
              <span class="result-icon">{{ uploadResultType === 'success' ? '✓' : '✕' }}</span>
              <span class="result-text">{{ uploadResultMessage }}</span>
              <button class="btn-msg-close" @click="uploadResultMessage = ''">✕</button>
            </div>
          </Transition>

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
              <span v-if="uploading"><span class="spinner" /> 업로드 중 {{ uploadProgress }}/{{ pendingFiles.length }}</span>
              <span v-else>{{ pendingFiles.length }}장 업로드</span>
            </button>
          </div>

          <!-- 등록된 이미지 -->
          <div class="registered-images">
            <h3 class="section-label">등록된 슬라이드 이미지 ({{ selected.images.length }}장)</h3>
            <div v-if="selected.images.length === 0" class="no-images">등록된 이미지가 없습니다.</div>
            <div v-else class="image-grid">
              <div
                v-for="(img, idx) in selected.images"
                :key="img.id"
                class="image-card"
              >
                <span class="order-badge">{{ idx + 1 }}</span>
                <img :src="img.image_url" :alt="`슬라이드 ${idx + 1}`" />
                <button class="btn-delete-img" @click="deleteImage(img.id)" title="삭제">✕</button>
              </div>
            </div>
          </div>

        </template>

        <div v-else class="panel-empty">
          왼쪽에서 슬라이더 항목을 선택하세요.
        </div>
      </section>
    </div>

    <!-- 새 항목 생성 모달 -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal">
        <h2 class="modal-title">새 슬라이더 항목 만들기</h2>
        <div class="field">
          <label>제목 <span class="required">*</span></label>
          <input v-model="newTitle" type="text" placeholder="예: 2024 Summer Collection" />
        </div>
        <div class="field">
          <label>부제목 (선택)</label>
          <input v-model="newSubtitle" type="text" placeholder="예: 여름 리빙 컬렉션" />
        </div>
        <p v-if="createError" class="error-msg">{{ createError }}</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showCreateModal = false">취소</button>
          <button class="btn-confirm" :disabled="creating" @click="createSlider">
            {{ creating ? '생성 중...' : '생성' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 항목 수정 모달 -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal">
        <h2 class="modal-title">슬라이더 항목 수정</h2>
        <div class="field">
          <label>제목 <span class="required">*</span></label>
          <input v-model="editTitle" type="text" />
        </div>
        <div class="field">
          <label>부제목 (선택)</label>
          <input v-model="editSubtitle" type="text" />
        </div>
        <p v-if="editError" class="error-msg">{{ editError }}</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showEditModal = false">취소</button>
          <button class="btn-confirm" :disabled="editing" @click="patchSlider">
            {{ editing ? '저장 중...' : '저장' }}
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

interface SliderImage { id: string; image_url: string; display_order: number }
interface Slider { id: string; title: string; subtitle?: string; images: SliderImage[] }

const sliders = ref<Slider[]>([])
const selected = ref<Slider | null>(null)
const loadingList = ref(false)

const fileInput = ref<HTMLInputElement | null>(null)
const pendingFiles = ref<{ file: File; preview: string }[]>([])
const isDragging = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadResultMessage = ref('')
const uploadResultType = ref<'success' | 'error'>('success')

const showCreateModal = ref(false)
const newTitle = ref('')
const newSubtitle = ref('')
const creating = ref(false)
const createError = ref('')

const showEditModal = ref(false)
const editingSlider = ref<Slider | null>(null)
const editTitle = ref('')
const editSubtitle = ref('')
const editing = ref(false)
const editError = ref('')

async function loadSliders() {
  loadingList.value = true
  try {
    const { data } = await api.get('/selections', { params: { category: 'slider', limit: 100 } })
    sliders.value = data.data as Slider[]
  } finally {
    loadingList.value = false
  }
}

async function selectSlider(s: Slider) {
  const { data } = await api.get(`/selections/${s.id}`)
  selected.value = data.data as Slider
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
    pendingFiles.value.push({ file, preview: URL.createObjectURL(file) })
  }
}

function removePending(idx: number) {
  URL.revokeObjectURL(pendingFiles.value[idx].preview)
  pendingFiles.value.splice(idx, 1)
}

async function uploadImages() {
  if (!selected.value || pendingFiles.value.length === 0) return
  uploading.value = true
  uploadProgress.value = 0
  uploadResultMessage.value = ''

  const startOrder = selected.value.images.length
  let totalOriginal = 0
  let totalOptimized = 0

  try {
    for (let i = 0; i < pendingFiles.value.length; i++) {
      const { file } = pendingFiles.value[i]
      const uploadFileType = file.type || 'image/png'

      const { data: presignData } = await api.post('/uploads/presign', {
        filename: file.name,
        content_type: uploadFileType,
        target: 'selections',
      })
      const { upload_url, object_key } = presignData.data

      // S3 PUT 시 서버의 서명과 일치시키기 위해 buffer로 변환하여 전송합니다.
      const fileBuffer = await file.arrayBuffer()
      const uploadRes = await fetch(upload_url, {
        method: 'PUT',
        body: fileBuffer,
        headers: {
          'Content-Type': uploadFileType,
        },
      })
      if (!uploadRes.ok) throw new Error('S3 업로드 실패')

      // 3) Optimization
      const { data: optData } = await api.post('/uploads/optimize', { object_key })
      const finalKey: string = optData.data.optimized_key
      totalOriginal += optData.data.original_bytes ?? 0
      totalOptimized += optData.data.optimized_bytes ?? 0

      // 4) Registration
      await api.post(`/selections/${selected.value!.id}/images`, {
        image_url: finalKey,
        display_order: startOrder + i,
      })

      uploadProgress.value = i + 1
    }

    const count = pendingFiles.value.length
    const savedKB = Math.round((totalOriginal - totalOptimized) / 1024)
    const pct = totalOriginal > 0 ? Math.round((1 - totalOptimized / totalOriginal) * 100) : 0

    if (totalOriginal > 0) {
      uploadResultMessage.value = `${count}장 업로드 완료! (${pct}% 압축, ${savedKB}KB 절약)`
    } else {
      uploadResultMessage.value = `${count}장 업로드 완료!`
    }
    
    uploadResultType.value = 'success'
    console.log('Upload Result:', uploadResultMessage.value)
    setTimeout(() => { uploadResultMessage.value = '' }, 6000)

    pendingFiles.value.forEach(f => URL.revokeObjectURL(f.preview))
    pendingFiles.value = []

    await selectSlider(selected.value!)
  } catch (err) {
    console.error('Upload Error:', err)
    uploadResultMessage.value = '업로드 중 오류가 발생했습니다.'
    uploadResultType.value = 'error'
    setTimeout(() => { uploadResultMessage.value = '' }, 6000)
  } finally {
    uploading.value = false
  }
}

async function deleteImage(imageId: string) {
  if (!selected.value) return
  if (!confirm('이미지를 삭제하시겠습니까?')) return
  try {
    await api.delete(`/selections/${selected.value.id}/images/${imageId}`)
    await selectSlider(selected.value!)
  } catch {
    alert('삭제 실패')
  }
}

function openCreateModal() {
  newTitle.value = ''
  newSubtitle.value = ''
  createError.value = ''
  showCreateModal.value = true
}

async function createSlider() {
  if (!newTitle.value.trim()) { createError.value = '제목을 입력해주세요.'; return }
  creating.value = true
  createError.value = ''
  try {
    await api.post('/selections', {
      title: newTitle.value.trim(),
      subtitle: newSubtitle.value.trim() || null,
      category: 'slider',
    })
    showCreateModal.value = false
    await loadSliders()
  } catch {
    createError.value = '생성 실패'
  } finally {
    creating.value = false
  }
}

function openEditModal(s: Slider) {
  editingSlider.value = s
  editTitle.value = s.title
  editSubtitle.value = s.subtitle ?? ''
  editError.value = ''
  showEditModal.value = true
}

async function patchSlider() {
  if (!editingSlider.value) return
  if (!editTitle.value.trim()) { editError.value = '제목을 입력해주세요.'; return }
  editing.value = true
  editError.value = ''
  try {
    await api.patch(`/selections/${editingSlider.value.id}`, {
      title: editTitle.value.trim(),
      subtitle: editSubtitle.value.trim() || null,
    })
    showEditModal.value = false
    await loadSliders()
    if (selected.value?.id === editingSlider.value.id) {
      const updated = sliders.value.find(s => s.id === editingSlider.value!.id)
      if (updated) await selectSlider(updated)
    }
  } catch {
    editError.value = '수정 실패'
  } finally {
    editing.value = false
  }
}

async function confirmDelete(s: Slider) {
  if (!confirm(`"${s.title}" 항목을 삭제하시겠습니까?\n이미지도 모두 삭제됩니다.`)) return
  try {
    await api.delete(`/selections/${s.id}`)
    if (selected.value?.id === s.id) selected.value = null
    await loadSliders()
  } catch {
    alert('삭제 실패')
  }
}

onMounted(loadSliders)
</script>

<style scoped>
.admin-page { max-width: 1100px; }
.page-title { font-size: 20px; font-weight: 600; margin: 0 0 6px; color: #111; }
.page-desc { font-size: 13px; color: #888; margin: 0 0 24px; }

.main-layout { display: grid; grid-template-columns: 240px 1fr; gap: 24px; }

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
.item-info { display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0; overflow: hidden; }
.project-name { font-size: 13px; color: #222; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.project-sub { font-size: 11px; color: #aaa; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.item-actions { display: flex; align-items: center; gap: 4px; flex-shrink: 0; margin-left: 8px; }
.image-count { font-size: 11px; color: #aaa; margin-right: 2px; }
.btn-icon { background: none; border: none; cursor: pointer; font-size: 11px; color: #888; padding: 2px 4px; border-radius: 3px; opacity: 0; transition: opacity 0.15s, background 0.12s; }
.btn-icon-del { color: #c0392b; }
.project-item:hover .btn-icon { opacity: 1; }
.btn-icon:hover { background: #eee; }
.btn-icon-del:hover { background: #fce8e6; }
.empty-item { padding: 16px; font-size: 13px; color: #bbb; text-align: center; }

.image-panel { background: #fff; border: 1px solid #e8e8e8; border-radius: 6px; padding: 24px; }
.panel-header { margin-bottom: 20px; }
.panel-title { font-size: 16px; font-weight: 600; margin: 0; }
.panel-sub { font-size: 13px; color: #888; margin: 4px 0 0; }
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
.upload-result-box { display: flex; align-items: center; justify-content: space-between; gap: 12px; font-size: 13.5px; font-weight: 600; padding: 12px 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.upload-result-box.success { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; border-left: 5px solid #22c55e; }
.upload-result-box.error { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; border-left: 5px solid #ef4444; }
.result-icon { font-size: 16px; }
.result-text { flex: 1; }
.btn-msg-close { background: none; border: none; font-size: 16px; color: currentColor; cursor: pointer; opacity: 0.5; }
.btn-msg-close:hover { opacity: 1; }

.fade-enter-active, .fade-leave-active { transition: all 0.4s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-10px); }

.registered-images { margin-top: 32px; }
.section-label { font-size: 13px; font-weight: 600; color: #555; margin: 0 0 12px; }
.no-images { font-size: 13px; color: #bbb; padding: 20px 0; }
.image-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 10px; }
.image-card { position: relative; aspect-ratio: 16/9; background: #f0f0f0; border-radius: 4px; overflow: hidden; }
.image-card img { width: 100%; height: 100%; object-fit: cover; }
.order-badge { position: absolute; top: 6px; left: 6px; background: rgba(0,0,0,0.6); color: #fff; font-size: 10px; padding: 2px 6px; border-radius: 3px; z-index: 1; }
.btn-delete-img { position: absolute; top: 4px; right: 4px; background: rgba(0,0,0,0.55); color: #fff; border: none; width: 22px; height: 22px; border-radius: 50%; cursor: pointer; font-size: 10px; display: flex; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.15s; }
.image-card:hover .btn-delete-img { opacity: 1; }

.required { color: #c0392b; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; padding: 32px; width: 400px; border-radius: 8px; }
.modal-title { font-size: 16px; font-weight: 600; margin: 0 0 24px; }
.field { display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }
.field label { font-size: 12px; font-weight: 500; color: #444; }
.field input { padding: 10px 12px; border: 1px solid #ddd; font-size: 14px; outline: none; font-family: inherit; border-radius: 3px; }
.field input:focus { border-color: #333; }
.error-msg { font-size: 12px; color: #c0392b; margin: 0 0 12px; }
.modal-actions { display: flex; gap: 8px; justify-content: flex-end; }
.btn-cancel { padding: 9px 20px; border: 1px solid #ddd; background: #fff; font-size: 13px; cursor: pointer; border-radius: 4px; }
.btn-confirm { padding: 9px 20px; background: #1a1a1a; color: #fff; border: none; font-size: 13px; cursor: pointer; border-radius: 4px; }
.btn-confirm:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.4); border-top-color: #fff; border-radius: 50%; animation: spin 0.7s linear infinite; vertical-align: middle; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
