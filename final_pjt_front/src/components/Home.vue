<template>
  <div class="arcade-container" ref="container">
    <div class="three-scene" ref="threeScene"></div>
    <div class="screen-overlay">
      <div class="game-screen">
        <RouterView v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </RouterView>
      </div>
    </div>
    
    <!-- 드래그 가능한 게임패드 스타일의 컨트롤러 -->
    <div 
      class="arcade-controls"
      ref="draggableControl"
      :class="{ 'stored': isStored }"
      :style="{ 
        left: position.x + 'px', 
        top: position.y + 'px'
      }"
      @mousedown="startDrag"
      @touchstart.passive="startDrag"
    >
      <!-- 보관/꺼내기 버튼 -->
      <template v-if="!isStored">
        <button class="store-button" @click.stop="toggleStorage" title="보관하기">
          <i class="fas fa-chevron-right"></i>
        </button>
      </template>

      <div class="controller-design">
        <div class="controller-header">
          <div class="led-light"></div>
          <div class="brand-text">WEALTH ARCADE</div>
        </div>

        <div class="controller-body">
          <div class="joystick-section">
            <div class="joystick">
              <RouterLink :to="{name : 'StartView' }" class="home-button">
                <span class="button-label">HOME</span>
              </RouterLink>
            </div>
          </div>

          <template v-if="authStore.isLoggedIn">
            <div class="button-grid">
              <RouterLink :to="{name : 'ItemListView' }" class="arcade-button inventory">
                <span class="button-label">상점</span>
              </RouterLink>
              <RouterLink :to="{name : 'AcademyView'}" class="arcade-button training">
                <span class="button-label">훈련장</span>
              </RouterLink>
              <RouterLink :to="{name : 'QuestView'}" class="arcade-button quest">
                <span class="button-label">퀘스트</span>
              </RouterLink>
              <RouterLink :to="{name : 'CashShopView'}" class="arcade-button shop">
                <span class="button-label">캐시샵</span>
              </RouterLink>
            </div>
          </template>
        </div>

        <div class="controller-footer">
          <div class="footer-line"></div>
          <div class="footer-text">©WEALTH ARCADE</div>
        </div>
      </div>
    </div>

    <!-- 복원 레버 (보관 상태일 때만 표시) -->
    <button 
  v-if="isStored"
  class="restore-button" 
  @click.stop="toggleStorage" 
  title="꺼내기"
>
  <i class="fas fa-chevron-left"></i>
  <div class="gamepad-icon">
    <i class="fas fa-gamepad"></i>
  </div>
</button>
  </div>
</template>


<script setup>
import * as THREE from 'three'
import { ref, onMounted, onUnmounted } from 'vue'
import { useGameStore } from '../stores/game'
import { useAuthStore } from '../stores/auth'
import { storeToRefs } from 'pinia'
import { RouterLink, RouterView } from 'vue-router'

const container = ref(null)
const threeScene = ref(null)
const gameStore = useGameStore()
const authStore = useAuthStore()
const { score, highScore, isPlaying } = storeToRefs(gameStore)
const draggableControl = ref(null)

// 컨트롤러 상태
const isStored = ref(false)
const initialPosition = {
  x: window.innerWidth - 450 - 20,
  y: window.innerHeight / 2
}

// 드래그 관련 상태
const position = ref({ ...initialPosition })
const isDragging = ref(false)
const dragOffset = ref({ x: 0, y: 0 })

// Three.js 관련 변수
let scene, camera, renderer, arcadeMachine

// 보관/꺼내기 함수
const toggleStorage = () => {
  isStored.value = !isStored.value
  if (isStored.value) {
    position.value.x = window.innerWidth - 40
  } else {
    position.value.x = initialPosition.x
  }
}

const startDrag = (event) => {
  if (
    event.target.closest('.arcade-button') || 
    event.target.closest('.home-button') ||
    event.target.closest('.store-button') ||
    event.target.closest('.restore-button') ||
    isStored.value
  ) return;
  
  isDragging.value = true
  const clientX = event.type === 'mousedown' ? event.clientX : event.touches[0].clientX
  const clientY = event.type === 'mousedown' ? event.clientY : event.touches[0].clientY
  
  dragOffset.value = {
    x: clientX - position.value.x,
    y: clientY - position.value.y
  }

  if (event.type === 'mousedown') {
    window.addEventListener('mousemove', doDrag)
    window.addEventListener('mouseup', stopDrag)
  } else {
    window.addEventListener('touchmove', doDrag, {passive: false})
    window.addEventListener('touchend', stopDrag)
  }
}

const doDrag = (event) => {
  if (!isDragging.value) return

  event.preventDefault()
  requestAnimationFrame(() => {  // 부드러운 움직임을 위한 최적화
    const clientX = event.type === 'mousemove' ? event.clientX : event.touches[0].clientX
    const clientY = event.type === 'mousemove' ? event.clientY : event.touches[0].clientY
    
    position.value = {
      x: clientX - dragOffset.value.x,
      y: clientY - dragOffset.value.y
    }

    const control = draggableControl.value
    if (control) {
      const rect = control.getBoundingClientRect()
      if (position.value.x < 0) position.value.x = 0
      if (position.value.y < 0) position.value.y = 0
      if (position.value.x + rect.width > window.innerWidth) {
        position.value.x = window.innerWidth - rect.width
      }
      if (position.value.y + rect.height > window.innerHeight) {
        position.value.y = window.innerHeight - rect.height
      }
    }
  })
}

const stopDrag = () => {
  isDragging.value = false
  window.removeEventListener('mousemove', doDrag)
  window.removeEventListener('mouseup', stopDrag)
  window.removeEventListener('touchmove', doDrag)
  window.removeEventListener('touchend', stopDrag)
}

// Three.js 초기화
const init = () => {
  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  threeScene.value.appendChild(renderer.domElement)

  const textureLoader = new THREE.TextureLoader()
  const boxTexture = textureLoader.load('/arcade.jpg')
  const material = new THREE.MeshPhongMaterial({
    map: boxTexture,
    specular: 0x666666,
    shininess: 30
  })
  
  const materials = [
    new THREE.MeshPhongMaterial({ map: textureLoader.load('/arcade.jpg') }),
    new THREE.MeshPhongMaterial({ map: textureLoader.load('/arcade.jpg') }),
    new THREE.MeshPhongMaterial({ map: textureLoader.load('/arcade.jpg') }),
    new THREE.MeshPhongMaterial({ map: textureLoader.load('/arcade.jpg') }),
    new THREE.MeshPhongMaterial({ map: textureLoader.load('/arcade.jpg') }),
    new THREE.MeshPhongMaterial({ map: textureLoader.load('/arcade.jpg') })
  ]
  
  const geometry = new THREE.BoxGeometry(10, 6, 2)
  arcadeMachine = new THREE.Mesh(geometry, materials)
  arcadeMachine = new THREE.Mesh(geometry, material)
  scene.add(arcadeMachine)

  const screenGeometry = new THREE.PlaneGeometry(1.5, 1.5)
  const screenMaterial = new THREE.MeshPhongMaterial({
    color: 0x000000,
    transparent: true,
    opacity: 0.9
  })
  const arcadeScreen = new THREE.Mesh(screenGeometry, screenMaterial)
  arcadeScreen.position.z = 0.51
  arcadeScreen.position.y = 0.5
  arcadeMachine.add(arcadeScreen)

  const light = new THREE.DirectionalLight(0xffffff, 2)
  light.position.set(4, 5, 5)
  scene.add(light)
  
  const ambientLight = new THREE.AmbientLight(0x404040)
  scene.add(ambientLight)

  camera.position.z = 5

  animate()
}

const animate = () => {
  requestAnimationFrame(animate)
  if (arcadeMachine) {
    arcadeMachine.rotation.y = Math.sin(Date.now() * 0.001) * 0.1
  }
  renderer.render(scene, camera)
}

const handleResize = () => {
  if (camera && renderer) {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
  }
  
  // 컨트롤러 위치 조정
  if (isStored.value) {
    position.value.x = window.innerWidth - 40
  } else {
    position.value.x = window.innerWidth - 450 - 20
  }
}

onMounted(() => {
  init()
  authStore.checkLoginStatus()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (renderer) {
    renderer.dispose()
  }
  stopDrag()
})

// template에서 사용할 변수와 함수들을 노출
defineExpose({
  container,
  threeScene,
  score,
  highScore,
  isPlaying,
  authStore,
  position,
  draggableControl,
  startDrag,
  isStored,
  toggleStorage
})
</script>

<style scoped>
.arcade-container {
  width: 100vw;
  height: 100vh;
  position: relative;
}

.three-scene {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.screen-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  max-width: 1600px;
  aspect-ratio: 4/3;
  z-index: 10;
  opacity: 95%;
}

.game-screen {
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  overflow: hidden;
  border: 2px solid #333;
}

.arcade-controls {
  position: fixed;
  cursor: move;
  user-select: none;
  z-index: 20;
  width: 450px;
  background: linear-gradient(145deg, #2a2a2a, #1a1a1a);
  border-radius: 20px;
  border: 3px solid #444;
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.5),
    inset 0 2px 5px rgba(255, 255, 255, 0.1),
    inset 0 -2px 5px rgba(0, 0, 0, 0.5);
  padding: 20px;
  transform: translateX(0);
  transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  will-change: transform;
  backface-visibility: hidden;
  transform-style: preserve-3d;
}

.arcade-controls.stored {
  transform: translateX(calc(100% - 60px));
  transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

/* 움직일 때 잔상 효과 */
.arcade-controls:active {
  transition: transform 0.1s linear;
  animation: moveBlur 0.3s ease-out;
}

@keyframes moveBlur {
  0% {
    filter: blur(0);
  }
  50% {
    filter: blur(3px);
    opacity: 0.8;
  }
  100% {
    filter: blur(0);
  }
}

.store-button {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  z-index: 22;
}

.restore-button {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 150px;
  background: #2a2a2a;
  border: 2px solid #444;
  border-radius: 10px 0 0 10px;
  color: white;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  z-index: 1000;
  box-shadow: 
    -5px 0 15px rgba(0, 0, 0, 0.3),
    inset 0 2px 5px rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
  animation: neonPulse 2s infinite;
}

.restore-button:hover {
  background: #333;
  width: 55px;
  right: 15px;
}

.restore-button:active {
  transform: translateY(-50%) scale(0.95);
}

.restore-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, transparent 0%, rgba(255, 255, 255, 0.1) 50%, transparent 100%);
  border-radius: 10px 0 0 10px;
  pointer-events: none;
}

.restore-button i {
  font-size: 1.2em;
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.restore-button span {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  transform: rotate(180deg);
  font-size: 16px;
  letter-spacing: 2px;
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

@keyframes neonPulse {
  0%, 100% {
    box-shadow: 
      -5px 0 15px rgba(0, 0, 0, 0.3),
      inset 0 2px 5px rgba(255, 255, 255, 0.1),
      0 0 5px rgba(255, 255, 255, 0.5);
  }
  50% {
    box-shadow: 
      -5px 0 15px rgba(0, 0, 0, 0.3),
      inset 0 2px 5px rgba(255, 255, 255, 0.1),
      0 0 20px rgba(255, 255, 255, 0.8);
  }
}

.controller-design {
  background: #222;
  border-radius: 15px;
  padding: 15px;
  border: 2px solid #555;
}

.controller-header {
  background: #1a1a1a;
  padding: 10px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
}

.controller-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  padding: 20px 10px;
}

.joystick-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.joystick {
  width: 120px;
  height: 120px;
  background: linear-gradient(145deg, #303030, #404040);
  border-radius: 50%;
  position: relative;
  box-shadow: 
    0 5px 15px rgba(0,0,0,0.3),
    inset 0 2px 5px rgba(255,255,255,0.1);
  display: flex;
  justify-content: center;
  align-items: center;
}

.home-button {
  width: 70px;
  height: 70px;
  background: linear-gradient(145deg, #ff4d4d, #cc0000);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-decoration: none;
  font-weight: bold;
  box-shadow: 
    0 4px 0 #8b0000,
    0 5px 15px rgba(0,0,0,0.3);
  transition: all 0.2s ease;
  will-change: transform;
}

.home-button:active {
  transform: translateY(4px);
  box-shadow: 
    0 0 0 #8b0000,
    0 2px 5px rgba(0,0,0,0.3);
}

.button-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  padding: 15px;
  background: #1a1a1a;
  border-radius: 20px;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
}

.arcade-button {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  color: white;
  font-weight: bold;
  text-align: center;
  transition: all 0.2s ease;
  border: none;
  position: relative;
  margin: 0 auto;
  will-change: transform;
}

.inventory {
  background: linear-gradient(145deg, #4d94ff, #0052cc);
  box-shadow: 
    0 4px 0 #003380,
    0 5px 15px rgba(0,0,0,0.3);
}

.training {
  background: linear-gradient(145deg, #66cc66, #2d862d);
  box-shadow: 
    0 4px 0 #1f5c1f,
    0 5px 15px rgba(0,0,0,0.3);
}

.quest {
  background: linear-gradient(145deg, #ffcc00, #cc9900);
  box-shadow: 
    0 4px 0 #806000,
    0 5px 15px rgba(0,0,0,0.3);
}

.shop {
  background: linear-gradient(145deg, #ff66ff, #cc00cc);
  box-shadow: 
    0 4px 0 #800080,
    0 5px 15px rgba(0,0,0,0.3);
}

.arcade-button:active {
  transform: translateY(4px);
  box-shadow: 
    0 0 0 #222,
    0 2px 5px rgba(0,0,0,0.3);
}

.button-label {
  font-size: 0.85em;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.led-light {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #f00;
  animation: blink 2s infinite;
}

.brand-text {
  font-size: 0.9em;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.controller-footer {
  padding: 10px;
  text-align: center;
}

.footer-line {
  height: 2px;
  background: linear-gradient(to right, transparent, #444, transparent);
  margin-bottom: 5px;
}

.footer-text {
  font-size: 0.7em;
  color: #666;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

@media (max-width: 768px) {
  .arcade-controls {
    width: 320px;
    padding: 15px;
  }

  .controller-body {
    flex-direction: column;
    gap: 15px;
  }

  .joystick {
    width: 100px;
    height: 100px;
  }

  .home-button {
    width: 60px;
    height: 60px;
  }

  .arcade-button {
    width: 55px;
    height: 55px;
  }

  .button-label {
    font-size: 0.75em;
  }

  .restore-button {
    height: 120px;
  }
}

/* 활성화된 버튼 효과 */
.arcade-button.router-link-active,
.home-button.router-link-active {
  filter: brightness(1.3);
  animation: activeGlow 1.5s ease-in-out infinite alternate;
}

@keyframes activeGlow {
  from {
    box-shadow: 0 4px 0 var(--button-shadow-color),
                0 0 10px rgba(255, 255, 255, 0.5);
  }
  to {
    box-shadow: 0 4px 0 var(--button-shadow-color),
                0 0 25px rgba(255, 255, 255, 0.8);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.gamepad-icon {
  height: 40px;
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  animation: iconGlow 1.5s ease-in-out infinite alternate;
}

.gamepad-icon i {
  font-size: 1.5em;
}

@keyframes iconGlow {
  from {
    filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.5));
    transform: scale(1);
  }
  to {
    filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.8));
    transform: scale(1.1);
  }
}

@keyframes neonPulse {
  0%, 100% {
    box-shadow: 
      -5px 0 15px rgba(0, 0, 0, 0.3),
      inset 0 2px 5px rgba(255, 255, 255, 0.1),
      0 0 10px rgba(255, 255, 255, 0.5);
  }
  50% {
    box-shadow: 
      -5px 0 15px rgba(0, 0, 0, 0.3),
      inset 0 2px 5px rgba(255, 255, 255, 0.1),
      0 0 25px rgba(255, 255, 255, 0.8);
  }
}
</style>