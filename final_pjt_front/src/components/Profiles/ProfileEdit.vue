<template>
  <div class="cyber-profile-container">
    <!-- 배경 효과 -->
    <div class="stars"></div>
    <div class="twinkling"></div>
    
    <div class="profile-terminal">
      <div class="terminal-header">
        <div class="glitch-title" data-text="PROFILE UPDATE">PROFILE UPDATE</div>
      </div>

      <div v-if="userInfo" class="terminal-content">
        <form @submit.prevent="updateProfile" class="cyber-form">
          <!-- 기본 정보 섹션 -->
          <div class="form-section">
            <div class="section-title">BASIC INFO</div>
            
            <div class="input-group">
              <label class="cyber-label">NICKNAME:</label>
              <input
                type="text"
                v-model="formData.nickname"
                class="cyber-input"
                required
              />
            </div>

            <div class="input-group">
              <label class="cyber-label">AGE:</label>
              <input
                type="number"
                v-model="formData.age"
                class="cyber-input"
                required
              />
            </div>

            <div class="input-group">
              <label class="cyber-label">EMAIL:</label>
              <input
                type="email"
                v-model="formData.email"
                class="cyber-input"
                required
              />
            </div>
          </div>

          <!-- 자산 정보 섹션 -->
          <div class="form-section">
            <div class="section-title">FINANCIAL STATUS</div>
            
            <div class="slider-group">
              <div class="slider-header">
                <label class="cyber-label">ANNUAL INCOME</label>
                <div class="slider-value">₩ {{ formatNumber(formData.annual_income) }}</div>
              </div>
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

            <div class="slider-group">
              <div class="slider-header">
                <label class="cyber-label">ASSETS</label>
                <div class="slider-value">₩ {{ formatNumber(formData.assets) }}</div>
              </div>
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

            <div class="slider-group">
              <div class="slider-header">
                <label class="cyber-label">TARGET AMOUNT</label>
                <div class="slider-value">₩ {{ formatNumber(formData.desired_amount) }}</div>
              </div>
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

            <div class="input-group">
              <div class="slider-header">
                <label class="cyber-label">TARGET PERIOD</label>
                <div class="slider-value">{{ formData.desired_period }} MONTHS</div>
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

          <!-- 버튼 그룹 -->
          <div class="button-group">

            <button type="submit" class="cyber-button" :disabled="isSubmitting">
              <span class="button-effect"></span>
              <span v-if="isSubmitting" class="cyber-spinner"></span>
              SAVE
            </button>
          </div>
        </form>

        <!-- 알림 메시지 -->
        <div v-if="message" :class="['cyber-alert', message.type]">
          {{ message.text }}
        </div>
      </div>

      <!-- 로딩 화면 -->
      <div v-else class="loading-screen">
        <div class="cyber-spinner"></div>
        <div class="loading-text">LOADING DATA...</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const userInfo = ref(null);
const formData = ref({
  nickname: '',
  age: '',
  email: '',
  annual_income: 1000000,
  assets: 1000000,
  desired_amount: 1000000,
  desired_period: 6
});
const isSubmitting = ref(false);
const message = ref(null);

// 숫자 포맷팅
const formatNumber = (value) => {
  return new Intl.NumberFormat('ko-KR').format(value);
};

// 초기 데이터 로드
const loadUserInfo = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://127.0.0.1:8000/accounts/profile_view/', {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    userInfo.value = response.data;
    formData.value = { ...response.data };
  } catch (error) {
    console.error('Error loading user info:', error);
    message.value = {
      type: 'error',
      text: 'Failed to load profile information'
    };
  }
};

// 프로필 업데이트
const updateProfile = async () => {
  isSubmitting.value = true;
  message.value = null;

  try {
    const token = localStorage.getItem('token');
    const response = await axios.put(
      'http://127.0.0.1:8000/accounts/profile_view/',
      formData.value,
      {
        headers: {
          'Authorization': `Token ${token}`
        }
      }
    );
    userInfo.value = response.data;
    message.value = {
      type: 'success',
      text: 'Profile updated successfully!'
    };
    router.push({ name: 'ProfileView' });
  } catch (error) {
    console.error('Error updating profile:', error);
    message.value = {
      type: 'error',
      text: 'Failed to update profile'
    };
  } finally {
    isSubmitting.value = false;
  }
};


// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  loadUserInfo();
});
</script>

<style scoped>
.cyber-profile-container {
  min-height: 100vh;
  background: #000;
  display: flex;
  justify-content: center;
  align-items: flex-start; /* center에서 flex-start로 변경 */
  padding: 40px 20px;
  position: relative;
  overflow-y: auto; /* 스크롤 추가 */
  overflow-x: hidden;
}

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

.profile-terminal {
  position: relative;
  z-index: 2;
  width: 900px;
  max-width: 95%;
  background: rgba(0, 0, 0, 0.9);
  border: 3px solid #f0f;
  border-radius: 20px;
  padding: 30px;
  margin: 20px auto; /* 여백 추가 */
  box-shadow: 
    0 0 20px #f0f,
    inset 0 0 40px rgba(255, 0, 255, 0.3);
}
/* 스크롤바 스타일링 추가 */

.terminal-content {
  max-height: calc(70vh - 100px); /* 터미널 내부 콘텐츠 최대 높이 설정 */
  overflow-y: auto; /* 내부 스크롤 추가 */
}

.terminal-content::-webkit-scrollbar {
  width: 8px;
}

.terminal-content::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 4px;
}

.terminal-content::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 4px;
  box-shadow: 0 0 5px #f0f;
}

.terminal-content::-webkit-scrollbar-thumb:hover {
  background: #0ff;
}

.terminal-header {
  text-align: center;
  margin-bottom: 30px;
}

.glitch-title {
  font-family: 'DungGeunMo', monospace;
  font-size: 2.5rem;
  color: #f0f;
  text-shadow:
    2px 2px #0ff,
    -2px -2px #f00;
  animation: glitch 1s infinite;
}

.cyber-form {
  display: grid;
  gap: 30px;
}

.form-section {
  background: rgba(255, 0, 255, 0.05);
  padding: 20px;
  border-radius: 10px;
  border: 1px solid rgba(255, 0, 255, 0.2);
}

.section-title {
  color: #f0f;
  font-size: 1.3rem;
  margin-bottom: 20px;
  text-shadow: 0 0 10px #f0f;
  font-family: 'DungGeunMo';
}

.input-group {
  margin-bottom: 20px;
}

.cyber-label {
  display: block;
  color: #f0f;
  margin-bottom: 8px;
  font-family: 'DungGeunMo';
}

.cyber-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid #f0f;
  padding: 10px;
  color: #fff;
  border-radius: 5px;
  font-family: 'DungGeunMo';
}

.cyber-input:focus {
  outline: none;
  border-color: #0ff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
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
}

.range-track {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #f0f, #0ff);
  transform: translateY(-50%);
  pointer-events: none;
}

.button-group {
  display: flex;
  gap: 20px;
  justify-content: flex-end;
}

.cyber-button {
  background: rgba(255, 0, 255, 0.1);
  border: 1px solid #f0f;
  color: #fff;
  padding: 10px 30px;
  font-family: 'DungGeunMo';
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.cyber-button:hover {
  background: rgba(255, 0, 255, 0.2);
  box-shadow: 0 0 15px #f0f;
}

.cyber-button.cancel {
  border-color: #ff0000;
}

.cyber-button.cancel:hover {
  box-shadow: 0 0 15px #ff0000;
}

.cyber-alert {
  margin-top: 20px;
  padding: 15px;
  border-radius: 5px;
  font-family: 'DungGeunMo';
  animation: fadeIn 0.3s ease;
}

.cyber-alert.success {
  background: rgba(0, 255, 0, 0.1);
  border: 1px solid #0f0;
  color: #0f0;
}

.cyber-alert.error {
  background: rgba(255, 0, 0, 0.1);
  border: 1px solid #f00;
  color: #f00;
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