import { defineStore } from 'pinia'



export const useGameStore = defineStore('game', {
  
  
},
{ 
  persist: {
  storage: sessionStorage,
  paths: ['token',]
}
 })


