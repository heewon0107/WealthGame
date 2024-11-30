<template>
  <div class="arcade-signup-container">
    <!-- 배경 효과 -->
    <div class="stars"></div>
    <div class="twinkling"></div>
    
    <div class="arcade-cabinet">
      <div class="screen-frame">
        <div class="screen-overlay"></div>
        <div class="screen-content">
          <div class="glitch-title" data-text="NEW PLAYER">NEW PLAYER</div>
          
          <form @submit.prevent="handleSubmit" class="signup-form">
            <!-- 기본 정보 섹션 -->
            <div class="form-section">
              <div class="section-title">BASIC INFO</div>
              
              <div class="input-group">
                <label for="username" class="cyber-label">USER ID:</label>
                <input
                  type="text"
                  id="username"
                  v-model="formData.username"
                  class="cyber-input"
                  placeholder="ENTER YOUR ID"
                  required
                />
                <div class="input-line"></div>
              </div>

              <div class="input-group">
                <label for="email" class="cyber-label">EMAIL:</label>
                <input
                  type="email"
                  id="email"
                  v-model="formData.email"
                  class="cyber-input"
                  placeholder="ENTER YOUR EMAIL"
                  required
                />
                <div class="input-line"></div>
              </div>

              <div class="input-group">
                <label for="password" class="cyber-label">PASSWORD:</label>
                <input
                  type="password"
                  id="password"
                  v-model="formData.password"
                  class="cyber-input"
                  placeholder="ENTER YOUR PASSWORD"
                  required
                />
                <div class="input-line"></div>
              </div>

              <div class="input-group">
                <label for="nickname" class="cyber-label">NICKNAME:</label>
                <input
                  type="text"
                  id="nickname"
                  v-model="formData.nickname"
                  class="cyber-input"
                  placeholder="ENTER YOUR NICKNAME"
                />
                <div class="input-line"></div>
              </div>

              <div class="input-group">
                <label for="age" class="cyber-label">AGE:</label>
                <input
                  type="number"
                  id="age"
                  v-model="formData.age"
                  class="cyber-input"
                  placeholder="ENTER YOUR AGE"
                />
                <div class="input-line"></div>
              </div>
            </div>

            <!-- 슬라이더 섹션 -->
            <div class="form-section">
              <div class="section-title">PLAYER STATS</div>
              
              <!-- Assets Slider -->
              <div class="slider-group">
                <div class="slider-header">
                  <label class="cyber-label">ASSETS</label>
                  <div class="slider-value">₩ {{ formatNumber(formData.assets) }}</div>
                </div>
                <div class="range-info">₩1,000,000 ~ ₩1,000,000,000</div>
                <div class="slider-container">
                  <input
                    type="range"
                    v-model="formData.assets"
                    min="1000000"
                    max="1000000000"
                    step="1000000"
                    class="cyber-range"
                  />
                  <div class="range-track"></div>
                </div>
              </div>

              <!-- Annual Income Slider -->
              <div class="slider-group">
                <div class="slider-header">
                  <label class="cyber-label">ANNUAL INCOME</label>
                  <div class="slider-value">₩ {{ formatNumber(formData.annual_income) }}</div>
                </div>
                <div class="range-info">₩1,000,000 ~ ₩100,000,000</div>
                <div class="slider-container">
                  <input
                    type="range"
                    v-model="formData.annual_income"
                    min="1000000"
                    max="100000000"
                    step="1000000"
                    class="cyber-range"
                  />
                  <div class="range-track"></div>
                </div>
              </div>

              <!-- Investment Amount Slider -->
              <div class="slider-group">
                <div class="slider-header">
                  <label class="cyber-label">INVESTMENT AMOUNT</label>
                  <div class="slider-value">₩ {{ formatNumber(formData.desired_amount) }}</div>
                </div>
                <div class="range-info">₩1,000,000 ~ ₩1,000,000,000</div>
                <div class="slider-container">
                  <input
                    type="range"
                    v-model="formData.desired_amount"
                    min="1000000"
                    max="1000000000"
                    step="1000000"
                    class="cyber-range"
                  />
                  <div class="range-track"></div>
                </div>
              </div>

              <!-- Target Period Slider -->
              <div class="input-group">
                <div class="slider-header">
                  <label class="cyber-label">TARGET PERIOD</label>
                </div>
                <select 
                  v-model="formData.desired_period" 
                  class="cyber-select"
                >
                  <option value="6">6 MONTHS</option>
                  <option value="12">12 MONTHS</option>
                  <option value="24">24 MONTHS</option>
                  <option value="36">36 MONTHS</option>
                </select>
              </div>
            </div>

            <button type="submit" class="neon-button">
              <span class="button-line"></span>
              <span class="button-line"></span>
              <span class="button-text">CREATE PLAYER</span>
              <span class="button-line"></span>
              <span class="button-line"></span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref,watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const periodList = "periodList";

const formData = ref({
  username: '',
  email: '',
  password: '',
  nickname: '',
  age: '',
  assets: 1000000,
  annual_income: 1000000,
  desired_amount: 100000,
  desired_period: 6,
});

const formatNumber = (value) => {
  return new Intl.NumberFormat('ko-KR').format(value);
};

const handleSubmit = async () => {
  try {
    const registerResponse = await axios.post('http://127.0.0.1:8000/accounts/register/', formData.value);
    const loginResponse = await axios.post('http://127.0.0.1:8000/accounts/login/', {
      email: formData.value.email,
      password: formData.value.password,
    });
    const token = loginResponse.data.token;
    localStorage.setItem('token', token);
    localStorage.setItem('is_superuser', loginResponse.data.is_superuser);  // user 정보를 저장
    localStorage.setItem('user_id', loginResponse.data.user_id)
    localStorage.setItem('userTier', loginResponse.data.userTier)
    authStore.setLoginStatus(true);
    router.push({ name: 'StartView' });
  } catch (error) {
    console.error('회원가입 또는 로그인 실패:', error);
    alert('회원가입에 실패했습니다. 입력 정보를 확인해주세요.');
  }
  
};
watch(() => formData.value.desired_period, (newValue) => {
  const validPeriods = [6, 12, 24, 36];
  const closest = validPeriods.reduce((prev, curr) => {
    return (Math.abs(curr - newValue) < Math.abs(prev - newValue) ? curr : prev);
  });
  formData.value.desired_period = closest;
});
</script>

<style scoped>

.arcade-signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #000;
  position: relative;
  overflow: hidden;
  padding: 40px 20px;
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

.arcade-cabinet {
  position: relative;
  z-index: 2;
  width: 800px;
  max-width: 90%;
  max-height: 90vh; /* 최대 높이 제한 */
  padding: 40px;
  background: rgba(26, 26, 26, 0.9);
  border: 4px solid #f0f;
  border-radius: 20px;
  box-shadow: 
    0 0 20px #f0f,
    inset 0 0 40px rgba(255, 0, 255, 0.3);
  overflow: hidden; /* 내부 스크롤을 위해 필요 */
}

.screen-frame {
  position: relative;
  padding: 20px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 10px;
  overflow-y: auto; /* 세로 스크롤 추가 */
  max-height: calc(80vh - 80px); /* 캐비닛 패딩을 고려한 높이 */
}
/* 스크롤바 스타일 개선 */
.screen-frame::-webkit-scrollbar {
  width: 12px;
  background: rgba(0, 0, 0, 0.3);
}

.screen-frame::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 6px;
  margin: 5px;
}

.screen-frame::-webkit-scrollbar-thumb {
  background: linear-gradient(45deg, #f0f, #0ff);
  border-radius: 6px;
  border: 3px solid rgba(0, 0, 0, 0.2);
  background-clip: padding-box;
}

.screen-frame::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(45deg, #0ff, #f0f);
}

/* 스캔라인 효과가 스크롤과 함께 움직이도록 수정 */
.screen-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

/* 모바일 반응형 조정 */
@media (max-width: 768px) {
  .arcade-cabinet {
    padding: 20px;
    max-height: 85vh;
  }

  .screen-frame {
    max-height: calc(75vh - 40px);
    padding: 15px;
  }
}
.screen-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(
    0deg,
    rgba(255, 0, 255, 0.03) 0px,
    rgba(255, 0, 255, 0.03) 1px,
    transparent 1px,
    transparent 2px
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
  position: relative;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.form-section {
  background: rgba(255, 0, 255, 0.05);
  padding: 20px;
  border-radius: 10px;
  border: 1px solid rgba(255, 0, 255, 0.2);
}

.section-title {
  font-family: 'DungGeunMo', monospace;
  color: #f0f;
  font-size: 1.5rem;
  margin-bottom: 20px;
  text-shadow: 0 0 10px #f0f;
  text-align: center;
}

.input-group {
  position: relative;
  margin-bottom: 20px;
}

.cyber-label {
  font-family: 'DungGeunMo', monospace;
  color: #f0f;
  font-size: 1rem;
  margin-bottom: 8px;
  display: block;
  text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

.cyber-input {
  width: 100%;
  padding: 12px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid #f0f;
  border-radius: 5px;
  color: #fff;
  font-family: 'DungGeunMo', monospace;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.cyber-input:focus {
  outline: none;
  border-color: #0ff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.slider-group {
  margin-bottom: 25px;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}


.slider-value {
  color: #0ff;
  font-family: 'DungGeunMo';
  text-align: right;
  min-width: 120px; 
}

.range-info {
  color: rgba(255, 0, 255, 0.7);
  font-size: 0.8rem;
  margin-bottom: 10px;
  font-family: 'DungGeunMo', monospace;
}

.slider-container {
  position: relative;
  padding: 10px 0;
  height: 30px; 
  display: flex;
  align-items: center; 
}

.cyber-range {
  -webkit-appearance: none;
  width: 100%;
  height: 2px;
  background: transparent;
  position: relative;
  z-index: 2;
  margin: 0; 
}

.cyber-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: #f0f;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 10px #f0f;
  transition: all 0.3s ease;
  margin-top: -9px; 
}

.cyber-range::-webkit-slider-runnable-track {
  width: 100%;
  height: 2px;
  background: transparent;
  border: none;
}

.cyber-range::-webkit-slider-thumb:hover {
  background: #0ff;
  box-shadow: 0 0 15px #0ff;
  transform: scale(1.2);
}



.range-track {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #f0f, #0ff);
  transform: translateY(-50%);
  pointer-events: none; /* 클릭 이벤트 방지 */
}

.neon-button {
  position: relative;
  padding: 15px 30px;
  background: transparent;
  border: none;
  color: #fff;
  font-family: 'DungGeunMo', monospace;
  font-size: 1.2rem;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.button-text {
  position: relative;
  z-index: 1;
  text-shadow: 0 0 10px #f0f;
}

.button-line {
  position: absolute;
  background: #f0f;
}

.button-line:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  transform: translateX(-100%);
  animation: line-anim 2s linear infinite;
}

.button-line:nth-child(2) {
  top: 0;
  right: 0;
  width: 2px;
  height: 100%;
  transform: translateY(-100%);
  animation: line-anim 2s linear infinite 0.5s;
}

.button-line:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  transform: translateX(100%);
  animation: line-anim 2s linear infinite 1s;
}
.button-line:nth-child(4) {
  bottom: 0;
  left: 0;
  width: 2px;
  height: 100%;
  transform: translateY(100%);
  animation: line-anim 2s linear infinite 1.5s;
}

@keyframes line-anim {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes scan-line {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

@keyframes move-twinkle {
  from { background-position: 0 0; }
  to { background-position: -10000px 5000px; }
}

@keyframes glitch {
  0% { text-shadow: 2px 2px #0ff, -2px -2px #f00; }
  25% { text-shadow: -2px 2px #0ff, 2px -2px #f00; }
  50% { text-shadow: 2px -2px #0ff, -2px 2px #f00; }
  75% { text-shadow: -2px -2px #0ff, 2px 2px #f00; }
  100% { text-shadow: 2px 2px #0ff, -2px -2px #f00; }
}

/* 스크롤바 스타일링 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 4px;
  box-shadow: 0 0 10px #f0f;
}

::-webkit-scrollbar-thumb:hover {
  background: #0ff;
  box-shadow: 0 0 15px #0ff;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .arcade-cabinet {
    padding: 20px;
  }

  .glitch-title {
    font-size: 2rem;
  }

  .section-title {
    font-size: 1.2rem;
  }

  .cyber-label {
    font-size: 0.9rem;
  }

  .cyber-input {
    font-size: 0.9rem;
    padding: 8px;
  }

  .neon-button {
    padding: 12px 24px;
    font-size: 1rem;
  }
}

.loading-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 40px;
}

.cyber-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f0f;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.cyber-select {
  width: 100%;
  padding: 12px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid #f0f;
  border-radius: 5px;
  color: #fff;
  font-family: 'DungGeunMo';
  cursor: pointer;
  transition: all 0.3s ease;
}

.cyber-select:focus {
  outline: none;
  border-color: #0ff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.cyber-select option {
  background: #000;
  color: #fff;
  padding: 10px;
}

.cyber-select:hover {
  border-color: #0ff;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.loading-text {
  color: #f0f;
  font-family: 'DungGeunMo';
  animation: pulse 1.5s ease infinite;
}

/* 애니메이션 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes move-twinkle {
  from { background-position: 0 0; }
  to { background-position: -10000px 5000px; }
}

@keyframes glitch {
  0% { text-shadow: 2px 2px #0ff, -2px -2px #f00; }
  25% { text-shadow: -2px 2px #0ff, 2px -2px #f00; }
  50% { text-shadow: 2px -2px #0ff, -2px 2px #f00; }
  75% { text-shadow: -2px -2px #0ff, 2px 2px #f00; }
  100% { text-shadow: 2px 2px #0ff, -2px -2px #f00; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .profile-terminal {
    padding: 20px;
  }

  .glitch-title {
    font-size: 1.8rem;
  }

  .button-group {
    flex-direction: column;
  }

  .cyber-button {
    width: 100%;
  }
}

</style>