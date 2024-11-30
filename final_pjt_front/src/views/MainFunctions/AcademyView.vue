<template>
  <div class="game-screen">
    <div class="stars"></div>
    <div class="twinkling"></div>
    
    <div class="game-header">
      <div class="neon-text">TRAINING ZONE</div>
    </div>
    
    <div class="game-content">
      <template v-if="isVisible">
        <div class="entrance-overlay">
          <div class="arcade-frame">
            <div class="scanner-line"></div>
            <div class="glitch-effect" data-text="READY?">READY?</div>
            <button 
              class="btn arcade-btn entrance-btn"
              @click="startTraining"
            >
              <span class="btn-content">
                <span class="entrance-text">START</span>
                <span class="btn-glitch"></span>
              </span>
            </button>
            
            <div class="arcade-controls-hint">
              <div class="control-key">↑</div>
              <div class="control-key">←</div>
              <div class="control-key">↓</div>
              <div class="control-key">→</div>
            </div>

            <div class="insert-coin">INSERT COIN - PRESS START</div>
          </div>
        </div>
      </template>
      <RouterView v-else class="router-view" />

      <div class="radar">
        <div class="radar-beam"></div>
        <div class="radar-center"></div>
      </div>

      <div class="status-bar">
        <div class="status-item">
          <span class="label">POWER</span>
          <div class="progress-bar">
            <div class="progress-fill"></div>
          </div>
        </div>
        <div class="status-item">
          <span class="label">SHIELD</span>
          <div class="progress-bar">
            <div class="progress-fill shield-fill"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterView, useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';

const router = useRouter();
const isVisible = ref(true);
let hoverSound;

onMounted(() => {
  // 효과음 초기화
  hoverSound = new Audio('/hover.mp3'); // 효과음 파일 필요
});

const startTraining = async () => {
  isVisible.value = false;
  await router.push({ name: 'AcademyList' });
};

</script>

<style scoped>
.game-screen {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  color: #fff;
  background: #000;
  position: relative;
  overflow: hidden;
}

/* 우주 배경 효과 */
.stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000 url('/stars.png') repeat;
  z-index: 0;
}

.twinkling {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: transparent url('/twinkling.png') repeat;
  animation: move-twinkle 200s linear infinite;
  opacity: 0.5;
  z-index: 1;
}

@keyframes move-twinkle {
  from { background-position: 0 0; }
  to { background-position: -10000px 5000px; }
}

.game-header {
  position: relative;
  z-index: 2;
  width: 100%;
  text-align: center;
  padding: 20px 0;
  background: linear-gradient(to bottom, 
    rgba(0,0,0,0.8) 0%,
    rgba(0,0,0,0) 100%);
}

.neon-text {
  font-size: 3rem;
  font-weight: bold;
  color: #f0f;
  text-shadow: 
    0 0 2px #f0f,
    0 0 4px #f0f,
    0 0 8px #f0f;
  animation: neon-pulse 1.5s ease-in-out infinite alternate;
  font-family: 'Press Start 2P', cursive;
}

@keyframes neon-pulse {
  from { 
    text-shadow: 
      0 0 2px #f0f,
      0 0 4px #f0f,
      0 0 8px #f0f;
  }
  to { 
    text-shadow: 
      0 0 3px #f0f,
      0 0 6px #f0f,
      0 0 8px #f0f,
      0 0 2px #f0f;
  }
}

.game-content {
  width: 100%;
  height: calc(100% - 100px);
  position: relative;
  z-index: 2;
}

.router-view {
  height: 100%;
  overflow-y: auto;
}

.entrance-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.7);
}

.arcade-frame {
  position: relative;
  background: rgba(138, 43, 226, 0.1);
  border: 4px solid #8a2be2;
  border-radius: 20px;
  padding: 80px;
  width: 80%;
  max-width: 800px;
  aspect-ratio: 16/9;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 
    0 0 20px #8a2be2,
    inset 0 0 40px rgba(138, 43, 226, 0.5);
}

.scanner-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: rgba(138, 43, 226, 0.5);
  animation: scan 2s linear infinite;
}

@keyframes scan {
  0% { top: 0; opacity: 0; }
  50% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}

.glitch-effect {
  font-size: 5rem;
  font-weight: bold;
  color: #f0f;
  text-shadow: 2px 2px #0ff;
  margin-bottom: 50px;
  position: relative;
  font-family: 'Press Start 2P', cursive;
}

.arcade-btn {
  padding: 25px 60px;
  font-size: 2.5rem;
  background: none;
  border: 2px solid #f0f;
  color: #f0f;
  font-weight: bold;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  margin: 30px 0;
  font-family: 'Press Start 2P', cursive;
}

.arcade-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 0, 255, 0.4),
    transparent
  );
  transition: 0.5s;
}

.arcade-btn:hover::before {
  left: 100%;
}

.arcade-btn:hover {
  background: rgba(255, 0, 255, 0.1);
  box-shadow: 0 0 20px #f0f;
  transform: scale(1.05);
}

.arcade-controls-hint {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 50px;
}

.control-key {
  width: 60px;
  height: 60px;
  border: 2px solid #f0f;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  color: #f0f;
  background: rgba(255, 0, 255, 0.1);
  box-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
}

.insert-coin {
  position: absolute;
  bottom: 20px;
  color: #f0f;
  font-size: 1rem;
  font-family: 'Press Start 2P', cursive;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.radar {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 150px;
  height: 150px;
  border: 2px solid #f0f;
  border-radius: 50%;
  overflow: hidden;
  z-index: 3;
}

.radar-beam {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent 50%, rgba(255, 0, 255, 0.5) 100%);
  animation: radar-scan 4s linear infinite;
  transform-origin: center;
}

.radar-center {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 10px;
  height: 10px;
  background: #f0f;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 10px #f0f;
}

@keyframes radar-scan {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.status-bar {
  position: absolute;
  top: 20px;
  left: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 3;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-item .label {
  width: 70px;
  color: #f0f;
  font-size: 0.9rem;
  font-family: 'Press Start 2P', cursive;
}

.progress-bar {
  width: 150px;
  height: 10px;
  background: rgba(255, 0, 255, 0.2);
  border: 1px solid #f0f;
}

.progress-fill {
  width: 75%;
  height: 100%;
  background: #f0f;
  animation: power-fluctuate 3s ease-in-out infinite;
}

.shield-fill {
  animation: shield-fluctuate 2.5s ease-in-out infinite;
}

@keyframes power-fluctuate {
  0% { width: 75%; }
  50% { width: 85%; }
  100% { width: 75%; }
}

@keyframes shield-fluctuate {
  0% { width: 60%; }
  50% { width: 70%; }
  100% { width: 60%; }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .arcade-frame {
    padding: 40px;
    width: 90%;
  }

  .glitch-effect {
    font-size: 3rem;
  }

  .arcade-btn {
    padding: 15px 30px;
    font-size: 1.8rem;
  }

  .control-key {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }

  .neon-text {
    font-size: 2rem;
  }

  .radar {
    width: 100px;
    height: 100px;
  }

  .status-bar {
    transform: scale(0.8);
    transform-origin: top left;
  }
}
</style>