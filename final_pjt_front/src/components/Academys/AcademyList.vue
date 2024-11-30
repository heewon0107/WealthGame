<template>
  <div class="arcade-list-container">
    <!-- 카테고리 네비게이션 버튼 -->
    <div class="category-container">
      <div class="nav-buttons">
        <button
          v-for="category in categories"
          :key="category"
          @click="selectedCategory = category"
          :class="['arcade-nav-button', { active: selectedCategory === category }]"
        >
          <span class="button-text">{{ category }}</span>
          <div class="button-glow"></div>
        </button>
      </div>
    </div>

    <!-- 문제 리스트 -->
    <div class="quest-container" v-if="filteredQuests">
      <div
        v-for="(questions, categoryName) in filteredQuests"
        :key="categoryName"
        :id="categoryName"
        class="category-section"
      >
        <h4 class="category-title">{{ categoryName }}</h4>
        <div class="questions-grid">
          <div
            v-for="(item, index) in questions"
            :key="item.id"
            class="question-item"
          >
            <div class="question-header">
              <span class="question-number">Q{{ index + 1 }}</span>
            </div>
            <p class="question-text">{{ item.question }}</p>
            <div v-if="item.choices" class="choices">
              <ul v-for="choice in parseChoices(item.choices)" :key="choice">
                {{ choice }}
              </ul>
            </div>
            <div class="answer-container">
              <p class="answer">A: {{ item.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="loading">
      <div class="loading-text">LOADING...</div>
      <div class="loading-bar"></div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed, onMounted } from 'vue';

const quests = ref([]);
const selectedCategory = ref(null);
const categories = ['예적금', '달러', '청약', '주식', '부동산'];

const parseChoices = (choicesString) => {
  if (!choicesString) return [];
  return choicesString
    .replace(/[\[\]']/g, '')
    .split(',')
    .map((choice) => choice.trim());
};

const filteredQuests = computed(() => {
  if (!quests.value.length) return null;

  if (!selectedCategory.value) {
    return quests.value.reduce((acc, quest) => {
      const categoryName = quest.category.name;
      if (!acc[categoryName]) {
        acc[categoryName] = [];
      }
      acc[categoryName].push(quest);
      return acc;
    }, {});
  }

  const filteredData = quests.value.filter(
    (quest) => quest.category.name === selectedCategory.value
  );

  return {
    [selectedCategory.value]: filteredData,
  };
});

onMounted(() => {
  axios
    .get('http://127.0.0.1:8000/quest/list/')
    .then((res) => {
      quests.value = res.data;
    })
    .catch((err) => {
      console.error(err);
    });
});
</script>

<style scoped>
.arcade-list-container {
  padding: 20px;
  color: #fff;
  height: 100%;
  overflow-y: auto;
  position: relative;
  margin-top: 60px;
}
.arcade-list-container::-webkit-scrollbar {
  width: 8px;
}
.arcade-list-container::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 10px;
}

.arcade-list-container::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 10px;
  box-shadow: 0 0 10px #f0f;
}

.arcade-list-container::-webkit-scrollbar-thumb:hover {
  background: #f0f;
  box-shadow: 0 0 15px #f0f;
}

.category-container {
  position: sticky;
  top: 0;
  z-index: 10;
  background: linear-gradient(to bottom, 
    rgba(0,0,0,0.9) 0%,
    rgba(0,0,0,0.8) 50%,
    rgba(0,0,0,0) 100%);
  padding: 20px 0;
}

.nav-buttons {
  padding: 70px;
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
}

.arcade-nav-button {
  position: relative;
  padding: 12px 24px;
  background: linear-gradient(45deg, #2b1055, #7597de);
  border: 2px solid #8a2be2;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  font-family: 'Press Start 2P', cursive;
  font-size: 0.9rem;
  text-shadow: 0 0 5px rgba(138, 43, 226, 0.8);
  box-shadow: 0 0 10px rgba(138, 43, 226, 0.5);
}

.arcade-nav-button::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #ff0, #00f, #f0f, #0ff);
  z-index: -1;
  animation: borderRotate 4s linear infinite;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.arcade-nav-button:hover::before,
.arcade-nav-button.active::before {
  opacity: 1;
}

.arcade-nav-button.active {
  background: linear-gradient(45deg, #4b2095, #9597de);
  transform: scale(1.05);
}

.button-text {
  position: relative;
  z-index: 1;
}

.quest-container {
  margin-top: 20px;
  padding: 20px;
}

.category-title {
  color: #f0f;
  font-size: 1.5rem;
  margin-bottom: 20px;
  text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.question-item {
  background: rgba(43, 16, 85, 0.7);
  border: 2px solid #8a2be2;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.question-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
}

.question-header {
  margin-bottom: 15px;
}

.question-number {
  background: #8a2be2;
  padding: 5px 10px;
  border-radius: 4px;
  font-weight: bold;
  font-family: 'Press Start 2P', cursive;
  font-size: 0.8rem;
}

.question-text {
  color: #fff;
  margin-bottom: 15px;
  line-height: 1.5;
}

.choices {
  margin: 15px 0;
}

.choices ul {
  margin: 8px 0;
  padding-left: 20px;
  color: #b19cd9;
}

.answer-container {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(138, 43, 226, 0.3);
}

.answer {
  color: #f0f;
  font-weight: bold;
  opacity: 0;
  transition: opacity 0.3s ease;
  text-shadow: 0 0 5px rgba(255, 0, 255, 0.5);
}

.question-item:hover .answer {
  opacity: 1;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
}

.loading-text {
  color: #f0f;
  font-family: 'Press Start 2P', cursive;
  margin-bottom: 20px;
  animation: blink 1s infinite;
}

.loading-bar {
  width: 200px;
  height: 20px;
  background: rgba(138, 43, 226, 0.3);
  border: 2px solid #8a2be2;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.loading-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 50%;
  background: linear-gradient(45deg, #8a2be2, #f0f);
  animation: loading 1s ease-in-out infinite;
}

@keyframes borderRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes loading {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(200%); }
}

@media (max-width: 768px) {
  .arcade-nav-button {
    padding: 8px 16px;
    font-size: 0.8rem;
  }

  .questions-grid {
    grid-template-columns: 1fr;
  }
}
</style>