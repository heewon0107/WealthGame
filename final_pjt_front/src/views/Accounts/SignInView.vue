<template>
  <div class="arcade-login-container">
    <!-- 배경 효과 -->
    <div class="stars"></div>
    <div class="twinkling"></div>
    
    <div class="arcade-cabinet">
      <div class="screen-frame">
        <div class="screen-overlay"></div>
        <div class="screen-content">
          <div class="glitch-title" data-text="LOGIN">LOGIN</div>
          
          <form @submit.prevent="handleSignIn" class="login-form">
            <div class="input-group">
              <label for="email" class="cyber-label">EMAIL:</label>
              <input
                type="email"
                id="email"
                v-model="email"
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
                v-model="password"
                class="cyber-input"
                placeholder="ENTER YOUR PASSWORD"
                required
              />
              <div class="input-line"></div>
            </div>
            
            <button type="submit" class="neon-button">
              <span class="button-line"></span>
              <span class="button-line"></span>
              <span class="button-text">PRESS START</span>
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
import { ref } from "vue";
import axios from "axios";
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useInventoryStore } from '@/stores/inventory';

const email = ref("");
const password = ref("");
const token = ref("");
const router = useRouter();
const authStore = useAuthStore();
const inventoryStore = useInventoryStore();

const handleSignIn = () => {
  axios({
    url: "http://127.0.0.1:8000/accounts/login/",
    method: "post",
    data: {
      email: email.value,
      password: password.value,
    },
  })
    .then(async (response) => {
      console.log(response.data);
      token.value = response.data.token;
      localStorage.setItem("token", token.value);
      localStorage.setItem('is_superuser', response.data.is_superuser);  // user 정보를 저장
      localStorage.setItem('user_id', response.data.user_id)
      localStorage.setItem('userTier', response.data.userTier)
      // 로그인 성공 시 인벤토리 초기화
      await inventoryStore.initializeInventory(response.data.user_id);
      
      // 인증 상태 업데이트
      authStore.setLoginStatus(true);
      
      router.push({name : 'StartView'});
    })
    .catch((error) => {
      console.error("로그인 오류:", error.response?.data || error);
      alert("로그인에 실패했습니다. 이메일과 비밀번호를 확인하세요.");
    });
};
</script>

<style scoped>
.arcade-login-container {
  position: relative;
  width: 100vw;
  min-height: 90vh;
  overflow: hidden;
  background: #000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-right: 1000px;
}

.stars, .twinkling {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
}

.stars {
  background: #000 url("/stars.png") repeat top center;
  z-index: 0;
}

.twinkling {
  background: transparent url("/twinkling.png") repeat top center;
  z-index: 1;
  animation: move-twinkle 200s linear infinite;
}

.arcade-cabinet {
  position: relative;
  z-index: 2;
  width: 80%;
  max-width: 600px;
  background: #1a1a1a;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 0 50px rgba(255, 0, 255, 0.3);
  border: 3px solid #f0f;
}

.screen-frame {
  position: relative;
  background: #000;
  border-radius: 10px;
  padding: 20px;
  overflow: hidden;
}

.screen-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    transparent 50%,
    rgba(255, 255, 255, 0.05) 50%
  );
  background-size: 100% 4px;
  pointer-events: none;
}

.screen-content {
  position: relative;
  z-index: 2;
  padding: 30px;
}

.glitch-title {
  font-size: 3em;
  text-align: center;
  color: #f0f;
  text-shadow: 2px 2px #0ff;
  margin-bottom: 40px;
  font-family: 'DungGeunMo';
  position: relative;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.input-group {
  position: relative;
}

.cyber-label {
  color: #f0f;
  font-family: 'DungGeunMo';
  margin-bottom: 10px;
  display: block;
  text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

.cyber-input {
  width: 100%;
  padding: 10px;
  background: transparent;
  border: none;
  border-bottom: 2px solid #f0f;
  color: #fff;
  font-family: 'DungGeunMo';
  font-size: 1.1em;
  outline: none;
}

.cyber-input:focus {
  border-color: #0ff;
}

.input-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: #0ff;
  transition: width 0.3s ease;
}

.cyber-input:focus + .input-line {
  width: 100%;
}

.neon-button {
  position: relative;
  padding: 15px 30px;
  background: transparent;
  border: none;
  color: #fff;
  font-family: 'DungGeunMo';
  font-size: 1.2em;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  margin-top: 20px;
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
  animation: line1 2s infinite;
}

.button-line:nth-child(2) {
  top: 0;
  right: 0;
  width: 2px;
  height: 100%;
  transform: translateY(-100%);
  animation: line2 2s infinite;
}

.button-line:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  transform: translateX(100%);
  animation: line3 2s infinite;
}

.button-line:nth-child(4) {
  bottom: 0;
  left: 0;
  width: 2px;
  height: 100%;
  transform: translateY(100%);
  animation: line4 2s infinite;
}

.button-text {
  position: relative;
  z-index: 1;
}

.neon-button:hover {
  background: rgba(255, 0, 255, 0.1);
  box-shadow: 0 0 30px rgba(255, 0, 255, 0.3);
}

@keyframes line1 {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes line2 {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

@keyframes line3 {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}

@keyframes line4 {
  0% { transform: translateY(100%); }
  100% { transform: translateY(-100%); }
}

@keyframes move-twinkle {
  from { background-position: 0 0; }
  to { background-position: -10000px 5000px; }
}

@media (max-width: 768px) {
  .arcade-cabinet {
    width: 95%;
    padding: 10px;
  }

  .glitch-title {
    font-size: 2em;
  }

  .cyber-input {
    font-size: 1em;
  }

  .neon-button {
    padding: 12px 24px;
    font-size: 1em;
  }
}
</style>