<template>
  <div class="cyber-news-container">
    <div class="cyber-title" data-text="ITEM NEWS">ITEM NEWS</div>
    
    <div v-if="newsList.length > 0" class="news-grid">
      <div v-for="(news, index) in newsList" 
           :key="index" 
           class="news-terminal"
           :class="{ 'fade-in': true }"
           :style="{ animationDelay: `${index * 0.1}s` }">
        <div class="terminal-header">
          <div class="terminal-buttons">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <div class="terminal-title">NEWS_{{ index + 1 }}</div>
        </div>
        
        <div class="terminal-content">
          <div class="image-container">
            <img 
              v-if="news.thumbnail_url" 
              :src="news.thumbnail_url" 
              :alt="news.title" 
              class="news-thumbnail"
              @error="handleImageError"
            />
            <!-- 이미지 없을 때 표시할 대체 이미지 -->
            <div v-else class="placeholder-image">
              <div class="cyber-box">WG NEWS</div>
            </div>
          </div>
          
          <div class="news-info">
            <h2 class="news-title">{{ news.title }}</h2>
            <div class="news-summary">
              <p>{{ news.summary }}</p>
            </div>
            <div class="news-meta">
              <span class="publisher">{{ news.publisher }}</span>
              <a :href="news.content_url" 
                 target="_blank" 
                 class="cyber-button"
                 @mouseover="handleHover"
                 @mouseout="handleHoverOut">
                <span class="button-text">READ_MORE</span>
                <span class="button-glitch"></span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 로딩 애니메이션 -->
    <div v-if="loading" class="loading-container">
      <div class="cyber-spinner">
        <div class="spinner-inner"></div>
        <div class="loading-text">LOADING DATA...</div>
      </div>
    </div>

    <div v-if="newsList.length === 0 && !loading" class="no-news">
      <div class="cyber-box">NO NEWS FOUND</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

const newsList = ref([]);
const loading = ref(false);
const soundEffect = new Audio('/path-to-your-hover-sound.mp3'); // 옵션: 호버 사운드

const props = defineProps({
  fin_prdt_nm: String
});

const page = ref(1);
const pageSize = 10;

const handleImageError = (event) => {
  event.target.style.display = 'none';
  event.target.parentElement.classList.add('show-placeholder');
};

const handleHover = () => {
  // 옵션: 호버 사운드 재생
  // soundEffect.play();
};

const handleHoverOut = () => {
  // 호버 아웃 효과
};

const fetchNews = () => {
  if (loading.value) return;

  loading.value = true;

  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/news',
    params: {
      keyword: props.fin_prdt_nm,
      page: page.value,
      page_size: pageSize
    }
  })
    .then((res) => {
      if (res.data && res.data.data && res.data.data.length > 0) {
        newsList.value = [...newsList.value, ...res.data.data];
        page.value += 1;
      }
    })
    .catch((err) => {
      console.error('API 호출 실패:', err);
    })
    .finally(() => {
      loading.value = false;
    });
};

const handleScroll = () => {
  const bottomOfPage = 
    window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 800;

  if (bottomOfPage && !loading.value) {
    fetchNews();
  }
};

onMounted(() => {
  fetchNews();
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.cyber-news-container {
  padding: 2rem;
  background: #000;
  min-height: 100vh;
  color: #fff;
  font-family: 'DungGeunMo', sans-serif;
  margin-bottom: 4rem;
}

.cyber-title {
  font-size: 3rem;
  text-align: center;
  color: #f0f;
  text-shadow: 2px 2px #0ff;
  margin-bottom: 3rem;
  position: relative;
  letter-spacing: 4px;
}

.cyber-title::before {
  content: attr(data-text);
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  text-shadow: 2px 2px #f00;
  animation: glitch 1s infinite;
  opacity: 0.8;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.news-terminal {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #f0f;
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.3s ease;
  opacity: 0;
  animation: fadeIn 0.5s forwards;
}

.news-terminal:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.4);
}

.terminal-header {
  background: rgba(255, 0, 255, 0.1);
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #f0f;
}

.terminal-buttons {
  display: flex;
  gap: 0.5rem;
}

.terminal-buttons span {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #f0f;
  opacity: 0.5;
}

.terminal-title {
  margin-left: auto;
  color: #f0f;
  font-size: 0.9rem;
}

.terminal-content {
  padding: 1.5rem;
}

.image-container {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  margin-bottom: 1rem;
  background: rgba(255, 0, 255, 0.1);
  border: 1px solid rgba(255, 0, 255, 0.2);
}

.news-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.news-terminal:hover .news-thumbnail {
  transform: scale(1.05);
}

.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, rgba(255, 0, 255, 0.1), rgba(0, 255, 255, 0.1));
}

.cyber-box {
  padding: 1rem 2rem;
  border: 2px solid #f0f;
  color: #f0f;
  text-shadow: 0 0 5px #f0f;
  font-size: 1.2rem;
  background: rgba(0, 0, 0, 0.5);
}

.news-title {
  font-size: 1.2rem;
  color: #0ff;
  margin-bottom: 1rem;
  line-height: 1.4;
  height: 2.8em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.news-summary {
  font-size: 0.9rem;
  color: #fff;
  margin-bottom: 1rem;
  line-height: 1.6;
  height: 4.8em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.publisher {
  color: #f0f;
  font-size: 0.9rem;
}

.cyber-button {
  position: relative;
  padding: 0.5rem 1rem;
  background: rgba(255, 0, 255, 0.1);
  border: 1px solid #f0f;
  color: #f0f;
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  overflow: hidden;
}

.cyber-button:hover {
  background: rgba(255, 0, 255, 0.2);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.4);
}

.button-glitch {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 0, 255, 0.3);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.cyber-button:hover .button-glitch {
  transform: translateX(100%);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.cyber-spinner {
  position: relative;
  width: 60px;
  height: 60px;
}

.spinner-inner {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top-color: #f0f;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner-inner::before,
.spinner-inner::after {
  content: '';
  position: absolute;
  border: 3px solid transparent;
  border-radius: 50%;
}

.spinner-inner::before {
  top: 5px;
  left: 5px;
  right: 5px;
  bottom: 5px;
  border-top-color: #0ff;
  animation: spin 2s linear infinite;
}

.spinner-inner::after {
  top: 15px;
  left: 15px;
  right: 15px;
  bottom: 15px;
  border-top-color: #f0f;
  animation: spin 1.5s linear infinite;
}

.loading-text {
  position: absolute;
  top: 70px;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  color: #f0f;
  font-size: 0.9rem;
  animation: blink 1s infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes glitch {
  0%, 100% { transform: translateX(-50%) skew(0deg); }
  20% { transform: translateX(-50%) skew(10deg); }
  40% { transform: translateX(-50%) skew(-10deg); }
}

@media (max-width: 768px) {
  .cyber-news-container {
    padding: 1rem;
  }
  
  .news-grid {
    grid-template-columns: 1fr;
  }
  
  .cyber-title {
    font-size: 2rem;
  }
  
  .image-container {
    height: 150px;
  }
}

/* 스크롤바 커스터마이징 */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
}

::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 0, 255, 0.8);
}
</style>