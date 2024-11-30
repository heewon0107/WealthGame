<template>
  <div class="result-container success">
    <div class="result-content">
      <div class="result-animation">
        <div class="success-icon">
          <i class="fas fa-crown"></i>
        </div>
      </div>
      <h2 class="result-title">LEVEL UP!</h2>
      <div class="success-message">
        새로운 티어로 성공적으로 전직했습니다!
      </div>
      <button @click="$emit('close')" class="close-btn">
        <span>CONTINUE</span>
        <i class="fas fa-arrow-right"></i>
      </button>
    </div>
  </div>
</template>

<style scoped>
.result-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(255, 0, 255, 0.2), rgba(0, 255, 255, 0.2));
}

.result-content {
  text-align: center;
  animation: fadeIn 0.5s ease-out;
}

.result-animation {
  margin-bottom: 2rem;
}

.success-icon {
  font-size: 5rem;
  color: #ffd700;
  animation: successPulse 2s infinite;
}

.result-title {
  font-size: 3rem;
  color: #ffd700;
  font-family: 'DungGeunMo';
  text-shadow: 
    0 0 10px #ffd700,
    0 0 20px #ffd700;
  margin-bottom: 1rem;
  animation: glowText 2s infinite;
}

.success-message {
  font-size: 1.5rem;
  color: #fff;
  margin-bottom: 2rem;
  font-family: 'DungGeunMo';
  opacity: 0;
  animation: slideUp 0.5s ease-out forwards;
  animation-delay: 0.3s;
}

.close-btn {
  background: linear-gradient(45deg, #ffd700, #ffa500);
  border: none;
  padding: 1rem 2rem;
  border-radius: 50px;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  font-family: 'DungGeunMo';
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 auto;
  transition: all 0.3s ease;
  opacity: 0;
  animation: slideUp 0.5s ease-out forwards;
  animation-delay: 0.6s;
}

.close-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}

@keyframes successPulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

@keyframes glowText {
  0%, 100% { text-shadow: 0 0 10px #ffd700, 0 0 20px #ffd700; }
  50% { text-shadow: 0 0 20px #ffd700, 0 0 40px #ffd700; }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>