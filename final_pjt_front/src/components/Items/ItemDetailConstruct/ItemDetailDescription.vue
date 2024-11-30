<template>
  <div class="arcade-detail-container">
    <div class="product-info">
      <div class="cyber-title" data-text="ITEM DETAILS">ITEM Description</div>
      <div class="info-grid">
        <div class="info-section">
          <h2 class="section-title">{{ product.kor_co_nm }}</h2>
          <h3 class="item-name">{{ product.fin_prdt_nm }}</h3>
          
          <div class="stats-box">
            <div class="stat-item description">
              <span class="stat-label">아이템 설명</span>
              <span class="stat-value">{{ product.etc_note || '설명 없음' }}</span>
            </div>
          </div>
        </div>

        <!-- 차트 섹션 -->
        <div class="chart-section">
          <div class="chart-title">금리 정보</div>
          <div class="chart-container">
            <Bar
              :data="chartData"
              :options="chartOptions"
            />
          </div>
        </div>
      </div>

      <!-- 상품 옵션 정보 -->
      <div v-if="options.length > 0" class="options-grid">
        <div class="option-card" v-for="option in filteredOptions" :key="option.save_trm">
          <div class="option-header">{{ option.save_trm }}개월</div>
          <div class="option-stats">
            <!-- 수정 모드 -->
            <div v-if="option.isEditing" class="edit-mode"  @keyup.enter="updateIntr(option)">
              <div class="edit-field">
                <span class="stat-label">기본금리</span>
                <input 
                  v-model="option.intr_rate" 
                  type="number" 
                  step="0.01" 
                  class="cyber-input"
                />
              </div>
              <div class="edit-field">
                <span class="stat-label">우대금리</span>
                <input 
                  v-model="option.intr_rate2" 
                  type="number" 
                  step="0.01" 
                  class="cyber-input"
                />
              </div>
              <div class="edit-buttons">
                <button @click="updateIntr(option)" class="cyber-button save">저장</button>
                <button @click="cancelEdit(option)" class="cyber-button cancel">취소</button>
              </div>
            </div>
            <!-- 표시 모드 -->
            <div v-else class="display-mode">
              <div class="option-stat">
                <span class="stat-label">기본금리</span>
                <span class="stat-value">{{ option.intr_rate }}%</span>
              </div>
              <div class="option-stat">
                <span class="stat-label">우대금리</span>
                <span class="stat-value highlight">{{ option.intr_rate2 }}%</span>
              </div>
              <button
                v-if="is_superuser === 'true'" 
                @click="editIntr(option)" 
                class="cyber-button edit"
              >
                금리 수정
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
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

const route = useRoute()
const product = ref({})
const options = ref([])
const is_superuser = ref(localStorage.getItem('is_superuser'))

// 6개월 이상인 옵션만 필터링
const filteredOptions = computed(() => {
  return options.value.filter(option => option.save_trm >= 6)
})

// 차트 데이터
const chartData = computed(() => ({
  labels: filteredOptions.value.map(opt => `${opt.save_trm}개월`),
  datasets: [
    {
      label: '기본금리',
      data: filteredOptions.value.map(opt => opt.intr_rate),
      backgroundColor: 'rgba(74, 222, 128, 0.8)',
      borderColor: '#4ade80',
      borderWidth: 1
    },
    {
      label: '우대금리',
      data: filteredOptions.value.map(opt => opt.intr_rate2),
      backgroundColor: 'rgba(255, 0, 255, 0.8)',
      borderColor: '#f0f',
      borderWidth: 1
    }
  ]
}))

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
          family: 'DungGeunMo'
        }
      }
    }
  }
}

const formatJoinPeriod = (joinPeriod) => {
  if (joinPeriod) {
    return `${joinPeriod}개월`
  }
  return '정보 없음'
}

const editIntr = (option) => {
  option.isEditing = true
}

const updateIntr = async (option) => {
  try {
    await axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/finlife/update_intr/',
      params: {
        option_id: option.id,
        intr_rate: option.intr_rate,
        intr_rate2: option.intr_rate2
      }
    })
    await fetchProductDetails(option.fin_prdt_cd)
    option.isEditing = false
  } catch (error) {
    console.error('금리 업데이트 실패:', error)
  }
}

const cancelEdit = async (option) => {
  option.isEditing = false
  await fetchProductDetails(option.fin_prdt_cd)
}

const fetchProductDetails = async (fin_prdt_cd) => {
  try {
    const [productRes, optionsRes] = await Promise.all([
      axios.get(`http://127.0.0.1:8000/finlife/deposit_product_detail/${fin_prdt_cd}`),
      axios.get(`http://127.0.0.1:8000/finlife/deposit-products-options/${fin_prdt_cd}`)
    ])
    
    product.value = productRes.data
    options.value = optionsRes.data
  } catch (error) {
    console.error('상품 데이터 불러오기 실패:', error)
  }
}

onMounted(() => {
  const fin_prdt_cd = route.params.fin_prdt_cd
  fetchProductDetails(fin_prdt_cd)
})
</script>

<style scoped>
.arcade-detail-container {
  padding: 2rem;
  color: #fff;
  font-family: 'DungGeunMo', sans-serif;
  max-height: 100vh;
  overflow-y: auto;
}

.arcade-detail-container::-webkit-scrollbar {
  width: 10px;
}

.arcade-detail-container::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
}

.arcade-detail-container::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 5px;
}

.arcade-detail-container::-webkit-scrollbar-thumb:hover {
  background: #ff00ff99;
}

.product-info {
  max-width: 1400px; /* 최대 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 */
  width: 100%;
}

.cyber-title {
  font-size: 2rem;
  color: #f0f;
  text-align: center;
  margin-bottom: 2rem;
  text-shadow: 2px 2px #0ff;
  position: relative;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.section-title {
  color: #f0f;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.item-name {
  color: #0ff;
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}

.stats-box {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
}

.stat-item {
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-bottom: 1px solid rgba(255, 0, 255, 0.2);
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  display: block;
  color: #f0f;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.stat-value {
  color: #fff;
  font-size: 1.1rem;
}

.description .stat-value {
  font-size: 0.9rem;
  line-height: 1.4;
}

.chart-section {
  background: rgba(255, 0, 255, 0.05);
  border-radius: 8px;
  padding: 1rem;
}

.chart-title {
  color: #f0f;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  text-align: center;
}

.chart-container {
  height: 300px;
  position: relative;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* 최소 너비를 250px에서 200px로 줄임 */
  gap: 1.5rem; /* 갭을 1rem에서 1.5rem으로 늘려 간격 확보 */
  margin-top: 2rem;
  padding-bottom: 2rem; /* 하단 여백 추가 */
}

.option-card {
  background: rgba(255, 0, 255, 0.1);
  border: 1px solid #f0f;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.3s ease;
  min-height: 200px; /* 최소 높이 설정 */
  display: flex; /* Flexbox 사용 */
  flex-direction: column; /* 세로 방향으로 정렬 */
}

.option-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
}

.option-header {
  color: #fff;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  text-align: center;
  flex-shrink: 0; /* 헤더 크기 고정 */
}

.option-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex-grow: 1; /* 남은 공간 채우기 */
}

.option-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  border-bottom: 1px solid rgba(255, 0, 255, 0.2);
}

.highlight {
  color: #0ff;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
}

.cyber-button {
  width: 100%;
  padding: 0.5rem 1rem;
  margin-top: 0.5rem;
  border: 1px solid;
  border-radius: 4px;
  font-family: 'DungGeunMo', sans-serif;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cyber-button.edit {
  background: rgba(255, 0, 255, 0.2);
  border-color: #f0f;
  color: #f0f;
}

.cyber-button.save {
  background: rgba(0, 255, 255, 0.2);
  border-color: #0ff;
  color: #0ff;
}

.cyber-button.cancel {
  background: rgba(255, 0, 0, 0.2);
  border-color: #f00;
  color: #f00;
}

.cyber-button:hover {
  box-shadow: 0 0 10px currentColor;
  transform: translateY(-1px);
}

.cyber-input {
  width: 100%;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid #f0f;
  border-radius: 4px;
  color: #fff;
  font-family: 'DungGeunMo', sans-serif;
  margin-bottom: 0.5rem;
}

.cyber-input:focus {
  outline: none;
  box-shadow: 0 0 10px #f0f;
}

.edit-mode {
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.edit-field {
  margin-bottom: 0.5rem;
}

.edit-buttons {
  display: grid;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 200px;
  }

  .options-grid {
    grid-template-columns: 1fr;
  }
}
</style>