<template>
  <div class="all">
    <!-- 로고 영역 -->
    <RouterLink :to="{name: 'StartView'}" class="logo-container">
      <img src="/wg_controller_color.png" alt="WG Controller" class="logo-image">
      <div class="logo-glow"></div>
    </RouterLink>

    <!-- 네비게이션 버튼 -->
    <div class="nav-buttons">
      <template v-if="authStore.isLoggedIn">
        <div v-if="userTier">
          <RouterLink v-if="userTier == '건물주'" :to="{name: 'QuestCredit'}" class="nav-button credit-button">
            <div class="button-content">
              <i class="fas fa-user-circle"></i>
              <span class="button-text">CREDIT</span>
            </div>
            <div class="button-glow gold-glow"></div>
          </RouterLink>
        </div>
        <RouterLink :to="{name : 'ProfileView'}" class="nav-button">
          <div class="button-content">
            <i class="fas fa-user-circle"></i>
            <span class="button-text">PROFILE</span>
          </div>
          <div class="button-glow"></div>
        </RouterLink>
        <button class="nav-button" @click="handleLogout">
          <div class="button-content">
            <i class="fas fa-sign-out-alt"></i>
            <span class="button-text">LOGOUT</span>
          </div>
          <div class="button-glow"></div>
        </button>
      </template>
      <template v-else>
        <RouterLink :to="{name:'SignUpView'}" class="nav-button">
          <div class="button-content">
            <i class="fas fa-user-plus"></i>
            <span class="button-text">SIGN UP</span>
          </div>
          <div class="button-glow"></div>
        </RouterLink>
        <RouterLink :to="{name:'SignInView'}" class="nav-button">
          <div class="button-content">
            <i class="fas fa-sign-in-alt"></i>
            <span class="button-text">LOGIN</span>
          </div>
          <div class="button-glow"></div>
        </RouterLink>
      </template>
    </div>
    <Home/>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Home from './components/Home.vue'
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useInventoryStore } from './stores/inventory'

const authStore = useAuthStore()
const router = useRouter()
const inventoryStore = useInventoryStore()

const userTier = ref(localStorage.getItem('userTier'))

const handleLogout = () => {
  const token = localStorage.getItem('token')
  axios({
    method: 'post',
    url: "http://127.0.0.1:8000/accounts/logout/",
    headers: {
      Authorization: `Token ${token}`,
    },
  })
  .then(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('userTier')
    localStorage.removeItem('is_superuser')
    
    // 인벤토리 스토어 초기화
    inventoryStore.clearInventory()
    // 인증 스토어 상태 변경
    authStore.setLoginStatus(false)
    router.push({name: 'StartView'})
    })
    .catch((error) => {
      console.error('로그아웃 실패:', error.response?.data || error)
      alert('로그아웃에 실패했습니다.')
    })
}

// 컴포넌트 마운트 시 로그인 상태 체크
onMounted(() => {
  authStore.checkLoginStatus()
})
</script>

<style>
body {
  margin: 0;
  padding: 0;
  overflow: hidden;
  background: #000;
}

@font-face {
  font-family: 'DungGeunMo';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_six@1.2/DungGeunMo.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}

* {
  font-family: 'DungGeunMo';
}

/* 로고 스타일 */
.logo-container {
  position: fixed;
  top: 20px;
  left: 80px;
  z-index: 1000;
  display: flex;
  align-items: center;
  text-decoration: none;
  transition: all 0.3s ease;
}

.logo-image {
  width: 200px;
  height: 200px;
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 0 5px rgba(255, 0, 255, 0.5));
  transition: all 0.3s ease;
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 110px;
  height: 110px;
  background: radial-gradient(circle, rgba(255, 0, 255, 0.2) 0%, transparent 70%);
  animation: logo-pulse 2s ease-in-out infinite;
}

.logo-container:hover .logo-image {
  transform: scale(1.1);
  filter: drop-shadow(0 0 10px rgba(255, 0, 255, 0.8));
}

/* 네비게이션 버튼 스타일 */
.nav-buttons {
  position: fixed;
  top: 30px;
  right: 40px;
  display: flex;
  gap: 20px;
  z-index: 1000;
}

.nav-button {
  position: relative;
  display: flex;
  align-items: center;
  padding: 15px 30px;
  background: rgba(255, 0, 255, 0.1);
  border: 3px solid #f0f;
  border-radius: 50px;
  color: #fff;
  text-decoration: none;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.button-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 8px;
}

.button-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 0, 255, 0.3),
    transparent
  );
  animation: button-shine 3s linear infinite;
}

.nav-button:hover {
  background: rgba(255, 0, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 
    0 0 10px rgba(255, 0, 255, 0.5),
    0 0 20px rgba(255, 0, 255, 0.3),
    0 0 30px rgba(255, 0, 255, 0.1);
}

.nav-button i {
  font-size: 1.5rem;
  color: #f0f;
  text-shadow: 0 0 5px rgba(255, 0, 255, 0.5);
}

.button-text {
  font-size: 1.2rem;
  color: #fff;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

/* 애니메이션 */
@keyframes button-shine {
  0% {
    left: -100%;
  }
  50% {
    left: 100%;
  }
  100% {
    left: 100%;
  }
}

@keyframes logo-pulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.5;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0.8;
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.5;
  }
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .logo-container {
    top: 15px;
    left: 20px;
  }

  .logo-image {
    width: 60px;
    height: 60px;
  }

  .logo-glow {
    width: 70px;
    height: 70px;
  }

  .nav-buttons {
    top: 15px;
    right: 15px;
  }

  .nav-button {
    padding: 12px 20px;
  }

  .button-text {
    display: none;
  }

  .nav-button i {
    font-size: 2rem;
  }
}

/* credit */
.credit-button {
  background: rgba(255, 215, 0, 0.1) !important;
  border: 3px solid #FFD700 !important;
}

.credit-button:hover {
  background: rgba(255, 215, 0, 0.2) !important;
  box-shadow: 
    0 0 10px rgba(255, 215, 0, 0.5),
    0 0 20px rgba(255, 215, 0, 0.3),
    0 0 30px rgba(255, 215, 0, 0.1) !important;
}

.credit-button i {
  color: #FFD700 !important;
  text-shadow: 0 0 5px rgba(255, 215, 0, 0.5) !important;
}

.gold-glow {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 215, 0, 0.3),
    transparent
  ) !important;
}
</style>