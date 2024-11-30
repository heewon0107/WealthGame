<template>
  <div class="arcade-container">
    <div class="arcade-header">
      <div class="neon-text">INVENTORY</div>
      <div class="scanline"></div>
    </div>

    <!-- 장바구니에 상품이 있을 때 -->
    <div v-if="buckets.length > 0" class="game-grid">
      <div v-for="bucket in buckets" :key="bucket.id" 
           class="game-card"
           :class="getBankClass(bucket.kor_co_nm)">
           <div class="game-card-inner" 
            @click="goToDetail(bucket.fin_prdt_cd, bucket.id)"
            @mousemove="handleMouseMove"
            @mouseleave="handleMouseLeave">
          <div class="card-glow"></div>
          
          <div class="bank-chip">
            <span class="chip-text">{{ bucket.kor_co_nm }}</span>
          </div>

          <h3 class="product-title">{{ bucket.fin_prdt_nm }}</h3>
          
          <button @click.stop="removeFromBucket(bucket.id)" class="delete-btn">
            <span class="btn-text">REMOVE</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 장바구니가 비었을 때 -->
    <div v-else class="empty-state">
      <div class="pixel-text">{{ emptyMessage }}</div>
      <div class="insert-coin">INSERT COIN TO START</div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const buckets = ref([]);
const emptyMessage = ref('인벤토리가 비었습니다.');

onMounted(() => {
  setupAxiosInterceptors();
  // 장바구니 데이터 로드
  loadBucket();
});

const setupAxiosInterceptors = () => {
  axios.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Token ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
};

const loadBucket = (() => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/bucket/'
  })
  .then((res) => {
    // 장바구니가 비어있을 때 빈 배열 처리
    if (!res.data || res.data.length === 0) {
      buckets.value = [];
      return;
    }
    
    axios({
      url: 'http://127.0.0.1:8000/finlife/id_to_deposit/',
      method: 'get',
      params: res.data
    })
    .then((res) => {
      buckets.value = res.data
    })
    .catch(err => {
      console.log('상품 정보 로드 실패:', err);
      buckets.value = [];
    })
  })
  .catch((err) => {
    // 404 에러일 경우 빈 장바구니로 처리
    if (err.response?.status === 404) {
      buckets.value = [];
      emptyMessage.value = '인벤토리가 비었습니다.';
      return;
    }
    console.log('인벤토리 데이터 로드 실패:', err);
    emptyMessage.value = '인벤토리 데이터를 불러오는데 실패했습니다.';
  });
});

// 장바구니에서 상품 삭제하는 메서드 (추가 기능)
const removeFromBucket = async (productId) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/bucket/`, {
      data: { product_id: productId }
    });
    // 성공적으로 삭제된 후 장바구니 데이터 새로고침
    
    await loadBucket();
  } catch (error) {
    console.error('상품 제거 실패:', error);
    alert('상품을 장바구니에서 제거하는데 실패했습니다.');
  }

  // 삭제 로직을 추가할 수 있습니다. 예: axios.delete()로 API 요청 보내기
};
const goToDetail = function(fin_prdt_cd, productId) {
  router.push({
    name: 'ItemDetail',
    params: { fin_prdt_cd: fin_prdt_cd },
    query: { productId: productId }  // query로 변경
  });
};

// 은행별 클래스 매핑 함수
const getBankClass = (bankName) => {
  const bankClasses = {
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
  
  return bankClasses[bankName] || '';
};

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

const handleMouseLeave = (e) => {
  const card = e.currentTarget;
  card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
};

</script>

<style scoped>
.arcade-container {
  background-color: #1a1a2e;
  min-height: 100vh;
  padding: 2rem;
  color: #fff;
}

.arcade-header {
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
}

.neon-text {
  font-family: 'Press Start 2P', cursive;
  font-size: 3rem;
  color: #e4c8e0;
  text-shadow: 0 0 10px #e4c8e0,
               0 0 20px #e4c8e0,
               0 0 30px #e4c8e0,
               0 0 40px #800080;
  letter-spacing: 4px;
  animation: neon-pulse 1.5s infinite alternate;
}

.game-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.game-card {
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  perspective: 1000px; /* 추가 */
}

.game-card-inner {
  background: linear-gradient(135deg, #2a1f3d, #1a1a2e);
  border-radius: 15px;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
  border: 2px solid #e4c8e0;
  height: 100%;
  transition: all 0.3s ease; /* transform 제거하고 all로 변경 */
  transform-style: preserve-3d; /* 추가 */
}
.game-card:hover .game-card-inner {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 10px 20px rgba(228, 200, 224, 0.3);
}

/* 은행별 스타일 */
.bank-suhyup .game-card-inner {
  background: linear-gradient(135deg, #0056a4, #ffffff);
}

.bank-hana .game-card-inner {
  background: linear-gradient(135deg, #008485, #e60012);
}

.bank-nonghyup .game-card-inner {
  background: linear-gradient(135deg, #00a862, #fff100);
}

.bank-shinhan .game-card-inner {
  background: linear-gradient(135deg, #0046ff, #ffd700);
}

.bank-kb .game-card-inner {
  background: linear-gradient(135deg, #545454, #ffbc00);
}

.bank-gwangju .game-card-inner {
  background: linear-gradient(135deg, #ff0000, #ffffff);
}

.bank-woori .game-card-inner {
  background: linear-gradient(135deg, #0067b3, #ffffff);
}

.bank-busan .game-card-inner {
  background: linear-gradient(135deg, #0067a3, #ff9ecd);
}

.bank-jeju .game-card-inner {
  background: linear-gradient(135deg, #ff6b00, #ffffff);
}

.bank-kyongnam .game-card-inner {
  background: linear-gradient(135deg, #ff0000, #ffcce6);
}

.bank-jeonbuk .game-card-inner {
  background: linear-gradient(135deg, #004ea2, #ffffff);
}

.bank-sc .game-card-inner {
  background: linear-gradient(135deg, #0051a3, #00a862);
}

.bank-im .game-card-inner {
  background: linear-gradient(135deg, #00a862, #0067b3);
}

.bank-kbank .game-card-inner {
  background: linear-gradient(135deg, #000080, #00ff00);
}

.bank-kdb .game-card-inner {
  background: linear-gradient(135deg, #87ceeb, #0067b3);
}

.bank-toss .game-card-inner {
  background: linear-gradient(135deg, #000033, #ffffff);
}
.bank-kakao{
  background: linear-gradient(135deg, #a7b321, #ffffff);
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 15px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
  box-shadow: 0 0 20px rgba(228, 200, 224, 0.5);
}

.game-card:hover .card-glow {
  opacity: 1;
}

.bank-chip {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  margin-bottom: 1rem;
  display: inline-block;
  backdrop-filter: blur(5px);
}

.chip-text {
  color: #fff;
  font-size: 0.9rem;
  font-weight: bold;
  text-transform: uppercase;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.product-title {
  font-size: 1.2rem;
  color: #ffffff;
  margin: 1rem 0;
  min-height: 3rem;
  line-height: 1.4;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.delete-btn {
  width: 100%;
  padding: 0.8rem;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #fff;
  font-family: 'Press Start 2P', cursive;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: auto;
}

.delete-btn:hover {
  background: rgba(255, 0, 0, 0.3);
  transform: scale(1.02);
  box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
}

/* 삭제 애니메이션 */
@keyframes explode {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.5;
  }
  100% {
    transform: scale(0);
    opacity: 0;
  }
}

.game-card.removing {
  animation: explode 0.5s ease-out forwards;
}

/* 빈 상태 스타일 */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.pixel-text {
  /* font-family: 'Press Start 2P', cursive; */
  font-size: 1.2rem;
  color: #e4c8e0;
  margin-bottom: 2rem;
}

.insert-coin {
  font-family: 'Press Start 2P', cursive;
  font-size: 0.8rem;
  color: #800080;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .neon-text {
    font-size: 2rem;
  }
  
  .game-grid {
    grid-template-columns: 1fr;
  }
  
  .game-card {
    margin: 1rem 0;
  }
}
</style>