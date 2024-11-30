<template>
  <div class="start-screen">
    <!-- 돈비 효과 -->
    <div class="money-rain"></div>
    <!-- 배경 효과 -->
    <div class="stars"></div>
    <div class="twinkling"></div>
    <div class="gradient-overlay"></div>
    
    <!-- 로고 섹션 -->
    <div class="logo-section">
      <div class="neon-border">
        <img src="/wg_line.png" alt="WEALTH GAME" class="logo-image" />
        <div class="logo-glow"></div>
      </div>
    </div>

    <!-- 모토 섹션 -->
    <div class="motto-section">
      <div class="cyber-frame">
        <div class="quote-mark left">❝</div>
        <h3 class="motto">
          <div class="glitch-text">인생의 재테크는 하나의 🎮 게임과 같습니다.</div>
          <div class="glitch-text">전략을 세우고 📈</div>
          <div class="glitch-text">레벨을 올리며 ⭐</div>
          <div class="glitch-text">새로운 스테이지를 클리어하듯 🏁</div>
          <div class="glitch-text">성장해나가는 과정입니다.</div>
        </h3>
        <div class="quote-mark right">❞</div>
      </div>
    </div>
    
    <div class="slogan-container" @click="refreshPage">
    <div class="cosmic-slogan" data-text="PLAY SMART">PLAY SMART</div>
    <div class="cosmic-slogan" data-text="GROW WEALTHY">GROW WEALTHY</div>
  </div>

  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';

onMounted(() => {
  startMoneyRain();
});

function startMoneyRain() {
  const container = document.querySelector('.money-rain');
  const symbols = ['💵', '💰', '💎', '⭐', '💫', '✨'];
  let rainInterval;

  const createMoney = () => {
    const money = document.createElement('div');
    money.className = 'money-symbol';
    money.innerHTML = symbols[Math.floor(Math.random() * symbols.length)];
    money.style.left = `${Math.random() * 100}%`;
    money.style.animationDuration = `${Math.random() * 3 + 2}s`;
    money.style.opacity = Math.random() * 0.7 + 0.3;
    money.style.transform = `scale(${Math.random() * 0.5 + 0.5})`;
    container.appendChild(money);

    money.addEventListener('animationend', () => {
      container.removeChild(money);
    });
  };

  // Initial money symbols
  for (let i = 0; i < 10; i++) {
    setTimeout(createMoney, Math.random() * 2000);
  }

  rainInterval = setInterval(createMoney, 300);

  onUnmounted(() => {
    clearInterval(rainInterval);
  });
}

const reload = () => window.location.reload();

const refreshPage = () => {
  window.location.reload()
}

function createMoneyBurst() {
 const container = document.querySelector('.money-rain');
 const burstCount = 20; // 한번에 생성할 이모지 수

 for (let i = 0; i < burstCount; i++) {
   const money = document.createElement('div');
   money.className = 'money-burst';
   money.innerHTML = symbols[Math.floor(Math.random() * symbols.length)];
   money.style.left = `50%`; // 이미지 중앙에서 시작
   money.style.top = `30%`; // 이미지 위치에 맞춰 조정
   money.style.animationDuration = `${Math.random() * 2 + 1}s`;
   container.appendChild(money);

   money.addEventListener('animationend', () => {
     container.removeChild(money);
   });
 }
}
</script>

<style scoped>


.start-screen {
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #13131f 0%, #20202f 100%);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  padding: 2rem;
}

/* 배경 효과 */
.stars {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(125deg, #000000 0%, #1a1a2e 100%);
}

.twinkling {
  position: absolute;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(white 1px, transparent 1px) 0 0 / 50px 50px,
    radial-gradient(white 1px, transparent 1px) 25px 25px / 50px 50px;
  opacity: 0.1;
  animation: twinkle 20s linear infinite;
}

.gradient-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.8) 100%);
  pointer-events: none;
}

/* 로고 섹션 */
.logo-section {
 position: relative;
 z-index: 2;
 transform: scale(3); 
 margin-top: 5vh;
}


.neon-border {
 padding: 2rem;
 border-radius: 10px;
 position: relative;
}

.neon-border::before {
 content: '';
 position: absolute;
 top: -2px;
 left: -2px;
 right: -2px;
 bottom: -2px;
 border-radius: 50px;
 z-index: -1;
 filter: blur(5px);
}


.logo-image {
  max-width: 1000px;
  height: auto;
  filter: drop-shadow(0 0 20px rgba(255,255,255,0.5));
  animation: logoFloat 3s ease-in-out infinite;
}

/* 모토 섹션 */
.motto-section {
  position: relative;
  z-index: 2;
  width: 80%;
  max-width: 800px;
}

.cyber-frame {
  padding: 2rem;
  background: rgba(255,255,255,0.05);
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  position: relative;
  margin-bottom: 25rem;
}

.quote-mark {
  font-size: 4rem;
  color: rgba(255,255,255,0.2);
  position: absolute;
}

.quote-mark.left {
  top: 0;
  left: 1rem;
}

.quote-mark.right {
  bottom: 0;
  right: 1rem;
}

.motto {
  font-size: 1.4rem;
  line-height: 2;
  color: #fff;
  text-align: center;
}

.glitch-text {
  position: relative;
  animation: glitchText 3s infinite;
  margin: 1rem 0;
}

/* 슬로건 섹션 */
.slogan-container {
 position: fixed;
 bottom: 4vh; /* 위치 상향 조정 */
 left: 50%;
 transform: translateX(-50%);
 text-align: center;
 z-index: 2;
}

.cosmic-slogan {
 font-size: 3.5rem; /* 크기 증가 */
 font-weight: 800;
 letter-spacing: 4px;
 margin: 1rem 0;
 background: linear-gradient(45deg, #00ffff, #4169e1, #9400d3);
 -webkit-background-clip: text;
 -webkit-text-fill-color: transparent;
 text-transform: uppercase;
 transition: all 0.3s ease;
 cursor: pointer;
}

/* 컨테이너에 호버 효과 적용 */
.slogan-container:hover .cosmic-slogan {
 transform: scale(1.1);
 letter-spacing: 8px;
 text-shadow: 
   0 0 10px rgba(65, 105, 225, 0.8),
   0 0 20px rgba(148, 0, 211, 0.8),
   0 0 30px rgba(0, 255, 255, 0.8);
 animation: cosmicPulse 1s ease infinite;
}

@keyframes cosmicPulse {
  0%, 100% { filter: brightness(1); }
  50% { filter: brightness(1.5); }
}

.neon-text-container {
  text-align: center;
}

.neon-text {
  font-size: 3.5rem;
  font-weight: 900;
  text-decoration: none;
  text-transform: uppercase;
  display: block;
  margin: 1rem 0;
  position: relative;
  transition: all 0.3s ease;
}

.play {
  color: #ff3366;
  text-shadow: 
    0 0 5px #ff3366,
    0 0 10px #ff3366,
    0 0 20px #ff3366;
}

.grow {
  color: #33ff99;
  text-shadow: 
    0 0 5px #33ff99,
    0 0 10px #33ff99,
    0 0 20px #33ff99;
}

/* 돈비 효과 */
.money-rain {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.money-symbol {
  position: absolute;
  top: -20px;
  font-size: 2rem;
  animation: moneyFall linear forwards;
}

/* 애니메이션 */
@keyframes moneyFall {
  to {
    transform: translateY(100vh) rotate(360deg);
  }
}

@keyframes stars {
  from { background-position: 0 0; }
  to { background-position: -10000px 5000px; }
}

@keyframes twinkle {
  from { transform: translateY(0); }
  to { transform: translateY(-50px); }
}

@keyframes borderRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes logoFloat {
  0% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0); }
}

@keyframes glitchText {
  0% { transform: translateX(0); }
  2% { transform: translateX(3px); }
  4% { transform: translateX(-3px); }
  6% { transform: translateX(0); }
  100% { transform: translateX(0); }
}



</style>