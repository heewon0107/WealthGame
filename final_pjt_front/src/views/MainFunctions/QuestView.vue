<template>
  <div class="game-screen">
    <!-- 배경 효과 -->
    <div class="stars"></div>
    <div class="twinkling"></div>
    
    <!-- 헤더 영역 -->
    <div class="quest-header">
      <div class="neon-title">QUEST ZONE</div>
      <!-- 랭킹 모달을 여는 버튼 -->
      <button @click="openRankingModal" class="open-ranking-btn">랭킹 보기</button>
      <div class="player-status">
        <div class="status-label">CURRENT Tier</div>
        <div class="current-tier">{{ userStore.tier || '알거지' }}</div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="game-content">
      <div class="arcade-frame">
        <div class="screen-overlay"></div>
        <div class="content-area">
          <QuestList />
        </div>
      </div>
    </div>

    <!-- 상태 표시 영역 -->
    <div class="status-bar">
      <div class="power-meter">
        <div class="meter-label">POWER</div>
        <div class="meter-bar">
          <div class="meter-fill"></div>
        </div>
      </div>
      <div class="exp-meter">
        <div class="meter-label">EXP</div>
        <div class="meter-bar">
          <div 
            class="meter-fill" 
            :style="{ width: `${calculateExpPercentage()}%` }"
          ></div>
        </div>
        <div class="exp-labels">
          <span class="exp-start">알거지</span>
          <span class="exp-end">건물주</span>
        </div>
      </div>
    </div>

    <!-- Teleport를 사용한 모달 -->
    <Teleport to="body">
      <div v-if="isModalOpen" class="modal-overlay" @click="closeRankingModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>최고의 플레이어들</h2>
            <button @click="closeRankingModal" class="close-modal-btn">X</button>
          </div>
          <div class="ranking-list">
            <div 
              v-for="(user, index) in userRankList" 
              :key="user.username" 
              class="rank-item"
            >
              <div class="rank-position">
                <span :class="{'gold': index === 0, 'silver': index === 1, 'bronze': index === 2}">
                  {{ index === 0 ? '1st' : index === 1 ? '2nd' : '3rd' }}
                </span>
              </div>
              <div class="rank-info">
                <span class="username">{{ user.username }}</span>
                <span class="tier">{{ user.tier }}</span>
                <span class="assets">{{ user.assets.toLocaleString() }} 자산</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from "@/stores/tier";
import QuestList from '@/components/Quests/QuestList.vue';
import { Teleport } from 'vue';

onMounted(() => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/accounts/ranking/'
  })
  .then((res) => {
    userRankList.value = res.data.ranking
  })
})
const userRankList = ref(null)

const userStore = useUserStore();
const isModalOpen = ref(false);  // 모달 열기/닫기 상태 관리

const openRankingModal = () => {
  isModalOpen.value = true;
};

// 모달 닫기 함수
const closeRankingModal = () => {
  isModalOpen.value = false;
};
// 클래스 순서 정의
const classOrder = ['알거지', '이자사냥꾼', '화폐술사', '집마스터', '차트마스터', '건물주'];

// EXP 퍼센트 계산
const calculateExpPercentage = () => {
  const currentIndex = classOrder.indexOf(userStore.tier);
  if (currentIndex === -1) return 0;
  return (currentIndex / (classOrder.length - 1)) * 100;
};
</script>

<style scoped>
.game-screen {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: white;
  padding: 20px;
  background: #000;
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

@keyframes move-twinkle {
  from { background-position: 0 0; }
  to { background-position: -10000px 5000px; }
}

/* 헤더 스타일 */
.quest-header {
  position: relative;
  z-index: 2;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  margin-bottom: 20px;
}

.neon-title {
  font-size: 3rem;
  font-weight: bold;
  color: #f0f;
  text-shadow: 
    0 0 2px #f0f,
    0 0 4px #f0f,
    0 0 8px #f0f;
  animation: neon-pulse 1.5s ease-in-out infinite alternate;
  font-family: 'DungGeunMo';
}

.player-status {
  background: rgba(255, 0, 255, 0.1);
  padding: 15px;
  border: 2px solid #f0f;
  border-radius: 10px;
  text-align: center;
}

.status-label {
  font-size: 0.8rem;
  color: #f0f;
  margin-bottom: 5px;
  font-family: 'DungGeunMo';
}

.current-tier {
  font-size: 1.2rem;
  color: #fff;
  text-shadow: 0 0 10px #f0f;
  font-family: 'DungGeunMo';
}

/* 메인 컨텐츠 영역 */
.game-content {
  position: relative;
  z-index: 2;
  width: 90%;
  height: calc(100% - 180px);
  padding: 20px;
}

.arcade-frame {
  width: 100%;
  height: 100%;
  background: rgba(255, 0, 255, 0.1);
  border: 4px solid #f0f;
  border-radius: 20px;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 0 20px #f0f,
    inset 0 0 40px rgba(255, 0, 255, 0.3);
}

.screen-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    transparent,
    rgba(255, 0, 255, 0.1) 50%,
    transparent
  );
  animation: scan-line 8s linear infinite;
  pointer-events: none;
}

.content-area {
  width: 100%;
  height: 100%;
  padding: 20px;
  overflow-y: auto;
}

/* 상태 표시 바 */
.status-bar {
  position: relative;
  z-index: 2;
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.power-meter,
.exp-meter {
  width: 200px;
}

.meter-label {
  color: #f0f;
  font-size: 0.8rem;
  margin-bottom: 5px;
  font-family: 'DungGeunMo';
}

.meter-bar {
  height: 10px;
  background: rgba(255, 0, 255, 0.2);
  border: 1px solid #f0f;
  border-radius: 5px;
  overflow: hidden;
}

.meter-fill {
  height: 100%;
  background: #f0f;
  transition: width 1s ease-in-out;
  box-shadow: 0 0 10px #f0f;
  animation: meter-glow 2s ease-in-out infinite;
}

.exp-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  font-size: 0.7rem;
  color: rgba(255, 0, 255, 0.8);
  font-family: 'DungGeunMo';
}

/* 랭킹 보기 버튼 */
.open-ranking-btn {
  background: rgba(255, 0, 255, 0.1);
  color: #fff;
  font-size: 1rem;
  padding: 10px 20px;
  border: 2px solid #f0f;
  border-radius: 10px;
  cursor: pointer;
  font-family: 'DungGeunMo';
  transition: all 0.3s ease;
  text-shadow: 0 0 5px #f0f;
}

.open-ranking-btn:hover {
  background: rgba(255, 0, 255, 0.2);
  box-shadow: 0 0 20px #f0f;
  transform: translateY(-2px);
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: rgba(20, 20, 20, 0.9);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 0, 255, 0.5);
  border-radius: 20px;
  padding: 30px;
  width: 90%;
  max-width: 600px;
  box-shadow: 
    0 0 30px rgba(255, 0, 255, 0.3),
    inset 0 0 30px rgba(255, 0, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.modal-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 200%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 0, 255, 0.2),
    transparent
  );
  animation: shine 3s infinite;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(255, 0, 255, 0.3);
  margin-bottom: 20px;
  position: relative;
}

.modal-header h2 {
  color: #fff;
  font-size: 2rem;
  text-shadow: 
    0 0 5px #f0f,
    0 0 10px #f0f;
  font-family: 'DungGeunMo';
  margin: 0;
}

.close-modal-btn {
  background: rgba(255, 0, 255, 0.1);
  color: #fff;
  font-size: 1.2rem;
  border: 1px solid rgba(255, 0, 255, 0.5);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-modal-btn:hover {
  background: rgba(255, 0, 255, 0.3);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
  transform: rotate(90deg);
}

.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 10px;
}

.rank-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 0, 255, 0.2);
  border-radius: 15px;
  padding: 15px;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.rank-item:hover {
  transform: translateX(10px);
  background: rgba(255, 255, 255, 0.1);
  box-shadow: -5px 0 15px rgba(255, 0, 255, 0.3);
}

.rank-position {
  width: 80px;
  text-align: center;
}

.rank-position .gold {
  color: #ffd700;
  font-size: 2rem;
  font-weight: bold;
  text-shadow: 
    0 0 10px rgba(255, 215, 0, 0.7),
    0 0 20px rgba(255, 215, 0, 0.5);
  animation: pulse-gold 2s infinite;
}

.rank-position .silver {
  color: #c0c0c0;
  font-size: 1.8rem;
  font-weight: bold;
  text-shadow: 
    0 0 10px rgba(192, 192, 192, 0.7),
    0 0 20px rgba(192, 192, 192, 0.5);
  animation: pulse-silver 2s infinite;
}

.rank-position .bronze {
  color: #cd7f32;
  font-size: 1.6rem;
  font-weight: bold;
  text-shadow: 
    0 0 10px rgba(205, 127, 50, 0.7),
    0 0 20px rgba(205, 127, 50, 0.5);
  animation: pulse-bronze 2s infinite;
}

.rank-info {
  flex-grow: 1;
  display: grid;
  grid-template-columns: 2fr 1fr 2fr;
  gap: 20px;
  align-items: center;
}

.username {
  color: #fff;
  font-weight: bold;
  font-size: 1.1rem;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

.tier {
  color: #f0f;
  font-style: italic;
  text-shadow: 0 0 5px rgba(255, 0, 255, 0.5);
}

.assets {
  color: #ffd700;
  font-weight: bold;
  text-align: right;
  text-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
}

/* 스크롤바 스타일 */
.ranking-list::-webkit-scrollbar {
  width: 8px;
}

.ranking-list::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 4px;
}

.ranking-list::-webkit-scrollbar-thumb {
  background: rgba(255, 0, 255, 0.3);
  border-radius: 4px;
  border: 2px solid rgba(255, 0, 255, 0.5);
}

.ranking-list::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 0, 255, 0.5);
}

/* 애니메이션 */
@keyframes neon-pulse {
  from { 
    text-shadow: 
      0 0 2px #f0f,
      0 0 4px #f0f,
      0 0 8px #f0f;
  }
  to { 
    text-shadow: 
      0 0 3px #f0f,
      0 0 6px #f0f,
      0 0 12px #f0f;
  }
}

@keyframes pulse-gold {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes pulse-silver {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.03); }
}

@keyframes pulse-bronze {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

@keyframes shine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes scan-line {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

@keyframes meter-glow {
  0% { filter: brightness(1); }
  50% { filter: brightness(1.3); }
  100% { filter: brightness(1); }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .quest-header {
    flex-direction: column;
    gap: 20px;
  }

  .neon-title {
    font-size: 2rem;
  }

  .status-bar {
    flex-direction: column;
    align-items: center;
  }

  .modal-content {
    width: 95%;
    padding: 20px;
  }

  .modal-header h2 {
    font-size: 1.5rem;
  }

  .rank-info {
    grid-template-columns: 1fr;
    gap: 10px;
    text-align: center;
  }

  .assets {
    text-align: center;
  }

  .rank-position .gold {
    font-size: 1.8rem;
  }

  .rank-position .silver {
    font-size: 1.6rem;
  }

  .rank-position .bronze {
    font-size: 1.4rem;
  }
}
</style>