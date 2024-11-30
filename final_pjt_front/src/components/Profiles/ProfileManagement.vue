<template>
  <div class="arcade-stats-container">
    <div v-if="userInfo" class="user-stats">
      <!-- 네온 헤더 -->
      <div class="neon-header">
        <div class="player-info">
          <div class="glitch-text" data-text="PLAYER STATUS">PLAYER STATUS</div>
          <div class="player-name">{{ userInfo.nickname }}</div>
        </div>
        <div class="tier-badge">
          <span class="tier-text">{{ userInfo.tier }}</span>
          <div class="tier-glow"></div>
        </div>
      </div>

      <!-- 스탯 그리드 -->
      <div class="cyber-grid">
        <!-- 기본 정보 카드 -->
        <div class="cyber-card">
          <div class="card-header">
            <i class="fas fa-user neon-icon"></i>
            <h3>BASIC INFO</h3>
            <RouterLink :to="{name : 'ProfileEdit'}" class="edit-button">
              <i class="fas fa-pencil"></i>
            </RouterLink>
          </div>
          <div class="card-content">
            <div class="data-line">
              <span class="label">NICKNAME:</span>
              <span class="value">{{ userInfo.nickname }}</span>
            </div>
            <div class="data-line">
              <span class="label">AGE:</span>
              <span class="value">{{ userInfo.age }} YEARS</span>
            </div>
            <div class="data-line">
              <span class="label">EMAIL:</span>
              <span class="value">{{ userInfo.email }}</span>
            </div>
          </div>
        </div>

        <!-- 자산 정보 카드 -->
        <div class="cyber-card">
          <div class="card-header">
            <i class="fas fa-coins neon-icon"></i>
            <h3>ASSETS</h3>
            <RouterLink :to="{name : 'ProfileEdit'}" class="edit-button">
              <i class="fas fa-pencil"></i>
            </RouterLink>
          </div>
          <div class="card-content">
            <div class="data-line">
              <span class="label">CURRENT:</span>
              <span class="value">₩ {{ formatNumber(userInfo.assets) }}</span>
            </div>
            <div class="data-line">
              <span class="label">ANNUAL:</span>
              <span class="value">₩ {{ formatNumber(userInfo.annual_income) }}</span>
            </div>
          </div>
        </div>

        <!-- 투자 목표 카드 -->
        <div class="cyber-card">
          <div class="card-header">
            <i class="fas fa-bullseye neon-icon"></i>
            <h3>INVESTMENT GOAL</h3>
            <RouterLink :to="{name : 'ProfileEdit'}" class="edit-button">
              <i class="fas fa-pencil"></i>
            </RouterLink>
          </div>
          <div class="card-content">
            <div class="data-line">
              <span class="label">TARGET:</span>
              <span class="value">₩ {{ formatNumber(userInfo.desired_amount) }}</span>
            </div>
            <div class="data-line">
              <span class="label">PERIOD:</span>
              <span class="value">{{ userInfo.desired_period }} MONTHS</span>
            </div>
            <div class="progress-container">
              <div class="progress-bar">
                <div 
                  class="progress-fill"
                  :style="{ width: progressPercentage + '%' }"
                >
                  {{ progressPercentage }}%
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 투자 성향 분석 카드 -->
        <div class="cyber-card analysis-card">
          <div class="card-header">
            <i class="fas fa-chart-pie neon-icon"></i>
            <h3>INVESTMENT ANALYSIS</h3>
          </div>
          <div class="card-content">
            <div class="analysis-grid">
              <!-- 3D 캐릭터 섹션 -->
              <div class="character-section">
                <div class="character-container" ref="characterContainer"></div>
              </div>

              <!-- 레이더 차트 섹션 -->
              <div class="radar-section">
                <canvas ref="radarChart"></canvas>
              </div>

              <!-- 분석 점수 섹션 -->
              <div class="scores-section">
                <div class="score-item" v-for="(score, index) in analysisScores" :key="index">
                  <div class="score-label">{{ score.label }}</div>
                  <div class="score-bar-container">
                    <div class="score-bar" :style="{ width: score.value + '%' }">
                      <span class="score-value">{{ score.value }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 로딩 스피너 -->
    <div v-else class="loading-container">
      <div class="neon-spinner"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/tier'
import axios from 'axios'
import Chart from 'chart.js/auto'
import * as THREE from 'three'

// 상태 관리
const userStore = useUserStore()
const router = useRouter()
const userInfo = ref(null)
const error = ref(null)
const radarChart = ref(null)
const chartInstance = ref(null)
const characterContainer = ref(null)

// Scene, camera, renderer variables
let scene, camera, renderer, robot
let animationId

// 분석 점수 데이터
const analysisScores = ref([
  { label: 'RISK TOLERANCE', value: 65 },
  { label: 'EXPERIENCE', value: 75 },
  { label: 'INVESTMENT PERIOD', value: 80 },
  { label: 'RETURN EXPECTATION', value: 70 },
  { label: 'LOSS TOLERANCE', value: 60 }
])

// Computed Properties
const progressPercentage = computed(() => {
  if (!userInfo.value) return 0
  const percentage = (userInfo.value.assets / userInfo.value.desired_amount) * 100
  return Math.min(Math.round(percentage), 100)
})

// Methods
const formatNumber = (number) => {
  return new Intl.NumberFormat('ko-KR').format(number)
}

// 3D Character Initialization
const initCharacter = () => {
  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(
    75,
    characterContainer.value.clientWidth / characterContainer.value.clientHeight,
    0.1,
    1000
  )
  camera.position.z = 5

  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
  renderer.setSize(characterContainer.value.clientWidth, characterContainer.value.clientHeight)
  characterContainer.value.appendChild(renderer.domElement)

  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
  scene.add(ambientLight)

  const pointLight = new THREE.PointLight(0xff00ff, 1)
  pointLight.position.set(5, 5, 5)
  scene.add(pointLight)

  // Robot creation
  const createRobot = () => {
    const group = new THREE.Group()

    // Head
    const head = new THREE.Mesh(
      new THREE.BoxGeometry(1, 1, 1),
      new THREE.MeshPhongMaterial({
        color: 0x404040,
        emissive: 0xff00ff,
        emissiveIntensity: 0.2,
      })
    )
    head.position.y = 1.5
    group.add(head)

    // Eyes
    const eyeGeometry = new THREE.SphereGeometry(0.15, 16, 16)
    const eyeMaterial = new THREE.MeshPhongMaterial({
      color: 0xff00ff,
      emissive: 0xff00ff,
      emissiveIntensity: 0.5,
    })

    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial)
    leftEye.position.set(-0.2, 1.5, 0.5)
    group.add(leftEye)

    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial)
    rightEye.position.set(0.2, 1.5, 0.5)
    group.add(rightEye)

    // Body
    const body = new THREE.Mesh(
      new THREE.CylinderGeometry(0.5, 0.7, 1.5, 8),
      new THREE.MeshPhongMaterial({
        color: 0x505050,
        emissive: 0xff00ff,
        emissiveIntensity: 0.1,
      })
    )
    body.position.y = 0.4
    group.add(body)

    // Arms
    const armGeometry = new THREE.CylinderGeometry(0.15, 0.15, 1, 8)
    const armMaterial = new THREE.MeshPhongMaterial({
      color: 0x606060,
      emissive: 0xff00ff,
      emissiveIntensity: 0.15,
    })

    const leftArm = new THREE.Mesh(armGeometry, armMaterial)
    leftArm.position.set(-0.8, 0.7, 0)
    leftArm.rotation.z = -Math.PI / 4
    group.add(leftArm)

    const rightArm = new THREE.Mesh(armGeometry, armMaterial)
    rightArm.position.set(0.8, 0.7, 0)
    rightArm.rotation.z = Math.PI / 4
    group.add(rightArm)

    return group
  }

  robot = createRobot()
  scene.add(robot)

  const animate = () => {
    animationId = requestAnimationFrame(animate)
    
    // Floating effect
    robot.position.y = Math.sin(Date.now() * 0.001) * 0.2
    
    // Rotation
    robot.rotation.y += 0.01

    // Eye blinking
    const eyes = robot.children.filter(child => 
      child.geometry instanceof THREE.SphereGeometry
    )
    eyes.forEach(eye => {
      eye.material.emissiveIntensity = 0.5 + Math.sin(Date.now() * 0.003) * 0.3
    })

    renderer.render(scene, camera)
  }

  animate()
}

// Radar Chart Initialization
const initRadarChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  const ctx = radarChart.value.getContext('2d')
  chartInstance.value = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: analysisScores.value.map(score => score.label),
      datasets: [{
        data: analysisScores.value.map(score => score.value),
        backgroundColor: 'rgba(255, 0, 255, 0.2)',
        borderColor: '#f0f',
        pointBackgroundColor: '#f0f',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#f0f'
      }]
    },
    options: {
      scales: {
        r: {
          beginAtZero: true,
          max: 100,
          ticks: {
            stepSize: 20,
            color: 'rgba(255, 255, 255, 0.7)',
            backdropColor: 'transparent'
          },
          grid: {
            color: 'rgba(255, 0, 255, 0.1)'
          },
          angleLines: {
            color: 'rgba(255, 0, 255, 0.1)'
          },
          pointLabels: {
            color: 'rgba(255, 255, 255, 0.7)',
            font: {
              family: 'DungGeunMo',
              size: 12
            }
          }
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    }
  })
}

// Fetch User Info
const fetchUserInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:8000/accounts/profile_view/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    userInfo.value = response.data
    userStore.tier = response.data.tier
    localStorage.setItem('userTier', response.data.tier)
  } catch (err) {
    console.error('Error fetching user info:', err)
    error.value = '프로필 정보를 불러오는데 실패했습니다.'
  }
}

// Resize Handler
const handleResize = () => {
  if (camera && renderer && characterContainer.value) {
    camera.aspect = characterContainer.value.clientWidth / characterContainer.value.clientHeight
    camera.updateProjectionMatrix()
    renderer.setSize(characterContainer.value.clientWidth, characterContainer.value.clientHeight)
  }
}

// Watchers
watch(() => userStore.tier, (newTier) => {
  if (userInfo.value) {
    userInfo.value.tier = newTier
  }
})

// Lifecycle Hooks
onMounted(async () => {
  try {
    await fetchUserInfo()
    await nextTick()
    
    if (radarChart.value) {
      initRadarChart()
    }
    if (characterContainer.value) {
      initCharacter()
    }
    
    window.addEventListener('resize', handleResize)
  } catch (err) {
    console.error('Error in component initialization:', err)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  cancelAnimationFrame(animationId)
  if (renderer) {
    renderer.dispose()
  }
})
</script>

<style scoped>
.arcade-stats-container {
  width: 100%;
  height: calc(80vh - 4rem);
  color: #fff;
  padding: 30px;
  overflow-y: auto;
}

/* 네온 헤더 스타일 */
.neon-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(255, 0, 255, 0.1);
  border: 2px solid #f0f;
  border-radius: 10px;
}

.glitch-text {
  font-size: 2rem;
  color: #f0f;
  text-shadow: 
    2px 2px #0ff,
    -2px -2px #f00;
  animation: glitch 1s infinite;
}

.player-name {
  font-size: 1.5rem;
  color: #fff;
  margin-top: 10px;
  text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

.tier-badge {
  position: relative;
  padding: 10px 20px;
  background: rgba(255, 0, 255, 0.2);
  border: 2px solid #f0f;
  border-radius: 5px;
}

.tier-text {
  position: relative;
  z-index: 2;
  font-size: 1.2rem;
  font-weight: bold;
  text-shadow: 0 0 10px #f0f;
}

/* 그리드 레이아웃 */
.cyber-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

/* 카드 스타일 */
.cyber-card {
  background: rgba(255, 0, 255, 0.05);
  border: 2px solid #f0f;
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.cyber-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
}

.card-header {
  background: linear-gradient(45deg, #f0f, #90f);
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.neon-icon {
  color: #fff;
  font-size: 1.5rem;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
}

.card-header h3 {
  margin: 0;
  flex: 1;
  font-size: 1.2rem;
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.edit-button {
  color: #fff;
  font-size: 1rem;
  opacity: 0.7;
  transition: all 0.3s ease;
}

.edit-button:hover {
  opacity: 1;
  transform: scale(1.1);
}

.card-content {
  padding: 20px;
}

/* 데이터 라인 스타일 */
.data-line {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.label {
  color: rgba(255, 255, 255, 0.7);
}

.value {
  color: #0ff;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
}

/* 프로그레스 바 스타일 */
.progress-container {
  margin-top: 15px;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #f0f, #0ff);
  transition: width 0.6s ease;
  text-align: right;
  padding-right: 5px;
  font-size: 0.8rem;
  line-height: 10px;
}

/* 투자 성향 분석 카드 */
.analysis-card {
  grid-column: 1 / -1;
}

.analysis-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 30px;
  height: 400px;
}

/* 3D 캐릭터 섹션 */
.character-section {
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  overflow: hidden;
}

.character-container {
  width: 100%;
  height: 100%;
}

/* 레이더 차트 섹션 */
.radar-section {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 20px;
}

/* 점수 섹션 */
.scores-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
  padding: 20px;
}

.score-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.score-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  font-family: 'DungGeunMo';
}

.score-bar-container {
  width: 100%;
  height: 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 7px;
  overflow: hidden;
}

.score-bar {
  height: 100%;
  background: linear-gradient(90deg, #f0f, #0ff);
  border-radius: 7px;
  transition: width 0.5s ease;
  position: relative;
}

.score-value {
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.8rem;
  color: #fff;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

/* 로딩 스피너 */
.loading-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.neon-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid transparent;
  border-top-color: #f0f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 애니메이션 */
@keyframes glitch {
  0% { text-shadow: 2px 2px #0ff, -2px -2px #f00; }
  25% { text-shadow: -2px 2px #0ff, 2px -2px #f00; }
  50% { text-shadow: 2px -2px #0ff, -2px 2px #f00; }
  75% { text-shadow: -2px -2px #0ff, 2px 2px #f00; }
  100% { text-shadow: 2px 2px #0ff, -2px -2px #f00; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .cyber-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .analysis-grid {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto 1fr;
  }

  .character-section {
    grid-column: 1 / -1;
    height: 300px;
  }
}

@media (max-width: 768px) {
  .neon-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .glitch-text {
    font-size: 1.5rem;
  }

  .cyber-grid {
    grid-template-columns: 1fr;
  }

  .analysis-grid {
    grid-template-columns: 1fr;
    height: auto;
    gap: 20px;
  }

  .radar-section {
    height: 300px;
  }

  .character-section {
    height: 250px;
  }
}
</style>