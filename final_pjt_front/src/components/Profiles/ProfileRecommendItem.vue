<template>
  <div class="cyber-recommend">
    <!-- 배경 효과 -->
    <div class="stars"></div>
    <div class="twinkling"></div>
    <div class="grid-overlay"></div>
    
    <div class="content-container">
      <div class="title-container">
        <div class="glitch-title" data-text="RECOMMENDED">RECOMMENDED</div>
        <div class="sub-title">FOR YOU</div>
      </div>
      
      <div class="category-select">
        <div class="neon-text">SELECT CATEGORY</div>
        <select v-model="selectedCategory" @change="updateData" class="cyber-select">
          <option value="나이">AGE MATCH</option>
          <option value="자산">ASSET MATCH</option>
          <option value="수입">INCOME MATCH</option>
          <option value="금액">AMOUNT MATCH</option>
          <option value="기간">PERIOD MATCH</option>
          <option value="티어">TIER MATCH</option>
        </select>
      </div>

      <div v-if="recommendItems && recommendItems.length > 0" class="items-grid">
        <div v-for="item in sortedItems" 
             :key="item.id" 
             :class="['item-card', getBankClass(item.kor_co_nm)]"
             @mousemove="handleMouseMove"
             @click="goToDetail(item.fin_prdt_cd, item.id)">
          <div class="card-glow"></div>
          <div class="card-content">
            <div class="bank-badge">{{ item.kor_co_nm }}</div>
            <h3 class="product-name">{{ item.fin_prdt_nm }}</h3>
            <button class="detail-btn">
              <span class="btn-text">VIEW DETAILS</span>
              <span class="btn-glow"></span>
            </button>
          </div>
          <div class="card-frame">
            <div class="corner top-left"></div>
            <div class="corner top-right"></div>
            <div class="corner bottom-left"></div>
            <div class="corner bottom-right"></div>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-state">
        <div class="error-text">NO MATCHING ITEMS</div>
        <div class="sub-text">TRY DIFFERENT CATEGORY</div>
        <div class="error-glitch"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const selectedCategory = ref("나이");
const recommendItems = ref(null);
const isLoggedIn = ref(false);

const bankClassMap = {
  '수협은행': 'bank-suhyup',
  '하나은행': 'bank-hana',
  '농협은행주식회사': 'bank-nonghyup',
  '신한은행': 'bank-shinhan',
  '국민은행': 'bank-kb',
  '광주은행': 'bank-gwangju',
  '우리은행': 'bank-woori',
  '부산은행': 'bank-busan',
  '제주은행': 'bank-jeju',
  '경남은행': 'bank-kyongnam',
  '전북은행': 'bank-jeonbuk',
  '한국스탠다드차타드은행': 'bank-sc',
  '아이엠뱅크': 'bank-im',
  '주식회사 케이뱅크': 'bank-kbank',
  '한국산업은행': 'bank-kdb',
  '토스뱅크 주식회사': 'bank-toss',
  '주식회사 카카오뱅크' : 'bank-kakao'
};

const getBankClass = (bankName) => {
  return bankClassMap[bankName] || '';
};

// 금리순으로 정렬된 아이템 리스트
const sortedItems = computed(() => {
  if (!recommendItems.value) return [];
  return [...recommendItems.value].sort((a, b) => (b.intr_rate2 || 0) - (a.intr_rate2 || 0));
});

const checkLoginStatus = function() {
  const token = localStorage.getItem('token');
  isLoggedIn.value = !!token;
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Token ${token}`;
  }
}

const goToDetail = function(fin_prdt_cd, productId) {
  router.push({
    name: 'ItemDetail',
    params: { fin_prdt_cd: fin_prdt_cd },
    query: { productId: productId }
  });
}

const updateData = async () => {
  let url = `http://127.0.0.1:8000/accounts/same/${selectedCategory.value}/`;
  try {
    const response = await axios.get(url);
    recommendItems.value = response.data;
  } catch (err) {
    console.error(err);
  }
}

onMounted(() => {
  checkLoginStatus();
  updateData();
})

const handleMouseMove = (e) => {
  const card = e.currentTarget;
  const rect = card.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  
  const centerX = rect.width / 2;
  const centerY = rect.height / 2;
  
  const rotateX = (y - centerY) / 10;
  const rotateY = -(x - centerX) / 10;
  
  card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
};
</script>

<style scoped>
.cyber-recommend {
  min-height: 100vh;
  background: #000;
  padding: 40px 20px;
  position: relative;
  overflow: hidden;
}

.stars {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000 url('/stars.png') repeat;
  z-index: 0;
}

.twinkling {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: transparent url('/twinkling.png') repeat;
  animation: move-twinkle 200s linear infinite;
  opacity: 0.5;
  z-index: 1;
}

.grid-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    linear-gradient(transparent 95%, rgba(255, 0, 255, 0.1) 95%),
    linear-gradient(90deg, transparent 95%, rgba(255, 0, 255, 0.1) 95%);
  background-size: 30px 30px;
  pointer-events: none;
  z-index: 1;
}

.content-container {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
}

.title-container {
  text-align: center;
  margin-bottom: 50px;
}

.glitch-title {
  font-family: 'DungGeunMo';
  font-size: 3.5rem;
  color: #f0f;
  text-shadow: 
    3px 3px #0ff,
    -3px -3px #f00;
  animation: glitch 5s infinite;
}

.sub-title {
  font-family: 'DungGeunMo';
  font-size: 2rem;
  color: #0ff;
  margin-top: 10px;
  text-shadow: 0 0 10px #0ff;
}

.category-select {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 40px;
}

.neon-text {
  font-family: 'DungGeunMo';
  color: #0ff;
  text-shadow: 0 0 10px #0ff;
}

.cyber-select {
  background: rgba(255, 0, 255, 0.1);
  border: 2px solid #f0f;
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  font-family: 'DungGeunMo';
  cursor: pointer;
  transition: all 0.3s ease;
}

.cyber-select:hover {
  border-color: #0ff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.cyber-select option {
  background: #000;
  color: #fff;
  padding: 10px;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 30px;
  padding: 20px;
}

.item-card {
  position: relative;
  height: 250px;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  transform-style: preserve-3d;
  overflow: hidden;
  border: none;
}

.item-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 10px 25px rgba(228, 200, 224, 0.4);
}

/* 카드 움직임 효과를 위한 스타일 */
.item-card {
  transition: transform 0.5s ease;
  perspective: 1000px;
}

.card-content {
  position: relative;
  height: 100%;
  padding: 20px;
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border-radius: 15px;
}

/* 은행별 스타일 */
.bank-suhyup {
  background: linear-gradient(135deg, #0056a4, #ffffff);
  box-shadow: 0 5px 15px rgba(0, 86, 164, 0.3);
}

.bank-hana {
  background: linear-gradient(135deg, #008485, #e60012);
  box-shadow: 0 5px 15px rgba(0, 132, 133, 0.3);
}

.bank-nonghyup {
  background: linear-gradient(135deg, #00a862, #fff100);
  box-shadow: 0 5px 15px rgba(0, 168, 98, 0.3);
}

.bank-shinhan {
  background: linear-gradient(135deg, #0046ff, #ffd700);
  box-shadow: 0 5px 15px rgba(0, 70, 255, 0.3);
}

.bank-kb {
  background: linear-gradient(135deg, #545454, #ffbc00);
  box-shadow: 0 5px 15px rgba(84, 84, 84, 0.3);
}

.bank-gwangju {
  background: linear-gradient(135deg, #ff0000, #ffffff);
  box-shadow: 0 5px 15px rgba(255, 0, 0, 0.3);
}

.bank-woori {
  background: linear-gradient(135deg, #0067b3, #ffffff);
  box-shadow: 0 5px 15px rgba(0, 103, 179, 0.3);
}

.bank-busan {
  background: linear-gradient(135deg, #0067a3, #ff9ecd);
  box-shadow: 0 5px 15px rgba(0, 103, 163, 0.3);
}

.bank-jeju {
  background: linear-gradient(135deg, #ff6b00, #ffffff);
  box-shadow: 0 5px 15px rgba(255, 107, 0, 0.3);
}

.bank-kyongnam {
  background: linear-gradient(135deg, #ff0000, #ffcce6);
  box-shadow: 0 5px 15px rgba(255, 0, 0, 0.3);
}

.bank-jeonbuk {
  background: linear-gradient(135deg, #004ea2, #ffffff);
  box-shadow: 0 5px 15px rgba(0, 78, 162, 0.3);
}

.bank-sc {
  background: linear-gradient(135deg, #0051a3, #00a862);
  box-shadow: 0 5px 15px rgba(0, 81, 163, 0.3);
}

.bank-im {
  background: linear-gradient(135deg, #00a862, #0067b3);
  box-shadow: 0 5px 15px rgba(0, 168, 98, 0.3);
}

.bank-kbank {
  background: linear-gradient(135deg, #000080, #00ff00);
  box-shadow: 0 5px 15px rgba(0, 0, 128, 0.3);
}

.bank-kdb {
  background: linear-gradient(135deg, #87ceeb, #0067b3);
  box-shadow: 0 5px 15px rgba(135, 206, 235, 0.3);
}

.bank-toss {
  background: linear-gradient(135deg, #000033, #ffffff);
  box-shadow: 0 5px 15px rgba(0, 0, 51, 0.3);
}
.bank-kakao{
  background: linear-gradient(135deg, #a7b321, #ffffff);
  box-shadow: 0 5px 15px rgba(184, 161, 34, 0.3);
}

.bank-badge {
  position: absolute;
  top: 15px;
  left: 15px;
  padding: 7px 15px;
  border-radius: 20px;
  font-family: 'DungGeunMo';
  font-size: 0.9rem;
  color: #fff;
  z-index: 2;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.product-name {
  font-family: 'DungGeunMo';
  font-size: 1.4rem;
  color: #fff;
  margin: 60px 20px 20px;
  line-height: 1.4;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
  position: relative;
  z-index: 2;
}

.detail-btn {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 30px;
  background: transparent;
  border: 2px solid #f0f;
  border-radius: 5px;
  color: #fff;
  font-family: 'DungGeunMo';
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.btn-text {
  position: relative;
  z-index: 2;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 0, 255, 0.5),
    transparent
  );
  transition: 0.5s;
}

.detail-btn:hover .btn-glow {
  left: 100%;
}

.detail-btn:hover {
  background: rgba(255, 0, 255, 0.2);
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
}

.item-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0) 100%
  );
  pointer-events: none;
}

.card-frame {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 2px solid transparent;
  pointer-events: none;
}

.corner {
  position: absolute;
  width: 15px;
  height: 15px;
  border: 2px solid #f0f;
}

.top-left {
  top: 0;
  left: 0;
  border-right: 0;
  border-bottom: 0;
}

.top-right {
  top: 0;
  right: 0;
  border-left: 0;
  border-bottom: 0;
}

.bottom-left {
  bottom: 0;
  left: 0;
  border-right: 0;
  border-top: 0;
}

.bottom-right {
  bottom: 0;
  right: 0;
  border-left: 0;
  border-top: 0;
}

.empty-state {
  text-align: center;
  padding: 100px 20px;
  position: relative;
}

.error-text {
  font-family: 'DungGeunMo';
  font-size: 2rem;
  color: #f0f;
  margin-bottom: 20px;
  text-shadow: 0 0 10px #f0f;
}

.sub-text {
  font-family: 'DungGeunMo';
  color: #0ff;
  font-size: 1.2rem;
  opacity: 0.8;
  animation: blink 1.5s infinite;
}

.error-glitch {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: rgba(255, 0, 255, 0.2);
  filter: blur(10px);
  animation: errorPulse 2s infinite;
}

/* 애니메이션 */
@keyframes glitch {
  0% {
    text-shadow: 3px 3px #0ff, -3px -3px #f00;
  }
  25% {
    text-shadow: -3px 3px #0ff, 3px -3px #f00;
  }
  50% {
    text-shadow: 3px -3px #0ff, -3px 3px #f00;
  }
  75% {
    text-shadow: -3px -3px #0ff, 3px 3px #f00;
  }
  100% {
    text-shadow: 3px 3px #0ff, -3px -3px #f00;
  }
}

@keyframes move-twinkle {
  from { background-position: 0 0; }
  to { background-position: -10000px 5000px; }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes errorPulse {
  0% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.5); opacity: 0.2; }
  100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
}

/* 반응형 */
@media (max-width: 768px) {
  .glitch-title {
    font-size: 2.5rem;
  }
  
  .sub-title {
    font-size: 1.5rem;
  }
  
  .items-grid {
    grid-template-columns: 1fr;
  }
  
  .category-select {
    flex-direction: column;
  }
  
  .cyber-select {
    width: 100%;
    max-width: 300px;
  }
}
</style>