import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false)

  function checkLoginStatus() {
    const token = localStorage.getItem('token')
    isLoggedIn.value = !!token
  }

  function setLoginStatus(status) {
    isLoggedIn.value = status
  }

  return {
    isLoggedIn,
    checkLoginStatus,
    setLoginStatus
  }
})