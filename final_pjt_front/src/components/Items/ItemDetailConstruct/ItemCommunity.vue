<template>
  <div class="arcade-comments">
    <div class="cyber-header">
      <div class="glitch-text" data-text="ITEM REVIEWS">ITEM REVIEWS</div>
    </div>

    <!-- 댓글 작성 폼 -->
    <div class="comment-form-container">
      <form @submit.prevent="submitComment" @keyup.enter="submitComment" class="cyber-form">
        <textarea
          v-model="commentContent"
          class="cyber-input"
          required
          placeholder="Write your review here..."
        ></textarea>
        <div v-if="!isLoggedIn" class="login-message">
          <span class="neon-text">Please login to leave a review</span>
        </div>
        <div v-if="isLoggedIn" class="submit-container">
          <button type="submit" class="cyber-button">
            <span class="button-text">SUBMIT</span>
            <div class="button-glow"></div>
          </button>
        </div>
      </form>
    </div>

    <!-- 댓글 목록 -->
    <div class="comments-container">
      <ul class="cyber-comments-list">
        <li v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <div class="user-info">
              <span class="user-tier" :class="getTierClass(comment.tier)">
                {{ comment.tier || '알거지' }}
              </span>
              <span class="username">{{ comment.nickname }}</span>
            </div>
            <div class="comment-actions" v-if="comment.user_id == user_id">
              <template v-if="comment.isEditing">
                <button @click="updateComment(comment.id)" class="action-btn save-btn">
                  <Save size="16"/>
                </button>
              </template>
              <template v-else>
                <button @click="editComment(comment.id)" class="action-btn edit-btn">
                  <Edit size="16"/>
                </button>
                <button @click="deleteComment(comment.id)" class="action-btn delete-btn">
                  <Trash size="16"/>
                </button>
              </template>
            </div>
          </div>
          
          <div class="comment-content">
            <template v-if="comment.isEditing">
              <input 
                v-model="comment.content" 
                type="text"  
                @keyup.enter="updateComment(comment.id)" 
                class="cyber-edit-input"
              />
            </template>
            <template v-else>
              {{ comment.content }}
            </template>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { Edit, Save, Trash } from 'lucide-vue-next'

const route = useRoute()
const commentContent = ref('')
const comments = ref([])
const isLoggedIn = ref(false)
const user_id = ref('')

// Tier 시스템
const tierColors = {
 '알거지': '#ff4655',        // 빨강
 '이자사냥꾼': '#cd7f32',    // 브론즈
 '화폐술사': '#c0c0c0',      // 실버
 '집마스터': '#ffd700',      // 골드
 '차트마스터': '#e5e4e2',    // 플래티넘
 '건물주': '#b9f2ff'         // 다이아몬드
}

const getTierClass = (tier) => {
 return `tier-${tier?.toLowerCase() || '알거지'}`
}

// 로그인 상태 체크
const checkLoginStatus = () => {
 const token = localStorage.getItem('token')
 isLoggedIn.value = !!token
 if (token) {
   axios.defaults.headers.common['Authorization'] = `Token ${token}`
 }
}

// 댓글 로드
const loadComments = async () => {
 try {
   const response = await axios.get(`http://127.0.0.1:8000/comments/api/products/${route.params.productId}/comments/`)
   console.log('Loaded comments:', response.data)
   comments.value = Array.isArray(response.data) ? response.data : response.data.comments
 } catch (error) {
   console.error('Failed to load comments:', error)
 }
}

// 댓글 작성
const submitComment = async () => {
  if (!commentContent.value || !isLoggedIn.value) return
  
  // localStorage에서 현재 유저의 티어 가져오기
  const currentTier = localStorage.getItem('userTier') || '알거지'

  
  try {
    const response = await axios.post('http://127.0.0.1:8000/comments/api/products/comments/', {
      product_id: route.params.productId,
      content: commentContent.value,
      tier: currentTier  // 현재 티어 정보 추가
    })
    console.log(currentTier);
    
    
    const newComment = {
      ...response.data.comment,
      tier: currentTier  // 응답에 현재 티어 추가
    }
    console.log(newComment);
    console.log(response.data.comment);
    
    comments.value.push(newComment)
    console.log(comments);
    
    
    commentContent.value = ''
    
    await loadComments()
  } catch (error) {
    console.error('Failed to submit comment:', error)
    alert('댓글 작성에 실패했습니다.')
  }
}

// 댓글 삭제
const deleteComment = async (commentId) => {
 try {
   await axios.delete(`http://127.0.0.1:8000/comments/api/comments/delete/`, {
     params: { 
       product_id: route.params.productId, 
       comment_id: commentId 
     }
   })
   comments.value = comments.value.filter(comment => comment.id !== commentId)
 } catch (error) {
   console.error('Error deleting comment:', error)
   alert(error.response.data.error)
 }
}

// 댓글 수정
const updateComment = async (commentId) => {
 const comment = comments.value.find(c => c.id === commentId)
 if (!comment) return

 try {
   await axios.put(`http://127.0.0.1:8000/comments/api/comments/update/`, {
     params: {
       product_id: route.params.productId,
       comment_id: commentId,
       content: comment.content
     }
   })
   comment.isEditing = false
 } catch (error) {
   console.error('Error updating comment:', error)
   alert(error.response.data.error)
 }
}

// 수정 모드 활성화
const editComment = (commentId) => {
 const comment = comments.value.find(c => c.id === commentId)
 if (comment) {
   comment.isEditing = true
 }
}

// 컴포넌트 마운트 시 초기화
onMounted(() => {
 loadComments()
 checkLoginStatus()
 
 const userId = localStorage.getItem('user_id')
 if (userId) {
   user_id.value = userId
 } else {
   user_id.value = 'Guest'
 }
})
</script>

<style scoped>
.arcade-comments {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  color: #fff;
  font-family: 'DungGeunMo', sans-serif;
  height: calc(150vh - 4rem);
  overflow-y: auto;
  margin-bottom: 100rem;
}
/* 전체 스크롤바 스타일 */
.arcade-comments::-webkit-scrollbar {
  width: 8px;
}

.arcade-comments::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 10px;
}

.arcade-comments::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 10px;
  box-shadow: 0 0 10px #f0f;
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

.comment-form-container {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #f0f;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.2);
}

.cyber-input {
  width: 100%;
  min-height: 100px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid #f0f;
  border-radius: 8px;
  color: #fff;
  padding: 1rem;
  font-family: 'DungGeunMo';
  resize: vertical;
}

.cyber-button {
  background: transparent;
  border: 2px solid #f0f;
  color: #fff;
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-family: 'DungGeunMo';
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.cyber-button:hover {
  background: rgba(255, 0, 255, 0.2);
  box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
}

.comments-container {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #f0f;
  border-radius: 16px;
  padding: 1.5rem;
  /* 최대 높이 제한 해제 */
  max-height: none;
  /* 스크롤 제거 (전체 컨테이너가 스크롤됨) */
  overflow-y: visible;
}

.comment-item {
  background: rgba(255, 0, 255, 0.1);
  border: 1px solid rgba(255, 0, 255, 0.3);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Tier 스타일 */
.user-tier {
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.tier-알거지 { 
  background: rgba(255, 70, 85, 0.2);
  color: #ff4655;
  border: 1px solid #ff4655;
}

.tier-이자사냥꾼 {
  background: rgba(205, 127, 50, 0.2);
  color: #cd7f32;
  border: 1px solid #cd7f32;
}

.tier-화폐술사 {
  background: rgba(192, 192, 192, 0.2);
  color: #c0c0c0;
  border: 1px solid #c0c0c0;
}

.tier-집마스터 {
  background: rgba(255, 215, 0, 0.2);
  color: #ffd700;
  border: 1px solid #ffd700;
}

.tier-차트마스터 {
  background: rgba(229, 228, 226, 0.2);
  color: #e5e4e2;
  border: 1px solid #e5e4e2;
}

.tier-건물주 {
  background: rgba(185, 242, 255, 0.2);
  color: #b9f2ff;
  border: 1px solid #b9f2ff;
}

.username {
  color: #f0f;
  font-weight: bold;
}

.action-btn {
  background: transparent;
  border: 1px solid #f0f;
  color: #f0f;
  padding: 0.4rem;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.5rem;
}

.edit-btn:hover {
  background: rgba(0, 255, 255, 0.2);
  border-color: #0ff;
  color: #0ff;
}

.delete-btn:hover {
  background: rgba(255, 0, 0, 0.2);
  border-color: #ff0000;
  color: #ff0000;
}

.cyber-edit-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid #f0f;
  border-radius: 4px;
  color: #fff;
  padding: 0.5rem;
  font-family: 'DungGeunMo';
}

/* 스크롤바 스타일 */
.comments-container::-webkit-scrollbar {
  width: 8px;
}

.comments-container::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 10px;
}

.comments-container::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 10px;
  box-shadow: 0 0 10px #f0f;
}

@keyframes glitch {
  0% { text-shadow: 2px 2px #0ff; }
  25% { text-shadow: -2px 2px #f0f; }
  50% { text-shadow: 2px -2px #0ff; }
  75% { text-shadow: -2px -2px #f0f; }
  100% { text-shadow: 2px 2px #0ff; }
}
</style>
