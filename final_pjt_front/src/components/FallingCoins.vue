<template>
    <div class="falling-coins-container">
      <TransitionGroup name="coin">
        <div
          v-for="coin in coins"
          :key="coin.id"
          class="coin"
          :style="{
            left: `${coin.left}%`,
            animationDuration: `${coin.duration}s`,
            opacity: coin.opacity,
            width: `${coin.size}px`,
            height: `${coin.size}px`
          }"
          @animationend="removeCoin(coin.id)"
          :data-text="'coin'"
        />
      </TransitionGroup>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  
  const coins = ref([]);
  let coinId = 0;
  let intervalId = null;
  
  const createCoin = () => {
    const coin = {
      id: coinId++,
      left: Math.random() * 100,
      duration: Math.random() * 3 + 2,
      opacity: Math.random() * 0.7 + 0.3,
      size: Math.random() * 20 + 10
    };
    coins.value.push(coin);
  };
  
  const removeCoin = (id) => {
    coins.value = coins.value.filter(coin => coin.id !== id);
  };
  
  onMounted(() => {
    // Initial coins
    for (let i = 0; i < 20; i++) {
      setTimeout(createCoin, Math.random() * 2000);
    }
    // Continuous coin creation
    intervalId = setInterval(createCoin, 300);
  });
  
  onUnmounted(() => {
    clearInterval(intervalId);
  });
  </script>
  
  <style scoped>
  .falling-coins-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
    overflow: hidden;
  }
  
  .coin {
    position: absolute;
    top: -20px;
    background: linear-gradient(45deg, #ffd700, #ffb900);
    border-radius: 50%;
    animation: fall linear forwards;
  }
  
  @keyframes fall {
    to {
      transform: translateY(100vh) rotate(360deg);
    }
  }
  
  .coin-enter-active {
    transition: opacity 0.3s;
  }
  
  .coin-leave-active {
    transition: opacity 0.3s;
  }
  
  .coin-enter-from,
  .coin-leave-to {
    opacity: 0;
  }
  </style>