import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    // localStorage에서 tier를 가져오거나, 없으면 기본값 사용
    tier: localStorage.getItem('userTier') || '알거지'
  }),
  
  actions: {
    async fetchUserTier() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('http://127.0.0.1:8000/accounts/profile_view/', {
          headers: {
            'Authorization': `Token ${token}`
          }
        })
        this.tier = response.data.tier     
        // localStorage에 tier 저장
        localStorage.setItem('userTier', response.data.tier)
      } catch (error) {
        console.error('티어 정보 가져오기 실패:', error)
      }
    },

    async updateTier(newTier) {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.put(
          'http://127.0.0.1:8000/accounts/update_tier/',
          { tier: newTier },
          {
            headers: {
              'Authorization': `Token ${token}`
            }
          }
        )
        if (response.data.success) {
          this.tier = newTier
          // localStorage에 새로운 tier 저장
          localStorage.setItem('userTier', newTier)
          return true
        }
        return false
      } catch (error) {
        console.error('티어 업데이트 실패:', error)
        return false
      }
    }
  }
})