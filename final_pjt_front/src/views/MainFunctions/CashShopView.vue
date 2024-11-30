<template>
  <div class="arcade-exchange-container">
    <!-- 배경 효과 -->
    <div class="stars"></div>
    <div class="twinkling"></div>
    <FallingCoins />
    
    <!-- 메인 컨텐트 -->
    <div class="exchange-cabinet">
      <div class="screen-frame">
        <div class="screen-overlay"></div>
        <div class="screen-content">
          <ExchangeTips />
          <div class="glitch-title" data-text="MONEY EXCHANGER">MONEY EXCHANGER</div>
          
          <div class="calculator-grid">
            <!-- 한국 → 외화 섹션 -->
            <div class="cyber-card">
              <div class="card-header">
                <div class="neon-text">KRW → FOREIGN</div>
              </div>
              <div class="card-content">
                <div class="input-group">
                  <label class="cyber-label">KRW AMOUNT:</label>
                  <input
                    type="number"
                    v-model.number="krwAmount"
                    class="cyber-input"
                    placeholder="ENTER KRW"
                    @input="calculateKrwToForeign"
                  />
                  <div class="input-line"></div>
                </div>

                <div class="input-group">
                  <label class="cyber-label">TARGET CURRENCY:</label>
                  <select
                    v-model="selectedCurrency1"
                    class="cyber-select"
                    @change="calculateKrwToForeign"
                  >
                    <option
                      v-for="currency in exchangeRateList"
                      :key="currency.cur_unit"
                      :value="currency.cur_unit"
                    >
                      {{ currency.cur_nm }} ({{ currency.cur_unit }})
                    </option>
                  </select>
                  <div class="select-line"></div>
                </div>

                <div class="result-display" v-if="krwToForeignAmount !== null">
                  <div class="result-value">
                    {{ krwToForeignAmount.toFixed(2) }}
                    {{ selectedCurrency1 }}
                  </div>
                </div>
              </div>
            </div>

            <!-- 외화 → 한국 섹션 -->
            <div class="cyber-card">
              <div class="card-header">
                <div class="neon-text">FOREIGN → KRW</div>
              </div>
              <div class="card-content">
                <div class="input-group">
                  <label class="cyber-label">FOREIGN AMOUNT:</label>
                  <input
                    type="number"
                    v-model.number="foreignAmount"
                    class="cyber-input"
                    placeholder="ENTER AMOUNT"
                    @input="calculateForeignToKrw"
                  />
                  <div class="input-line"></div>
                </div>

                <div class="input-group">
                  <label class="cyber-label">SOURCE CURRENCY:</label>
                  <select
                    v-model="selectedCurrency2"
                    class="cyber-select"
                    @change="calculateForeignToKrw"
                  >
                    <option
                      v-for="currency in exchangeRateList"
                      :key="currency.cur_unit"
                      :value="currency.cur_unit"
                    >
                      {{ currency.cur_nm }} ({{ currency.cur_unit }})
                    </option>
                  </select>
                  <div class="select-line"></div>
                </div>

                <div class="result-display" v-if="foreignToKrwAmount !== null">
                  <div class="result-value">
                    {{ foreignToKrwAmount.toFixed(2) }} KRW
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import FallingCoins from '@/components/FallingCoins.vue';
import ExchangeTips from '@/components/ExchangeTips.vue';

const exchangeRateList = ref([]);
const krwAmount = ref(0);
const foreignAmount = ref(0);
const selectedCurrency1 = ref('USD');
const selectedCurrency2 = ref('USD');
const krwToForeignAmount = ref(null);
const foreignToKrwAmount = ref(null);

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/exchange/today_exchange/');
    exchangeRateList.value = res.data;
  } catch (err) {
    console.error('환율 데이터 요청 오류:', err);
  }
});

const calculateKrwToForeign = () => {
  if (krwAmount.value <= 0 || exchangeRateList.value.length === 0) {
    krwToForeignAmount.value = null;
    return;
  }

  const selectedCurrencyData = exchangeRateList.value.find(
    (currency) => currency.cur_unit === selectedCurrency1.value
  );

  if (selectedCurrencyData) {
    const selectedRate = parseFloat(selectedCurrencyData.ttb.replace(/,/g, ''));
    if (!isNaN(selectedRate)) {
      krwToForeignAmount.value = krwAmount.value / selectedRate;
    } else {
      krwToForeignAmount.value = null;
    }
  } else {
    krwToForeignAmount.value = null;
  }
};

const calculateForeignToKrw = () => {
  if (foreignAmount.value <= 0 || exchangeRateList.value.length === 0) {
    foreignToKrwAmount.value = null;
    return;
  }

  const selectedCurrencyData = exchangeRateList.value.find(
    (currency) => currency.cur_unit === selectedCurrency2.value
  );

  if (selectedCurrencyData) {
    const selectedRate = parseFloat(selectedCurrencyData.ttb.replace(/,/g, ''));
    if (!isNaN(selectedRate)) {
      foreignToKrwAmount.value = foreignAmount.value * selectedRate;
    } else {
      foreignToKrwAmount.value = null;
    }
  } else {
    foreignToKrwAmount.value = null;
  }
};
</script>

<style scoped>
.arcade-exchange-container {
  min-height: 90vh;
  background: #000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* 배경 효과 */
.stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000 url('/stars.png') repeat;
  z-index: 0;
}

.twinkling {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: transparent url('/twinkling.png') repeat;
  animation: move-twinkle 200s linear infinite;
  opacity: 0.5;
  z-index: 1;
}

.exchange-cabinet {
  position: relative;
  z-index: 2;
  width: 90%;
  max-width: 1200px;
  padding: 40px;
  background: rgba(26, 26, 26, 0.9);
  border: 4px solid #f0f;
  border-radius: 20px;
  box-shadow: 
    0 0 20px #f0f,
    inset 0 0 40px rgba(255, 0, 255, 0.3);
}

.screen-frame {
  position: relative;
  padding: 20px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  overflow: hidden;
}

.screen-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    transparent 0%,
    rgba(255, 0, 255, 0.1) 50%,
    transparent 100%
  );
  animation: scan-line 8s linear infinite;
  pointer-events: none;
}

.screen-content {
  position: relative;
  z-index: 3;
  padding: 20px;
}

.glitch-title {
  font-family: 'DungGeunMo', monospace;
  font-size: 3rem;
  color: #f0f;
  text-align: center;
  margin-bottom: 40px;
  text-shadow:
    2px 2px #0ff,
    -2px -2px #f00;
  animation: glitch 1s infinite;
}

.calculator-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.cyber-card {
  background: rgba(255, 0, 255, 0.05);
  border: 2px solid #f0f;
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.cyber-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
}

.card-header {
  background: linear-gradient(45deg, #f0f, #90f);
  padding: 15px;
  text-align: center;
}

.neon-text {
  font-family: 'DungGeunMo', monospace;
  color: #fff;
  font-size: 1.5rem;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
}

.card-content {
  padding: 20px;
}

.input-group {
  margin-bottom: 20px;
}

.cyber-label {
  display: block;
  color: #f0f;
  font-family: 'DungGeunMo', monospace;
  margin-bottom: 8px;
  text-shadow: 0 0 5px rgba(255, 0, 255, 0.5);
}

.cyber-input,
.cyber-select {
  width: 100%;
  padding: 10px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid #f0f;
  border-radius: 5px;
  color: #fff;
  font-family: 'DungGeunMo', monospace;
  transition: all 0.3s ease;
}

.cyber-input:focus,
.cyber-select:focus {
  outline: none;
  border-color: #0ff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.result-display {
  background: rgba(255, 0, 255, 0.1);
  padding: 15px;
  border-radius: 5px;
  margin-top: 20px;
  text-align: center;
}

.result-value {
  font-family: 'DungGeunMo', monospace;
  color: #0ff;
  font-size: 1.5rem;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

@keyframes move-twinkle {
  from { background-position: 0 0; }
  to { background-position: -10000px 5000px; }
}

@keyframes scan-line {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

@keyframes glitch {
  0% { text-shadow: 2px 2px #0ff, -2px -2px #f00; }
  25% { text-shadow: -2px 2px #0ff, 2px -2px #f00; }
  50% { text-shadow: 2px -2px #0ff, -2px 2px #f00; }
  75% { text-shadow: -2px -2px #0ff, 2px 2px #f00; }
  100% { text-shadow: 2px 2px #0ff, -2px -2px #f00; }
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .exchange-cabinet {
    padding: 20px;
    width: 95%;
  }

  .glitch-title {
    font-size: 2rem;
  }

  .neon-text {
    font-size: 1.2rem;
  }

  .result-value {
    font-size: 1.2rem;
  }

  .calculator-grid {
    grid-template-columns: 1fr;
  }

  .card-content {
    padding: 15px;
  }
}

/* 입력 필드 스타일 */
.input-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #f0f, #0ff);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.cyber-input:focus + .input-line,
.cyber-select:focus + .select-line {
  transform: scaleX(1);
}

/* 셀렉트 박스 스타일 */
.select-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #f0f, #0ff);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

/* 호버 효과 강화 */
.cyber-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 
    0 0 20px rgba(255, 0, 255, 0.4),
    0 0 40px rgba(255, 0, 255, 0.2);
}

.cyber-card:hover .neon-text {
  text-shadow: 
    0 0 15px rgba(255, 255, 255, 1),
    0 0 30px rgba(255, 255, 255, 0.5),
    0 0 45px rgba(255, 255, 255, 0.3);
}

.result-display:hover {
  transform: scale(1.02);
  transition: transform 0.3s ease;
}

.result-display:hover .result-value {
  color: #fff;
  text-shadow: 
    0 0 10px #0ff,
    0 0 20px #0ff,
    0 0 30px #0ff,
    0 0 40px rgba(0, 255, 255, 0.5);
}

/* 애니메이션 성능 최적화 */
.coin, 
.screen-overlay,
.glitch-title {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* 스크린 오버레이 강화 */
.screen-overlay {
  background: linear-gradient(
    transparent 0%,
    rgba(255, 0, 255, 0.1) 50%,
    transparent 100%
  );
  mix-blend-mode: overlay;
}

/* 글로벌 트랜지션 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 폰트 최적화 */
@font-face {
  font-family: 'DungGeunMo';
  font-display: swap;
  src: url('/fonts/DungGeunMo.woff2') format('woff2');
}

</style>