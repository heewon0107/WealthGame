import { defineStore } from "pinia"
import { ref, computed, watch } from 'vue'

export const useMapStore = defineStore('map', () => {
  
  const address = ref(null)
  const city = ref('')
  const area = ref('')

  const addressWatch = watch(address, (newValue) => {
    const splited = newValue.split(' ')
    city.value = splited[0]
    area.value = splited[1]
  })



  return { city, area}
}, { persist: true })
