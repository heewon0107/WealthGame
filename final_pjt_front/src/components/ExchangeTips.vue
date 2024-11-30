<template>
  <div class="tips-container">
    <div class="cyber-sign">
      <div class="sign-content">
        <div class="sign-header">실시간 환율 투자 팁</div>
        <div class="sign-body">
          <div class="tip-scroll">
            <div class="tip-text">
              단기 투자 → 일일 & 주간 변동 체크하고 뉴스 확인하기
            </div>
            <div class="tip-text">
              장기 투자 → 월별 흐름 분석하고 경제 지표 살펴보기
            </div>
            <div class="tip-text">
              투자 원칙 → 소액부터 시작! 시장 동향 파악! 리스크 관리!
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 필요한 경우 여기에 로직 추가
</script>

<style scoped>
.tips-container {
  width: 100%;
  margin-bottom: 2rem;
  perspective: 1000px;
}

.cyber-sign {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #f0f;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
  transform: rotateX(10deg);
  transform-style: preserve-3d;
}

.sign-content {
  background: rgba(255, 0, 255, 0.05);
  padding: 1rem;
  border-radius: 4px;
}

.sign-header {
  color: #f0f;
  font-size: 1.5rem;
  text-align: center;
  margin-bottom: 1rem;
  font-family: 'DungGeunMo', monospace;
  text-shadow: 
    0 0 5px #f0f,
    0 0 10px #f0f,
    0 0 15px #f0f;
  animation: glow 1.5s ease-in-out infinite alternate;
}

.sign-body {
  overflow: hidden;
}

.tip-scroll {
  animation: scrollTips 20s linear infinite;
}

.tip-text {
  color: #0ff;
  text-align: center;
  padding: 0.5rem;
  font-family: 'DungGeunMo', monospace;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
  margin: 0.5rem 0;
}

@keyframes glow {
  from {
    text-shadow: 
      0 0 5px #f0f,
      0 0 10px #f0f,
      0 0 15px #f0f;
  }
  to {
    text-shadow: 
      0 0 10px #f0f,
      0 0 20px #f0f,
      0 0 30px #f0f;
  }
}

@keyframes scrollTips {
  0% {
    transform: translateY(100%);
  }
  100% {
    transform: translateY(-100%);
  }
}

</style>