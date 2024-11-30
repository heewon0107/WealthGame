<template>
  <div class="result-container fail">
    <div class="result-content">
      <div class="result-animation">
        <div class="fail-icon">
          <i class="fas fa-exclamation-triangle"></i>
        </div>
      </div>
      <h2 class="result-title">QUEST FAILED</h2>
      <div class="fail-message">
        아쉽게도 도전에 실패했습니다.<br>
        다시 한번 도전해보세요!
      </div>
      <button @click="$emit('close')" class="close-btn">
        <span>RETRY</span>
        <i class="fas fa-redo"></i>
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
  background: linear-gradient(135deg, rgba(255, 0, 0, 0.2), rgba(128, 0, 0, 0.2));
}

.result-content {
  text-align: center;
  animation: fadeIn 0.5s ease-out;
}

.result-animation {
  margin-bottom: 2rem;
}

.fail-icon {
  font-size: 5rem;
  color: #ff4444;
  animation: failShake 0.5s ease-in-out;
}

.result-title {
  font-size: 3rem;
  color: #ff4444;
  font-family: 'DungGeunMo';
  text-shadow: 
    0 0 10px #ff4444,
    0 0 20px #ff4444;
  margin-bottom: 1rem;
  animation: glowTextFail 2s infinite;
}

.fail-message {
  font-size: 1.5rem;
  color: #fff;
  margin-bottom: 2rem;
  font-family: 'DungGeunMo';
  line-height: 1.6;
  opacity: 0;
  animation: slideUp 0.5s ease-out forwards;
  animation-delay: 0.3s;
}

.close-btn {
  background: linear-gradient(45deg, #ff4444, #cc0000);
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
  box-shadow: 0 0 20px rgba(255, 68, 68, 0.5);
}

@keyframes failShake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-10px); }
  40% { transform: translateX(10px); }
  60% { transform: translateX(-10px); }
  80% { transform: translateX(10px); }
}

@keyframes glowTextFail {
  0%, 100% { text-shadow: 0 0 10px #ff4444, 0 0 20px #ff4444; }
  50% { text-shadow: 0 0 20px #ff4444, 0 0 40px #ff4444; }
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

@media (max-width: 768px) {
  .result-title {
    font-size: 2rem;
  }

  .fail-message {
    font-size: 1.2rem;
  }

  .close-btn {
    font-size: 1rem;
    padding: 0.8rem 1.6rem;
  }
}
</style>