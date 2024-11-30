<template>
  <div class="credit-container" @click="showEnding">
    <div class="retro-overlay"></div>
    <div class="scan-lines"></div>
    
    <div class="credit-content">
      <h2 class="credit-title credit-text">🏆 CONGRATULATIONS 🏆</h2>
      
      <h4 class="credit-text main-message">
        축하드립니다. 당신은 WEALTH GAME의<br>모든 퀘스트를 클리어했습니다.
      </h4>
      
      <div class="divider credit-text">* * * * *</div>
      
      <p class="credit-text message">
        인생은 게임과도 같습니다.<br>
        매 순간마다 새로운 선택지를 골라가며<br>
        미래를 개척해 가야합니다.
      </p>
      
      <p class="credit-text message">
        여러분들의 행복한 미래,<br>
        부유하진 않더라도 안정적인 삶을 위해<br>
        WEALTH GAME에서 길잡이를 드립니다.
      </p>
      
      <div class="divider credit-text">* * * * *</div>
      
      <h4 class="credit-text ending-message">
        <span class="blink">해당 화면을 클릭하면 엔딩화면이 나옵니다.</span>
      </h4>
    </div>
    
    <div class="credit-decoration top-left"></div>
    <div class="credit-decoration top-right"></div>
    <div class="credit-decoration bottom-left"></div>
    <div class="credit-decoration bottom-right"></div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const showEnding = () => {
  router.push({name : 'Ending'});
}
</script>

<style scoped>
.credit-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #0a0a0a;
  color: #FFD700;
  padding: 20px;
  text-align: center;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  font-family: 'DungGeunMo', sans-serif;
}

.retro-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    linear-gradient(
      45deg,
      rgba(255, 215, 0, 0.1) 25%,
      transparent 25%,
      transparent 75%,
      rgba(255, 215, 0, 0.1) 75%
    );
  background-size: 4px 4px;
  pointer-events: none;
}

.scan-lines {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.03) 50%,
    rgba(0, 0, 0, 0.03) 50%
  );
  background-size: 100% 4px;
  pointer-events: none;
}

.credit-content {
  position: relative;
  z-index: 2;
  max-width: 1000px; /* 최대 너비 증가 */
  padding: 2rem;
}

.credit-text {
  opacity: 0;
  animation: slideIn 3s forwards;
  margin: 30px 0; /* 여백 증가 */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.credit-title {
  font-size: 4em; /* 타이틀 크기 증가 */
  color: #FFD700;
  text-shadow: 0 0 10px #FFD700;
  animation: glowingGold 2s infinite, slideIn 3s forwards;
  margin-bottom: 50px; /* 하단 여백 증가 */
}

.main-message {
  font-size: 2.2em; /* 메인 메시지 크기 증가 */
  color: #F0F0F0;
  animation-delay: 0.5s;
  line-height: 1.4;
  margin-bottom: 40px;
}

.message {
  font-size: 1.8em; /* 일반 메시지 크기 증가 */
  color: #E0E0E0;
  line-height: 1.8;
  animation-delay: 1.5s;
  margin: 40px 0; /* 여백 증가 */
}

.divider {
  color: #FFD700;
  letter-spacing: 15px; /* 구분선 간격 증가 */
  font-size: 2em; /* 구분선 크기 증가 */
  animation-delay: 1s;
  margin: 40px 0; /* 여백 증가 */
}

.ending-message {
  font-size: 2em; /* 엔딩 메시지 크기 증가 */
  color: #FFD700;
  animation-delay: 2.5s;
  margin-top: 50px; /* 상단 여백 증가 */
}

.credit-decoration {
  position: absolute;
  width: 150px; /* 장식 크기 증가 */
  height: 150px;
  border: 3px solid #FFD700; /* 테두리 두께 증가 */
  opacity: 0.5;
}

.top-left {
  top: 20px;
  left: 20px;
  border-right: none;
  border-bottom: none;
}

.top-right {
  top: 20px;
  right: 20px;
  border-left: none;
  border-bottom: none;
}

.bottom-left {
  bottom: 20px;
  left: 20px;
  border-right: none;
  border-top: none;
}

.bottom-right {
  bottom: 20px;
  right: 20px;
  border-left: none;
  border-top: none;
}

.blink {
  animation: blink 1s infinite;
}

@keyframes slideIn {
  0% {
    transform: translateY(-50px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes glowingGold {
  0% {
    text-shadow: 0 0 10px #FFD700;
  }
  50% {
    text-shadow: 0 0 20px #FFD700, 0 0 30px #FFD700;
  }
  100% {
    text-shadow: 0 0 10px #FFD700;
  }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.credit-container:hover .credit-decoration {
  animation: borderGlow 1.5s infinite;
}

@keyframes borderGlow {
  0% {
    box-shadow: 0 0 5px #FFD700;
  }
  50% {
    box-shadow: 0 0 20px #FFD700;
  }
  100% {
    box-shadow: 0 0 5px #FFD700;
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .credit-title {
    font-size: 2.8em;
  }
  
  .main-message {
    font-size: 1.8em;
  }
  
  .message {
    font-size: 1.4em;
  }
  
  .ending-message {
    font-size: 1.6em;
  }
  
  .credit-decoration {
    width: 80px;
    height: 80px;
  }
  
  .divider {
    font-size: 1.5em;
    letter-spacing: 10px;
  }
}
</style>