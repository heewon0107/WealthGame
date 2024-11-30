<template>
  <div class="arcade-detail-container">
    <!-- 뒤로가기 버튼 -->
    <button class="cyber-back-btn" @click="goBack">
      <ArrowLeft class="icon-glow" size="20" />
      BACK
    </button>
    
    <!-- 아이템 정보 -->
    <div class="cyber-product-info">
      <div class="cyber-header">
        <div class="glitch-text" data-text="ITEM INFO">ITEM INFO</div>
        <h2 class="product-title">{{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}</h2>
      </div>
      <button 
        @click="toggleBucket" 
        class="inventory-btn"
        :class="{'added': isAdded, 'not-added': !isAdded}"
      >
        <Backpack class="btn-icon" size="20" />
        {{ isAdded ? '인벤토리 삭제' : '인벤토리 추가' }}
      </button>
    </div>

    <!-- 네비게이션 메뉴 -->
    <div class="cyber-tabs">
      <router-link
        :to="{name: 'ItemDetailDescription'}"
        class="cyber-tab"
        active-class="active-tab"
      >
        <Scroll class="tab-icon" size="20" />
        아이템 설명
      </router-link>
      <router-link
        :to="{name: 'ItemNearShop'}"
        class="cyber-tab"
        active-class="active-tab"
      >
        <Store class="tab-icon" size="20" />
        주변 상점 찾기
      </router-link>
      <router-link
        :to="{name: 'ItemCommunity', params: { productId: productId }}"
        class="cyber-tab"
        active-class="active-tab"
      >
        <MessageSquare class="tab-icon" size="20" />
        아이템 후기
      </router-link>
      <router-link
        v-if="productName"
        :to="{name: 'ItemNews', params: {fin_prdt_nm: productName}}"
        class="cyber-tab"
        active-class="active-tab"
      >
        <Newspaper class="tab-icon" size="20" />
        아이템 뉴스
      </router-link>
    </div>

    <!-- 라우터 뷰 -->
    <div class="cyber-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { useInventoryStore } from '@/stores/inventory'
import { 
  ArrowLeft, 
  Backpack, 
  Scroll, 
  Store, 
  MessageSquare, 
  Newspaper 
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const inventoryStore = useInventoryStore()

const product = ref({})
const productId = ref(0)
const isAdded = ref(false)
const productName = ref('')

// axios 설정
const setupAxios = () => {
  const token = localStorage.getItem('token')
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Token ${token}`
  }
}

// 상품 세부 정보 불러오기
const fetchProductDetails = async (fin_prdt_cd) => {
  try {
    const productResponse = await axios.get(`http://127.0.0.1:8000/finlife/deposit_product_detail/${fin_prdt_cd}`)
    product.value = productResponse.data
    productId.value = productResponse.data.id
    productName.value = productResponse.data.fin_prdt_nm
    // 상품 정보를 가져온 후 인벤토리 상태 확인
    isAdded.value = inventoryStore.getItemStatus(productResponse.data.id)
  } catch (error) {
    console.error('상품 데이터 불러오기 실패:', error)
  }
}

// 인벤토리 추가/삭제 토글
const toggleBucket = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/bucket/',
      {
        product_id: productId.value,
      },
      {
        headers: {
          'Authorization': `Token ${token}`
        }
      }
    )

    const status = response.data.message
    inventoryStore.setItemStatus(productId.value, status)
    isAdded.value = inventoryStore.getItemStatus(productId.value)
  } catch (error) {
    console.error('인벤토리 작업 실패:', error)
  }
}

// 뒤로가기
const goBack = () => {
  router.go(-1)
}

// 컴포넌트 마운트 시 초기화
onMounted(async () => {
  setupAxios()
  await inventoryStore.initializeInventory()
  const fin_prdt_cd = route.params.fin_prdt_cd
  await fetchProductDetails(fin_prdt_cd)
  router.push({ name: 'ItemDetailDescription' })
})

// 인벤토리 상태 변경 감지
watch(
  () => inventoryStore.inventoryItems,
  (newInventory) => {
    if (productId.value) {
      isAdded.value = newInventory[productId.value] || false
    }
  },
  { deep: true }
)

// 라우트 변경 감지
watch(
  () => route.params.fin_prdt_cd,
  async (newVal, oldVal) => {
    if (newVal !== oldVal) {
      await fetchProductDetails(newVal)
    }
  }
)
</script>

<style scoped>
.arcade-detail-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
  font-family: 'DungGeunMo', sans-serif;
  color: #fff;
  height: calc(100vh);  /* 상단 여백 2rem을 고려한 높이 */
  overflow-y: auto;  /* 스크롤 가능하도록 */
}
.arcade-detail-container::-webkit-scrollbar {
  width: 8px;
}

.arcade-detail-container::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 10px;
}

.arcade-detail-container::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 10px;
  box-shadow: 0 0 10px #f0f;
}

.arcade-detail-container::-webkit-scrollbar-thumb:hover {
  background: #f0f;
  box-shadow: 0 0 15px #f0f;
}

.cyber-back-btn {
  background: transparent;
  border: 2px solid #f0f;
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'DungGeunMo';
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.cyber-back-btn:hover {
  background: rgba(255, 0, 255, 0.2);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
}

.cyber-product-info {
  background: rgba(0, 0, 0, 0.8);
  padding: 2rem;
  border-radius: 16px;
  border: 2px solid #f0f;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.2);
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cyber-header {
  text-align: left;
}

.glitch-text {
  font-size: 1rem;
  color: #f0f;
  text-shadow: 2px 2px #0ff;
  margin-bottom: 0.5rem;
  animation: glitch 1s infinite;
}

.product-title {
  color: #fff;
  font-size: 2rem;
  margin: 0;
}

.inventory-btn {
  background: transparent;
  border: 2px solid #f0f;
  color: #fff;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'DungGeunMo';
  transition: all 0.3s ease;
}

.inventory-btn.added {
  background: #f0f;
  border-color: #fff;
}

.inventory-btn.not-added:hover {
  background: rgba(255, 0, 255, 0.2);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
}

.inventory-btn.added:hover {
  background: #ff3366;
}

.cyber-tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.cyber-tab {
  background: rgba(0, 0, 0, 0.6);
  border: 2px solid #f0f;
  color: #fff;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.cyber-tab:hover {
  background: rgba(255, 0, 255, 0.2);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
}

.active-tab {
  background: #f0f;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.4);
  transform: translateY(-2px);
}

.icon-glow {
  color: #f0f;
  filter: drop-shadow(0 0 5px #f0f);
}

.btn-icon {
  color: currentColor;
}

.tab-icon {
  color: currentColor;
}

.cyber-content {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #f0f;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;  /* 하단 여백 추가 */
}

@keyframes glitch {
  0% {
    text-shadow: 2px 2px #0ff;
  }
  25% {
    text-shadow: -2px 2px #f0f;
  }
  50% {
    text-shadow: 2px -2px #0ff;
  }
  75% {
    text-shadow: -2px -2px #f0f;
  }
  100% {
    text-shadow: 2px 2px #0ff;
  }
}

@media (max-width: 768px) {
  .cyber-product-info {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .cyber-header {
    text-align: center;
  }

  .cyber-tabs {
    flex-direction: column;
  }

  .cyber-tab {
    width: 100%;
    justify-content: center;
  }

  .product-title {
    font-size: 1.5rem;
  }
}
</style>
