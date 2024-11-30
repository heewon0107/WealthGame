// stores/inventory.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useInventoryStore = defineStore('inventory', () => {
  const inventoryItems = ref({})
  const currentUser = ref(null)

// stores/inventory.js
const initializeInventory = async (userId = null) => {
  const token = localStorage.getItem('token')
  const currentUserId = userId || localStorage.getItem('user_id')
  if (!token || !currentUserId) return

  currentUser.value = currentUserId
  inventoryItems.value = {}
  
  try {
    const products = JSON.parse(sessionStorage.getItem('depositProducts') || '[]')
    
    // Promise.all을 사용하여 모든 요청을 동시에 처리
    const promises = products.map(async product => {
      const response = await axios.get('http://127.0.0.1:8000/bucket/have/', {
        params: { product_id: product.id },
        headers: {
          'Authorization': `Token ${token}`
        }
      })
      return { id: product.id, status: response.data.isAdded }
    })

    const results = await Promise.all(promises)
    results.forEach(({ id, status }) => {
      inventoryItems.value[id] = status
    })

    return true  // 초기화 완료 표시
  } catch (error) {
    console.error('인벤토리 초기화 실패:', error)
    return false
  }
}

  const clearInventory = () => {
    currentUser.value = null
    inventoryItems.value = {}
  }

  const setItemStatus = (productId, status) => {
    if (productId) {
      inventoryItems.value[productId] = status
    }
  }

  const getItemStatus = (productId) => {
    if (!productId) return false
    return inventoryItems.value[productId] || false
  }

  return {
    inventoryItems,
    currentUser,
    initializeInventory,
    clearInventory,
    setItemStatus,
    getItemStatus
  }
})