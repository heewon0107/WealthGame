<template>
  <div class="arcade-quest-container">
    <div class="quest-header">
      <div class="header-text">
        <div class="glitch-text" data-text="CHALLENGE QUESTS">CHALLENGE QUESTS</div>
        <div 
          :class="[
            'sub-text',
            { 'completion-text': userStore.tier === '건물주' }
          ]"
        >
          <template v-if="userStore.tier === '건물주'">
            <span class="completion-icon">👑</span>
            모든 퀘스트를 완료하였습니다!
            <span class="completion-icon">👑</span>
          </template>
          <template v-else>
            새로운 티어로 전직하세요!
          </template>
        </div>
      </div>
    </div>

    <!-- 퀘스트 테이블 -->
    <div class="quest-table-container">
      <div class="scanner-line"></div>
      <table class="quest-table">
        <thead>
          <tr>
            <th>CURRENT</th>
            <th>NEXT</th>
            <th>LOCATION</th>
            <th>ENTER</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="(quest, index) in quests" 
            :key="index"
            :class="{ 'current-tier': quest.job === userStore.tier }"
          >
            <td>
              <div class="class-name">{{ quest.job }}</div>
            </td>
            <td>
              <div class="reward-name">{{ quest.reward }}</div>
            </td>
            <td>
              <div class="hunting-ground">{{ quest.huntingGround }}</div>
            </td>
            <td>
              <button 
                class="enter-btn" 
                @click="openModal(quest)"
                :disabled="quest.job !== userStore.tier"
                :class="{
                  'available': quest.job === userStore.tier,
                  'locked': quest.job !== userStore.tier
                }"
              >
                <span class="btn-text" v-if="quest.job === userStore.tier">
                  START!
                  <i class="fas fa-play"></i>
                </span>
                <span class="btn-text" v-else>
                  <i class="fas fa-lock"></i>
                  LOCKED
                </span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 모달 -->
    <teleport to="body">
      <div 
        class="modal fade" 
        id="questModal" 
        tabindex="-1" 
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        aria-labelledby="questModalLabel" 
        aria-hidden="true"
      >
        <div class="modal-dialog modal-lg modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="questModalLabel">
                {{ selectedQuest?.job }} → {{ selectedQuest?.reward }}
              </h5>
              <button 
                type="button" 
                class="btn-close" 
                data-bs-dismiss="modal" 
                aria-label="Close"
                :disabled="isQuizInProgress"
              ></button>
            </div>
            <div class="modal-body">
              <QuestListDetail 
                v-if="selectedQuest"
                :quest="selectedQuest"
                @quiz-started="handleQuizStart"
                @quiz-ended="handleQuizEnd"
              />
            </div>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useUserStore } from "@/stores/tier"
import QuestListDetail from "./QuestListDetail.vue"

// Store
const userStore = useUserStore()

// Refs
const isQuizInProgress = ref(false)
const selectedQuest = ref(null)

// Data
const quests = ref([
  { job: "알거지", reward: "이자사냥꾼", huntingGround: "예적금" },
  { job: "이자사냥꾼", reward: "화폐술사", huntingGround: "달러" },
  { job: "화폐술사", reward: "집마스터", huntingGround: "청약" },
  { job: "집마스터", reward: "차트마스터", huntingGround: "주식" },
  { job: "차트마스터", reward: "건물주", huntingGround: "부동산" },
])

// Methods
const openModal = (quest) => {
  if (quest.job === userStore.tier) {
    selectedQuest.value = { ...quest }
    const modal = new bootstrap.Modal(document.getElementById("questModal"))
    modal.show()
  }
}

const handleQuizStart = () => {
  isQuizInProgress.value = true
}

const handleQuizEnd = () => {
  isQuizInProgress.value = false
}

// Lifecycle Hooks
onMounted(async () => {
  await userStore.fetchUserTier()
})

onBeforeUnmount(() => {
  selectedQuest.value = null
})
</script>

<style scoped>
.arcade-quest-container {
  width: 100%;
  height: 100%;
  padding: 20px;
  color: #fff;
}

.quest-header {
  text-align: center;
  margin-bottom: 30px;
  position: relative;
}

.header-text {
  position: relative;
  z-index: 2;
}

.glitch-text {
  font-size: 2.5rem;
  font-weight: bold;
  color: #f0f;
  text-shadow: 2px 2px #0ff;
  position: relative;
  font-family: 'DungGeunMo';
  margin-bottom: 15px;
}

.sub-text {
  font-size: 1.2rem;
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
  opacity: 0.8;
  font-family: 'DungGeunMo';
}

.completion-text {
  color: #FFD700 !important;
  font-size: 1.4rem !important;
  text-shadow: 0 0 15px rgba(255, 215, 0, 0.7) !important;
  animation: glowingGold 2s infinite;
  font-weight: bold;
  letter-spacing: 1px;
}

.completion-icon {
  display: inline-block;
  margin: 0 10px;
  animation: bounceIcon 1s infinite alternate;
}

/* 테이블 스타일 */
.quest-table-container {
  position: relative;
  background: rgba(255, 0, 255, 0.1);
  border: 2px solid #f0f;
  border-radius: 15px;
  padding: 20px;
  overflow: hidden;
}

.scanner-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: rgba(255, 0, 255, 0.5);
  box-shadow: 0 0 10px #f0f;
  animation: scan 3s linear infinite;
}

.quest-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 10px;
}

.quest-table th {
  padding: 15px;
  text-align: center;
  color: #f0f;
  font-family: 'DungGeunMo';
  font-size: 1rem;
  letter-spacing: 1px;
  border-bottom: 2px solid rgba(255, 0, 255, 0.3);
}

.quest-table td {
  padding: 20px 15px;
  text-align: center;
  background: rgba(255, 0, 255, 0.05);
  transition: all 0.3s ease;
  font-family: 'DungGeunMo';
}

.quest-table tr {
  transition: all 0.3s ease;
}

.quest-table tr:hover td {
  background: rgba(255, 0, 255, 0.1);
  transform: scale(1.02);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
}

.current-tier td {
  background: rgba(255, 0, 255, 0.15) !important;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
}

.class-name,
.reward-name,
.hunting-ground {
  font-size: 1.1rem;
  font-weight: bold;
  text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

/* 버튼 스타일 */
.enter-btn {
  padding: 12px 25px;
  border: 2px solid #f0f;
  background: transparent;
  color: #fff;
  border-radius: 25px;
  cursor: pointer;
  font-family: 'DungGeunMo';
  font-size: 1rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.enter-btn.available {
  background: linear-gradient(45deg, #f0f, #90f);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
}

.enter-btn.available:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 25px rgba(255, 0, 255, 0.7);
}

.enter-btn.available::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(45deg);
  animation: shine 3s infinite;
}

.enter-btn.locked {
  background: rgba(108, 117, 125, 0.3);
  border-color: #6c757d;
  cursor: not-allowed;
  opacity: 0.7;
}

.btn-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

/* 모달 스타일 */
.modal-content {
  background: #1a1a1a;
  border: 2px solid #f0f;
  box-shadow: 0 0 30px rgba(255, 0, 255, 0.3);
}

.modal-header {
  background: linear-gradient(45deg, #f0f, #90f);
  border-bottom: none;
  padding: 1.5rem;
}

.modal-title {
  color: #fff;
  font-family: 'DungGeunMo';
  font-size: 1.3rem;
  margin: 0;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.btn-close {
  color: #fff;
  text-shadow: none;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.btn-close:not(:disabled):hover {
  opacity: 1;
  transform: rotate(90deg);
}

.btn-close:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.modal-body {
  padding: 0;
  background: #1a1a1a;
}

/* 애니메이션 */
@keyframes scan {
  0% { top: 0; }
  100% { top: 100%; }
}

@keyframes shine {
  0% { transform: translateX(-100%) rotate(45deg); }
  100% { transform: translateX(100%) rotate(45deg); }
}

@keyframes glowingGold {
  0% {
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
  }
  50% {
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.9),
                 0 0 30px rgba(255, 215, 0, 0.7),
                 0 0 40px rgba(255, 215, 0, 0.5);
  }
  100% {
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
  }
}

@keyframes bounceIcon {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-5px);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .glitch-text {
    font-size: 1.8rem;
  }

  .sub-text {
    font-size: 1rem;
  }

  .completion-text {
    font-size: 1.2rem !important;
  }
  
  .completion-icon {
    margin: 0 5px;
  }

  .quest-table th,
  .quest-table td {
    padding: 10px 8px;
    font-size: 0.9rem;
  }

  .enter-btn {
    padding: 8px 16px;
    font-size: 0.8rem;
  }
}
</style>