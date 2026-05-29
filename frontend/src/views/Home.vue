<template>
  <div class="home-container">
    
    <nav class="navbar">
      <div class="nav-brand">Analytics Fish</div>
      <div class="nav-links"></div>
    </nav>

    <div class="main-content">
      
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="orange-tag">{{ $t('home.tagline') }}</span>
            <span class="version-text">{{ $t('home.version') }}</span>
          </div>
          
          <h1 class="main-title">
            {{ $t('home.heroTitle1') }}<br>
            <span class="gradient-text">{{ $t('home.heroTitle2') }}</span>
          </h1>
          
          <div class="hero-desc">
            <p>
              <i18n-t keypath="home.heroDesc" tag="span">
                <template #brand><span class="highlight-bold">{{ $t('home.heroDescBrand') }}</span></template>
                <template #agentScale><span class="highlight-orange">{{ $t('home.heroDescAgentScale') }}</span></template>
                <template #optimalSolution><span class="highlight-code">{{ $t('home.heroDescOptimalSolution') }}</span></template>
              </i18n-t>
            </p>
            <p class="slogan-text">
              {{ $t('home.slogan') }}<span class="blinking-cursor">_</span>
            </p>
          </div>
           
          <div class="decoration-square"></div>
        </div>
        
        <div class="hero-right">
          <button class="scroll-down-btn" @click="scrollToBottom">
            ↓
          </button>
        </div>
      </section>

      
      <section class="dashboard-section">
        
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> {{ $t('home.systemStatus') }}
          </div>
          
          <h2 class="section-title">{{ $t('home.systemReady') }}</h2>
          <p class="section-desc">
            {{ $t('home.systemReadyDesc') }}
          </p>
          
          
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">{{ $t('home.metricLowCost') }}</div>
              <div class="metric-label">{{ $t('home.metricLowCostDesc') }}</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">{{ $t('home.metricHighAvail') }}</div>
              <div class="metric-label">{{ $t('home.metricHighAvailDesc') }}</div>
            </div>
          </div>

          
          <div class="steps-container">
            <div class="steps-header">
               <span class="diamond-icon">◇</span> {{ $t('home.workflowSequence') }}
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <span class="step-num">01</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step01Title') }}</div>
                  <div class="step-desc">{{ $t('home.step01Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">02</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step02Title') }}</div>
                  <div class="step-desc">{{ $t('home.step02Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">03</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step03Title') }}</div>
                  <div class="step-desc">{{ $t('home.step03Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">04</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step04Title') }}</div>
                  <div class="step-desc">{{ $t('home.step04Desc') }}</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">05</span>
                <div class="step-info">
                  <div class="step-title">{{ $t('home.step05Title') }}</div>
                  <div class="step-desc">{{ $t('home.step05Desc') }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        
        <div class="right-panel">
          <div class="console-box">
            
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">{{ $t('home.realitySeed') }}</span>
                <span class="console-meta">{{ $t('home.supportedFormats') }}</span>
              </div>
              
              <div 
                class="upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />
                
                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">↑</div>
                  <div class="upload-title">{{ $t('home.dragToUpload') }}</div>
                  <div class="upload-hint">{{ $t('home.orBrowse') }}</div>
                </div>
                
                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            
            <div class="console-divider">
              <span>{{ $t('home.inputParams') }}</span>
            </div>

            
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">{{ $t('home.simulationPrompt') }}</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  :placeholder="$t('home.promptPlaceholder')"
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">{{ $t('home.engineBadge') }}</div>
              </div>
            </div>

            
            <div class="console-section btn-section">
              <button 
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!loading">{{ $t('home.startEngine') }}</span>
                <span v-else>{{ $t('home.initializing') }}</span>
                <span class="btn-arrow">→</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      
      <HistoryDatabase />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'

const router = useRouter()
const formData = ref({
  simulationRequirement: ''
})
const files = ref([])
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)
const fileInput = ref(null)
const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== '' && files.value.length > 0
})
// @ 2026 Developed by Saksham Nirula
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}
const removeFile = (index) => {
  files.value.splice(index, 1)
}
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(files.value, formData.value.simulationRequirement)
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  })
}
</script>

<style scoped>

:root {
  --primary: #0F172A;
  --secondary: #1E293B;
  --accent: #06B6D4;
  --accent-2: #8B5CF6;
  --accent-3: #EC4899;
  --text-primary: #F8FAFC;
  --text-secondary: #94A3B8;
  --text-tertiary: #64748B;
  --bg-dark: #0F172A;
  --bg-card: #1E293B;
  --border-dark: #334155;

  --primary-gradient: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%);
  --secondary-gradient: linear-gradient(135deg, #EC4899 0%, #F43F5E 100%);
  --tertiary-gradient: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%);
  --warm-gradient: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);

  --font-mono: 'IBM Plex Mono', 'Courier New', monospace;
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  --font-display: 'Sora', -apple-system, BlinkMacSystemFont, sans-serif;
}

.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--bg-dark) 0%, #1a2f4f 100%);
  font-family: var(--font-sans);
  color: var(--text-primary);
}


.navbar {
  height: 70px;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.8) 100%);
  color: var(--text-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 50px;
  border-bottom: 1px solid rgba(6, 182, 212, 0.1);
  backdrop-filter: blur(10px);
}

.nav-brand {
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: 0px;
  font-size: 1.4rem;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.arrow {
  font-family: sans-serif;
}


.main-content {
  max-width: 100%;
  margin: 0;
  padding: 60px 0;
}


.hero-section {
  display: flex;
  justify-content: center;
  margin-bottom: 0;
  position: relative;
  background: transparent;
  padding: 80px 60px;
  border-radius: 0;
  perspective: 1000px;
  box-shadow: none;
}

.hero-left {
  flex: 1;
  padding-right: 0;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 900px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  justify-content: center;
}

.orange-tag {
  background: rgba(6, 182, 212, 0.2);
  color: var(--accent);
  padding: 6px 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  font-size: 0.75rem;
  border-radius: 6px;
  border: 1px solid rgba(6, 182, 212, 0.4);
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.2);
}

.version-text {
  color: #999;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.main-title {
  font-size: 4.5rem;
  line-height: 1.1;
  font-weight: 700;
  margin: 0 0 40px 0;
  letter-spacing: -1.5px;
  color: var(--text-primary);
  font-family: var(--font-display);
  text-align: center;
}

.gradient-text {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--text-secondary);
  max-width: 700px;
  margin-bottom: 50px;
  font-weight: 400;
  text-align: center;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: var(--text-primary);
  font-weight: 700;
}

.highlight-orange {
  color: var(--accent);
  font-weight: 700;
  font-family: var(--font-mono);
}

.highlight-code {
  background: rgba(6, 182, 212, 0.15);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--accent);
  font-weight: 600;
}

.slogan-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 0.5px;
  border-bottom: 3px solid var(--accent);
  padding-bottom: 10px;
  margin-top: 20px;
  text-align: center;
}

.blinking-cursor {
  color: var(--accent);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: var(--orange);
}

.hero-right {
  flex: 0.8;
  display: none;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-end;
}


.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 2px solid rgba(6, 182, 212, 0.5);
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(139, 92, 246, 0.1));
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--accent);
  font-size: 1.2rem;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  border-radius: 8px;
}

.scroll-down-btn:hover {
  border-color: var(--accent);
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(139, 92, 246, 0.2));
  transform: translateY(4px);
  box-shadow: 0 8px 24px rgba(6, 182, 212, 0.2);
}


.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: none;
  padding: 80px 60px;
  align-items: flex-start;
  background: transparent;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}


.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: var(--accent);
  font-size: 0.8rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 15px 0;
  color: var(--text-primary);
  font-family: var(--font-display);
}

.section-desc {
  color: var(--text-secondary);
  margin-bottom: 25px;
  line-height: 1.6;
}

.metrics-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric-card {
  border: 1px solid rgba(6, 182, 212, 0.3);
  padding: 24px 32px;
  min-width: 150px;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(30, 58, 138, 0.1) 100%);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(6, 182, 212, 0.1);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  cursor: pointer;
}

.metric-card:hover {
  transform: translateY(-8px) rotateX(5deg);
  box-shadow: 0 12px 48px rgba(6, 182, 212, 0.2);
  border-color: rgba(6, 182, 212, 0.6);
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 5px;
  color: var(--accent);
}

.metric-label {
  font-size: 0.85rem;
  color: var(--text-tertiary);
}


.steps-container {
  border: 1px solid rgba(139, 92, 246, 0.2);
  padding: 40px;
  position: relative;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(236, 72, 153, 0.06) 100%);
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(139, 92, 246, 0.1);
}

.steps-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--text-tertiary);
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding: 15px;
  border-radius: 10px;
  transition: all 0.3s ease;
  background: rgba(139, 92, 246, 0.05);
}

.workflow-item:hover {
  background: rgba(139, 92, 246, 0.15);
  transform: translateX(8px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.2);
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--accent);
  opacity: 0.6;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.step-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
}


.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid rgba(6, 182, 212, 0.4);
  padding: 8px;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(6, 182, 212, 0.15);
  backdrop-filter: blur(10px);
}

.console-section {
  padding: 20px;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
  border-radius: 10px;
  margin-bottom: 10px;
  border: 1px solid rgba(6, 182, 212, 0.25);
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--accent);
  font-weight: 600;
  letter-spacing: 1px;
}

.upload-zone {
  border: 2px dashed rgba(6, 182, 212, 0.6);
  height: 200px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
  border-radius: 12px;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%);
  border-color: rgba(6, 182, 212, 0.8);
  box-shadow: 0 8px 32px rgba(6, 182, 212, 0.3);
}

.upload-placeholder {
  text-align: center;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-icon {
  width: 50px;
  height: 50px;
  border: 2px solid var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: var(--accent);
  border-radius: 8px;
  font-size: 1.5rem;
  font-weight: 600;
}

.upload-title {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 5px;
  color: var(--accent);
  text-align: center;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-align: center;
}

.file-list {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  background: rgba(30, 41, 59, 0.8);
  padding: 8px 12px;
  border: 1px solid rgba(6, 182, 212, 0.2);
  font-family: var(--font-mono);
  font-size: 0.85rem;
  border-radius: 6px;
  color: var(--text-secondary);
}

.file-name {
  flex: 1;
  margin: 0 10px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: var(--text-tertiary);
  transition: color 0.2s;
}

.remove-btn:hover {
  color: var(--accent);
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 15px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 2px;
  background: linear-gradient(90deg, rgba(6, 182, 212, 0.3), transparent);
}

.console-divider::after {
  background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.3));
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--accent);
  letter-spacing: 1px;
  font-weight: 600;
}

.input-wrapper {
  position: relative;
  border: 2px solid rgba(6, 182, 212, 0.4);
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
  border-radius: 10px;
  transition: all 0.3s ease;
}

.input-wrapper:focus-within {
  border-color: var(--accent);
  box-shadow: 0 8px 24px rgba(6, 182, 212, 0.25);
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 150px;
  color: var(--text-primary);
}

.code-input::placeholder {
  color: rgba(6, 182, 212, 0.5);
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--accent);
  font-weight: 600;
}

.start-engine-btn {
  width: 100%;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
  color: var(--text-primary);
  border: none;
  padding: 20px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(6, 182, 212, 0.3);
}


.start-engine-btn:not(:disabled) {
  animation: pulse-glow 2s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--accent-2) 0%, var(--accent-3) 100%);
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 16px 48px rgba(139, 92, 246, 0.4);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(-2px) scale(0.99);
}

.start-engine-btn:disabled {
  background: linear-gradient(135deg, rgba(100, 116, 139, 0.3) 0%, rgba(71, 85, 105, 0.3) 100%);
  color: var(--text-tertiary);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}


@keyframes pulse-glow {
  0% { box-shadow: 0 8px 24px rgba(6, 182, 212, 0.3); }
  50% { box-shadow: 0 12px 36px rgba(6, 182, 212, 0.5); }
  100% { box-shadow: 0 8px 24px rgba(6, 182, 212, 0.3); }
}


@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }
  
  .hero-section {
    flex-direction: column;
  }
  
  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }
  
  .hero-logo {
    max-width: 200px;
    margin-bottom: 20px;
  }
}
</style>

<style>

html[lang="en"] .main-title {
  font-size: 3.5rem;
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: -1px;
}

html[lang="en"] .hero-desc {
  text-align: left;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: 0;
}

html[lang="en"] .slogan-text {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  letter-spacing: 0;
}

html[lang="en"] .tag-row {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .navbar .nav-links {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}


html[lang="en"] .status-section {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .status-section .status-ready {
  font-size: 1.6rem;
}

html[lang="en"] .status-section .metric-value {
  font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 1.4rem;
}

html[lang="en"] .workflow-list .step-title {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

html[lang="en"] .workflow-list .step-desc {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  font-size: 0.72rem !important;
  line-height: 1.4 !important;
}

html[lang="en"] .workflow-list {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
</style>
