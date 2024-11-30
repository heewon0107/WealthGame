<template>
  <div class="arcade-profile-container">
    <!-- 배경 효과 -->
    <div class="stars"></div>
    <div class="twinkling"></div>
    
    <div class="profile-content">
      <!-- 네비게이션 섹션 -->
      <div class="navigation-section">
        <div class="nav-buttons">
          <RouterLink 
            :to="{name: 'ProfileManagement'}" 
            class="cyber-button"
          >
            <div class="button-content">
              <i class="fas fa-chart-bar"></i>
              <span>STATS</span>
            </div>
            <div class="button-glow"></div>
          </RouterLink>
          
          <RouterLink 
            :to="{name: 'ProfileSaveItem'}" 
            class="cyber-button"
          >
            <div class="button-content">
              <i class="fas fa-box"></i>
              <span>INVENTORY</span>
            </div>
            <div class="button-glow"></div>
          </RouterLink>
          
          <RouterLink 
            :to="{name: 'ProfileRecommendItem'}" 
            class="cyber-button"
          >
            <div class="button-content">
              <i class="fas fa-gift"></i>
              <span>RECOMMEND ITEMS</span>
            </div>
            <div class="button-glow"></div>
          </RouterLink>
        </div>
      </div>
      
      <!-- 라우터 뷰 컨테이너 -->
      <div class="arcade-frame">
        <div class="screen-overlay"></div>
        <div class="content-area">
          <RouterView/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router';
import { onMounted } from 'vue';

const router = useRouter()

onMounted(() => {
  // 컴포넌트가 마운트되면 바로 STATS 페이지로 리다이렉션
  if (router.currentRoute.value.name === 'ProfileView') {
    router.push({ name: 'ProfileManagement' })
  }
})
</script>

<style scoped>
.arcade-profile-container {
  min-height: 100vh;
  background: #000;
  position: relative;
  overflow: hidden;
  padding: 20px;
}

/* 배경 효과 */
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

.profile-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 네비게이션 섹션 */
.navigation-section {
  position: sticky;
  top: 0px;
  z-index: 100;
  backdrop-filter: blur(5px);
  padding: 40px 0px;
}

.nav-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.cyber-button {
  position: relative;
  padding: 15px 30px;
  background: rgba(255, 0, 255, 0.1);
  border: 2px solid #f0f;
  border-radius: 5px;
  color: #fff;
  text-decoration: none;
  overflow: hidden;
  transition: all 0.3s ease;
  min-width: 180px;
}

.button-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  font-family: 'DungGeunMo';
}

.button-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 0, 255, 0.3),
    transparent
  );
  animation: button-shine 3s linear infinite;
}

.cyber-button:hover {
  background: rgba(255, 0, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 
    0 0 10px rgba(255, 0, 255, 0.5),
    0 0 20px rgba(255, 0, 255, 0.3),
    0 0 30px rgba(255, 0, 255, 0.1);
}

.cyber-button.router-link-active {
  background: rgba(255, 0, 255, 0.3);
  box-shadow: 
    0 0 15px rgba(255, 0, 255, 0.6),
    0 0 30px rgba(255, 0, 255, 0.4),
    0 0 45px rgba(255, 0, 255, 0.2);
  border-color: #ff00ff;
}

/* 아케이드 프레임 */
.arcade-frame {
  width: 100%;
  height: calc(100vh - 150px);
  background: rgba(255, 0, 255, 0.1);
  border: 4px solid #f0f;
  border-radius: 20px;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 0 20px #f0f,
    inset 0 0 40px rgba(255, 0, 255, 0.3);
}

.screen-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    transparent,
    rgba(255, 0, 255, 0.1) 50%,
    transparent
  );
  animation: scan-line 8s linear infinite;
  pointer-events: none;
}

.content-area {
  width: 100%;
  height: 100%;
  padding: 40px;
  overflow-y: auto;
  position: relative;
  z-index: 2;
}

.content-area::-webkit-scrollbar {
  width: 10px;
}

.content-area::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 5px;
}

.content-area::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 5px;
  box-shadow: 0 0 10px #f0f;
}

/* 애니메이션 */
@keyframes button-shine {
  0% { left: -100%; }
  50% { left: 100%; }
  100% { left: 100%; }
}

@keyframes scan-line {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

@keyframes move-twinkle {
  from { background-position: 0 0; }
  to { background-position: -10000px 5000px; }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .arcade-profile-container {
    padding: 10px;
  }

  .nav-buttons {
    flex-direction: column;
    align-items: center;
  }

  .cyber-button {
    width: 90%;
    padding: 12px 20px;
    min-width: unset;
  }

  .arcade-frame {
    height: calc(100vh - 250px);
  }
}
</style>