<template>
  <div class="arcade-quiz-container">
    <!-- 퀴즈 섹션 -->
    <transition name="fade" mode="out-in">
      <div v-if="!showResult" class="quiz-section">
        <div class="quiz-header">
          <h4 class="quest-title">{{ quest?.job }} → {{ quest?.reward }}</h4>
          <div class="progress-info">
            <div class="progress-text">PROGRESS: {{ currentQuestionIndex + 1 }}/{{ filteredQuestions.length }}</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${(currentQuestionIndex / filteredQuestions.length) * 100}%` }"></div>
            </div>
          </div>
        </div>

        <div v-if="currentQuestion" class="question-box">
          <div class="question-number">Q{{ currentQuestionIndex + 1 }}</div>
          <h5 class="question-text">{{ currentQuestion.question }}</h5>
          
          <!-- 객관식 -->
          <div v-if="currentQuestion.choices" class="choices-grid">
            <button
              v-for="(choice, index) in parseChoices(currentQuestion.choices)"
              :key="index"
              class="choice-btn"
              :class="{ selected: userAnswer === (index + 1).toString() }"
              @click="selectAnswer((index + 1).toString())"
            >
              {{ choice }}
            </button>
          </div>
          
          <!-- 주관식 -->
          <div v-else class="subjective-answer">
            <input 
              type="text" 
              v-model="userAnswer"
              @keyup.enter="submitAnswer"
              class="answer-input"
              placeholder="답을 입력하세요"
            >
          </div>

          <button 
            @click="submitAnswer"
            class="submit-btn"
            :disabled="!userAnswer"
          >
            제출하기
          </button>
        </div>
      </div>

      <!-- 결과 컴포넌트 -->
      <div v-else class="result-section">
        <QuestSuccess v-if="isSuccess" @close="closeQuest" />
        <QuestFail v-else @close="closeQuest" />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/tier'
import axios from 'axios'
import QuestSuccess from './QuestSuccess.vue'
import QuestFail from './QuestFail.vue'

// Props
const props = defineProps({
  quest: {
    type: Object,
    required: true,
    default: () => null
  }
})

// Emits
const emit = defineEmits(['quiz-started', 'quiz-ended'])

// Store
const userStore = useUserStore()

// Refs
const allQuestions = ref([])
const currentQuestionIndex = ref(0)
const userAnswer = ref('')
const showResult = ref(false)
const isSuccess = ref(false)

// Computed
const filteredQuestions = computed(() => {
  if (!props.quest || !allQuestions.value.length) return []
  return allQuestions.value
    .filter(q => q.category?.name === props.quest.huntingGround)
    .slice(0, 5)
})

const currentQuestion = computed(() => {
  if (!filteredQuestions.value.length) return null
  return filteredQuestions.value[currentQuestionIndex.value]
})

// Methods
const resetQuizState = () => {
  currentQuestionIndex.value = 0
  userAnswer.value = ''
  showResult.value = false
  isSuccess.value = false
  emit('quiz-started')
}

const parseChoices = (choicesStr) => {
  if (!choicesStr) return []
  try {
    return eval(choicesStr)
  } catch {
    return []
  }
}

const selectAnswer = (answer) => {
  userAnswer.value = answer
}

const submitAnswer = async () => {
  if (!currentQuestion.value || !userAnswer.value) return

  if (currentQuestion.value.answer === userAnswer.value) {
    if (currentQuestionIndex.value < filteredQuestions.value.length - 1) {
      currentQuestionIndex.value++
      userAnswer.value = ''
    } else {
      const success = await userStore.updateTier(props.quest.reward)
      showResult.value = true
      isSuccess.value = success
      emit('quiz-ended')
    }
  } else {
    showResult.value = true
    isSuccess.value = false
    emit('quiz-ended')
  }
}

const closeQuest = () => {
  emit('quiz-ended')
  const modal = bootstrap.Modal.getInstance(document.getElementById('questModal'))
  if (modal) {
    modal.hide()
  }
}

// Watchers
watch(() => props.quest, (newQuest) => {
  if (newQuest) {
    resetQuizState()
  }
}, { immediate: true })

// Lifecycle Hooks
onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/quest/list/')
    allQuestions.value = response.data
  } catch (error) {
    console.error('퀘스트 목록 로딩 실패:', error)
    allQuestions.value = []
  }
})
</script>

<style scoped>
.arcade-quiz-container {
  background: #1a1a1a;
  min-height: 400px;
  position: relative;
}

/* 퀴즈 섹션 스타일 */
.quiz-section {
  padding: 2rem;
}

.quiz-header {
  margin-bottom: 2rem;
}

.quest-title {
  color: #f0f;
  font-size: 1.5rem;
  text-align: center;
  margin-bottom: 1rem;
  font-family: 'DungGeunMo';
  text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
}

.progress-info {
  background: rgba(255, 0, 255, 0.1);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #f0f;
}

.progress-text {
  color: #f0f;
  font-size: 0.9rem;
  margin-bottom: 8px;
  font-family: 'DungGeunMo';
}

.progress-bar {
  height: 8px;
  background: rgba(255, 0, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #f0f;
  transition: width 0.3s ease;
  box-shadow: 0 0 10px #f0f;
}

/* 문제 박스 스타일 */
.question-box {
  background: rgba(255, 0, 255, 0.05);
  border: 2px solid #f0f;
  border-radius: 15px;
  padding: 2rem;
  margin-top: 2rem;
  position: relative;
  overflow: hidden;
}

.question-number {
  position: absolute;
  top: 10px;
  right: 10px;
  color: #f0f;
  font-size: 0.9rem;
  font-family: 'DungGeunMo';
  opacity: 0.8;
}

.question-text {
  color: white;
  font-size: 1.2rem;
  margin-bottom: 2rem;
  font-family: 'DungGeunMo';
  line-height: 1.6;
}

/* 객관식 보기 스타일 */
.choices-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.choice-btn {
  background: rgba(255, 0, 255, 0.1);
  border: 2px solid #f0f;
  color: white;
  padding: 1rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'DungGeunMo';
  text-align: left;
}

.choice-btn:hover {
  background: rgba(255, 0, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
}

.choice-btn.selected {
  background: rgba(255, 0, 255, 0.3);
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.4);
}

/* 주관식 입력 스타일 */
.answer-input {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid #f0f;
  border-radius: 10px;
  color: white;
  font-family: 'DungGeunMo';
  margin-bottom: 1.5rem;
}

.answer-input:focus {
  outline: none;
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
}

/* 제출 버튼 스타일 */
.submit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(45deg, #f0f, #90f);
  border: none;
  border-radius: 10px;
  color: white;
  font-family: 'DungGeunMo';
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.4);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 결과 섹션 스타일 */
.result-section {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 트랜지션 효과 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .quiz-section {
    padding: 1rem;
  }

  .quest-title {
    font-size: 1.2rem;
  }

  .question-text {
    font-size: 1rem;
  }

  .choices-grid {
    grid-template-columns: 1fr;
  }

  .choice-btn {
    padding: 0.8rem;
  }
}
</style>