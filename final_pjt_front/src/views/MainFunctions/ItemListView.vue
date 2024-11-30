<template>
  <div class="arcade-deposit-container">
    <div class="cyber-header">
      <div class="glitch-text" data-text="예적금 상품 조회">예적금 상품 조회</div>
    </div>

    <div class="cyber-filters">
      <div class="filter-item">
        <Gamepad2 size="20" class="icon-glow" />
        <label for="bank">은행선택:</label>
        <select v-model="filterBank" id="bank">
          <option value="">전체</option>
          <option v-for="bank in filteredBanks" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
      </div>

      <div class="filter-item">
        <Timer size="20" class="icon-glow" />
        <label for="period">기간선택:</label>
        <select v-model="filterPeriod" id="period">
          <option value="">전체</option>
          <option v-for="period in availablePeriods" :key="period" :value="period">
            {{ period }}개월
          </option>
        </select>
      </div>
    </div>
    <div v-if="loading" class="loading-overlay">
      <div class="loading-content">LOADING...</div>
    </div>

    <div v-else-if="filteredDepositProducts.length > 0" class="deposit-list">
      <div v-for="product in filteredDepositProducts" 
           :key="product.fin_prdt_cd" 
           class="cyber-card"
           @click="goToDetail(product.fin_prdt_cd, product.id)">
        <div class="card-header">
          <div class="header-main">
          <Coins class="bank-icon icon-glow" size="24" />
          <h2 class="cyber-title">{{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}</h2>
          <button 
            @click.stop="toggleBucket(product.id)" 
            class="inventory-btn"
            :class="{'added': isInBucket[product.id]}"
          >
            <Backpack class="inventory-icon" size="20" />
            {{ isInBucket[product.id] ? '인벤토리 삭제' : '인벤토리 추가' }}
          </button>
        </div>
          <div class="rate-summary">
            <div class="rate-summary-item highest">
              최고금리: {{ getMaxRate(product.options) }}%
            </div>
            <div class="rate-summary-item lowest">
              최저금리: {{ getMinRate(product.options) }}%
            </div>
          </div>
        </div>
        
        <div class="card-content">
          <div class="chart-container">
            <Bar
              :data="formatChartData(getFilteredOptions(product.options))"
              :options="chartOptions"
              class="rate-chart"
            />
          </div>
        </div>

        <div class="card-footer">
          <Sparkles size="16" class="icon-glow" />
          공시 제출월: {{ product.dcls_month }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { useInventoryStore } from '@/stores/inventory'
import { useRouter } from 'vue-router'
import { 
  Gamepad2,
  Timer,
  Coins,
  Sparkles,
  Backpack
} from 'lucide-vue-next'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const loading = ref(true)
const router = useRouter()
const depositProducts = ref([])
const filterBank = ref('')
const filterPeriod = ref('')
const availablePeriods = ref([6, 12, 24, 36])
const isInBucket = ref({})
const inventoryStore = useInventoryStore()

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(255, 0, 255, 0.1)',
      },
      ticks: {
        color: '#f0f'
      }
    },
    x: {
      grid: {
        color: 'rgba(255, 0, 255, 0.1)',
      },
      ticks: {
        color: '#f0f'
      }
    }
  },
  plugins: {
    legend: {
      labels: {
        color: '#f0f',
        font: {
          // family: 'DungGeunMo'
        }
      }
    }
  }
}

const formatChartData = (options) => {
  if (!options) return null
  
  return {
    labels: options.map(opt => `${opt.save_trm}개월`),
    datasets: [
      {
        label: '기본금리',
        data: options.map(opt => opt.intr_rate),
        backgroundColor: 'rgba(74, 222, 128, 0.8)',  // 기본금리 초록색
        borderColor: '#4ade80',
        borderWidth: 1
      },
      {
        label: '우대금리',
        data: options.map(opt => opt.intr_rate2),
        backgroundColor: 'rgba(255, 0, 255, 0.8)',   // 우대금리 보라색
        borderColor: '#f0f',
        borderWidth: 1
      }
    ]
  }
}

const getFilteredOptions = (options = []) => {
  if (!filterPeriod.value) return options;
  return options.filter(option => option.save_trm === parseInt(filterPeriod.value));
}

const getMaxRate = (options = []) => {
  if (!options.length) return 0;
  return Math.max(...options.map(opt => opt.intr_rate2))?.toFixed(2) || 0;
}

const getMinRate = (options = []) => {
  if (!options.length) return 0;
  return Math.min(...options.map(opt => opt.intr_rate2))?.toFixed(2) || 0;
}

const isHighestRate = (currentOption, allOptions = []) => {
  if (!allOptions.length) return false;
  const maxRate = Math.max(...allOptions.map(opt => opt.intr_rate2));
  return currentOption.intr_rate2 === maxRate;
}

const isLowestRate = (currentOption, allOptions = []) => {
  if (!allOptions.length) return false;
  const minRate = Math.min(...allOptions.map(opt => opt.intr_rate2));
  return currentOption.intr_rate2 === minRate;
}

const goToDetail = (fin_prdt_cd, productId) => {
  router.push({
    name: 'ItemDetail',
    params: { fin_prdt_cd: fin_prdt_cd, productId: productId }
  });
}

const filteredBanks = computed(() => {
  return [...new Set(depositProducts.value.map(product => product.kor_co_nm))]
})

const formatJoinPeriod = (joinPeriod) => {
  if (Array.isArray(joinPeriod)) {
    return joinPeriod.join(', ')
  }
  return joinPeriod
}

const filteredDepositProducts = computed(() => {
  return depositProducts.value.filter(product => {
    const matchesBank = filterBank.value === '' || product.kor_co_nm === filterBank.value;
    const hasMatchingPeriod = !filterPeriod.value || 
      (product.options || []).some(option => option.save_trm === parseInt(filterPeriod.value));
    return matchesBank && hasMatchingPeriod;
  })
})

const toggleBucket = async (productId) => {
  const token = localStorage.getItem('token')
  if (!token) {
    alert('로그인이 필요한 서비스입니다.')
    return
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/bucket/', 
      {
        product_id: productId,
      },
      {
        headers: {
          'Authorization': `Token ${token}`  // 헤더 추가
        }
      }
    )

    const status = response.data.message
    inventoryStore.setItemStatus(productId, status)
    isInBucket.value[productId] = inventoryStore.getItemStatus(productId)
  } catch (error) {
    console.error('인벤토리 작업 실패:', error)
  }
}

onMounted(async () => {
  try {
    loading.value = true

    const response = await axios.get('http://127.0.0.1:8000/finlife/deposit-products/')
    const products = response.data
    
    // 상품 정보 가져오기
    const promises = products.map(product => {
      return axios.get(`http://127.0.0.1:8000/finlife/deposit-products-options/${product.fin_prdt_cd}/`)
        .then(optionRes => {
          product.options = optionRes.data
          const periods = [...new Set(product.options.map(option => option.save_trm))]
          product.join_period = periods
          loading.value = false
          return product
        })
        .catch(error => {
          product.options = []
          product.join_period = []
          console.error(error)
          loading.value = false
          return product
        })
    })

    const completedProducts = await Promise.all(promises)
    depositProducts.value = completedProducts
    sessionStorage.setItem('depositProducts', JSON.stringify(completedProducts))
    
    // 인벤토리 초기화 완료 후 상태 업데이트
    await inventoryStore.initializeInventory()
    
    // 모든 상품의 인벤토리 상태를 한 번에 업데이트
    depositProducts.value.forEach(product => {
      isInBucket.value[product.id] = inventoryStore.getItemStatus(product.id)
    })

    loading.value = false
  } catch (err) {
    console.error(err)
  }
})

</script>

<style scoped>
.arcade-deposit-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
  /* font-family: 'DungGeunMo', sans-serif; */
  color: #fff;
  background: rgba(0, 0, 0, 0.9);
  min-height: 100vh
}

.cyber-header {
  text-align: center;
  margin-bottom: 2rem;
}

.glitch-text {
  font-size: 2.5rem;
  color: #f0f;
  text-shadow: 2px 2px #0ff;
  position: relative;
  animation: glitch 1s infinite;
}

.cyber-filters {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  background: rgba(255, 0, 255, 0.1);
  padding: 1rem;
  border-radius: 12px;
  border: 2px solid #f0f;
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.filter-item label {
  color: #f0f;
  text-shadow: 0 0 5px #f0f;
}

.filter-item select {
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.7);
  border: 2px solid #f0f;
  border-radius: 8px;
  color: #fff;
  /* font-family: 'DungGeunMo'; */
  outline: none;
}

.filter-item select:focus {
  box-shadow: 0 0 15px #f0f;
}

.cyber-card {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #f0f;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.2);
  transition: all 0.3s ease;
  cursor: pointer;
}

.cyber-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(255, 0, 255, 0.4);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.cyber-title {
  color: #fff;
  font-size: 1.25rem;
  margin: 0;
}

.rate-summary {
  border-left: 2px solid #f0f;
  padding-left: 1rem;
  font-size: 0.9rem;
}

.rate-summary-item {
  margin-bottom: 0.5rem;
  text-shadow: 0 0 5px currentColor;
}

.rate-summary-item.highest {
  color: #0ff;
}

.rate-summary-item.lowest {
  color: #f0f;
}

.icon-glow {
  color: #f0f;
  filter: drop-shadow(0 0 5px #f0f);
}

.chart-container {
  height: 200px;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  margin-top: 1rem;
  border: 1px solid rgba(255, 0, 255, 0.3);
}

.card-footer {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  color: #0ff;
  font-size: 0.9rem;
  text-shadow: 0 0 5px #0ff;
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

.deposit-list {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 16px;
  padding-bottom: 2rem;
}

.deposit-list::-webkit-scrollbar {
  width: 8px;
}

.deposit-list::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 10px;
}

.deposit-list::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 10px;
  box-shadow: 0 0 10px #f0f;
}

.deposit-list::-webkit-scrollbar-thumb:hover {
  background: #f0f;
  box-shadow: 0 0 15px #f0f;
}
.inventory-btn {
  background: transparent;
  border: 2px solid #f0f;
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  /* font-family: 'DungGeunMo'; */
  transition: all 0.3s ease;
  margin-left: 1rem;
  white-space: nowrap;  /* 텍스트가 줄바꿈되지 않도록 */
}

.inventory-btn:hover {
  background: rgba(255, 0, 255, 0.2);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
}

.inventory-btn.added {
  background: #f0f;
  border-color: #fff;
  animation: pulse 1s infinite;
}

.inventory-btn.added:hover {
  background: #ff3366;  /* 삭제 동작을 암시하는 빨간색 계열로 변경 */
}

.inventory-icon {
  color: #f0f;
}

.inventory-btn.added .inventory-icon {
  color: #fff;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 0, 255, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 0, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 0, 255, 0);
  }
}

@media (max-width: 768px) {
  .cyber-filters {
    flex-direction: column;
  }
  
  .chart-container {
    height: 150px;
  }

  .card-header {
    flex-direction: column;
    gap: 1rem;
  }

  .rate-summary {
    border-left: none;
    border-top: 2px solid #f0f;
    padding-left: 0;
    padding-top: 1rem;
    width: 100%;
  }

  .glitch-text {
    font-size: 2rem;
  }
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-content {
  color: #f0f;
  font-size: 2rem;
  /* font-family: 'DungGeunMo'; */
  text-shadow: 0 0 10px #f0f;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
</style>