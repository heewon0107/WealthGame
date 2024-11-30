<template>
  <div class="arcade-map-container">
    <div class="cyber-header">
      <div class="glitch-text" data-text="BANK RADAR">BANK RADAR</div>
      <div class="sub-text">내 주변 은행을 찾아보세요!</div>
    </div>

    <div class="search-panel">
      <div class="select-group">
        <div class="cyber-select">
          <span class="select-label">CITY</span>
          <select v-model="cityInput" class="neon-select">
            <option value="" disabled>시/도 선택</option>
            <option v-for="city in cityList" :value="city">{{ city }}</option>
          </select>
        </div>

        <div class="cyber-select">
          <span class="select-label">AREA</span>
          <select v-model="areaInput" class="neon-select">
            <option value="" disabled>지역 선택</option>
            <option value="all" v-if="cityInput">전체</option>
            <option v-for="area in areaObj[cityInput]" :value="area">{{ area }}</option>
          </select>
        </div>

        <div class="cyber-select">
          <span class="select-label">BANK</span>
          <select v-model="bankInput" class="neon-select">
            <option value="" disabled>은행 선택</option>
            <option value="은행">전체</option>
            <option v-for="bank in bankList" :value="bank">{{ bank }}</option>
          </select>
        </div>

        <button @click="search" class="cyber-button">
          <span class="button-line"></span>
          <span class="button-line"></span>
          <span class="button-text">SCAN</span>
          <span class="button-line"></span>
          <span class="button-line"></span>
        </button>
      </div>

      <div class="map-container">
        <div class="map-frame">
          <div class="scanner-line"></div>
          <div ref="container" class="map-content"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMapStore } from '@/stores/map'

const store = useMapStore()
const cityInput = ref(store.city)
const areaInput = ref(store.area)
const bankInput = ref('')

const cityList = [
  "서울특별시",
  "인천광역시",
  "대전광역시",
  "광주광역시",
  "대구광역시",
  "울산광역시",
  "부산광역시",
  "경기도",
  "강원도",
  "충청북도",
  "충청남도",
  "전라북도",
  "전라남도",
  "경상북도",
  "경상남도",
  "제주도"
]

const areaObj = {
    "서울특별시": ["강남구","강동구","강북구","강서구","관악구","광진구","구로구","금천구","노원구","도봉구","동대문구","동작구","마포구","서대문구","서초구","성동구","성북구","송파구","양천구","영등포구","용산구","은평구","종로구","중구","중랑구"],
    "인천광역시": ["계양구","남구","남동구","동구","부평구","서구","연수구","중구","강화군","옹진군"],
    "대전광역시": ["대덕구","동구","서구","유성구","중구"],
    "광주광역시": ["광산구","남구","동구", "북구","서구"],
    "대구광역시": ["남구","달서구","동구","북구","서구","수성구","중구","달성군"],
    "울산광역시": ["남구","동구","북구","중구","울주군"],
    "부산광역시": ["강서구","금정구","남구","동구","동래구","부산진구","북구","사상구","사하구","서구","수영구","연제구","영도구","중구","해운대구","기장군"],
    "경기도": ["고양시","과천시","광명시","광주시","구리시","군포시","김포시","남양주시","동두천시","부천시","성남시","수원시","시흥시","안산시","안성시","안양시","양주시","오산시","용인시","의왕시","의정부시","이천시","파주시","평택시","포천시","하남시","화성시","가평군","양평군","여주군","연천군"],
    "강원도": ["강릉시","동해시","삼척시","속초시","원주시","춘천시","태백시","고성군","양구군","양양군","영월군","인제군","정선군","철원군","평창군","홍천군","화천군","횡성군"],
    "충청북도": ["제천시","청주시","충주시","괴산군","단양군","보은군","영동군","옥천군","음성군","증평군","진천군","청원군"],
    "충청남도": ["계룡시","공주시","논산시","보령시","서산시","아산시","천안시","금산군","당진군","부여군","서천군","연기군","예산군","청양군","태안군","홍성군"],
    "전라북도": ["군산시","김제시","남원시","익산시","전주시","정읍시","고창군","무주군","부안군","순창군","완주군","임실군","장수군","진안군"],
    "전라남도": ["광양시","나주시","목포시","순천시","여수시","강진군","고흥군","곡성군","구례군","담양군","무안군","보성군","신안군","영광군","영암군","완도군","장성군","장흥군","진도군","함평군","해남군","화순군"],
    "경상북도": ["경산시","경주시","구미시","김천시","문경시","상주시","안동시","영주시","영천시","포항시","고령군","군위군","봉화군","성주군","영덕군","영양군","예천군","울릉군","울진군","의성군","청도군","청송군","칠곡군"],
    "경상남도": ["거제시","김해시","마산시","밀양시","사천시","양산시","진주시","진해시","창원시","통영시","거창군","고성군","남해군","산청군","의령군","창녕군","하동군","함안군","함양군","합천군"],
    "제주도": ["서귀포시","제주시","남제주군","북제주군"],
}

const bankList = [
  '경남은행',
  '국민은행',
  '광주은행',
  '기업은행',
  '농협',
  '대구은행',
  '부산은행',
  '산업은행',
  '새마을금고',
  '수협',
  '신한은행',
  '신협',
  '씨티은행',
  '우리은행',
  '전북은행',
  '제주은행',
  '하나은행',
  'sc제일은행',
]

let map = null
let infowindow = null
let markerList = []
const container = ref(null)

const initMap = () => {
  let lat = 37.5509646154244
  let lng = 127.0276
  
  if (cityInput.value && areaInput.value) {
    const geocoder = new kakao.maps.services.Geocoder()
    geocoder.addressSearch(`${cityInput.value} ${areaInput.value}`, (result, status) => {
      if (status === kakao.maps.services.Status.OK) {
        const options = {
          center: new kakao.maps.LatLng(result[0].y, result[0].x),
          level: 3
        }
        map = new kakao.maps.Map(container.value, options)
        const zoomControl = new kakao.maps.ZoomControl()
        map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT)
        infowindow = new kakao.maps.InfoWindow({zIndex:1})
        return
      }
    })
  } 

  const options = {
    center: new kakao.maps.LatLng(lat, lng),
    level: 3
  }
  map = new kakao.maps.Map(container.value, options)
  const zoomControl = new kakao.maps.ZoomControl()
  map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT)
  infowindow = new kakao.maps.InfoWindow({zIndex:1})
}

const loadScript = function() {
  const key = import.meta.env.VITE_API_KEY
  const script = document.createElement('script')
  
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${key}&libraries=services`
  script.addEventListener('load', () => kakao.maps.load(initMap))
  document.head.appendChild(script)
}

function placesSearchCB (data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {
        var bounds = new kakao.maps.LatLngBounds()

        for (var i=0; i<data.length; i++) {
            const marker = new kakao.maps.Marker({
              map: map,
              position: new kakao.maps.LatLng(data[i].y, data[i].x) 
            })     
            const tag = `<div class="custom-infowindow">${data[i].place_name}</div>`
            bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x))
            kakao.maps.event.addListener(marker, 'click', function() {
                infowindow.setContent(tag)
                infowindow.open(map, marker)
            })
            markerList.push(marker)
        }

        map.setBounds(bounds)
    } 
}

function resetMarker() {
  markerList.forEach((marker) => {
    marker.setMap(null)
  })

  markerList.length = 0
}

const search = function() {
  resetMarker()
  const ps = new kakao.maps.services.Places()
  if (!cityInput.value) {
    window.alert('시/도를 선택하세요.')
  } else if (!areaInput.value) {
    window.alert('지역을 선택하세요.')
  } else if (!bankInput.value) {
    window.alert('은행을 선택하세요')
  } else {
    let keyword = `${cityInput.value} ${areaInput.value} ${bankInput.value}`
    keyword = keyword.replace(' all', '')
    ps.keywordSearch(keyword, placesSearchCB)
  }
}

onMounted(() => {
  if (window.kakao?.maps) {
    console.log('맵 있음', window.kakao.maps)
    initMap()
  } else {
    console.log('load 필요')
    loadScript()
  }
})

</script>

<style scoped>
.arcade-map-container {
  padding: 2rem;
  color: #fff;
  font-family: 'DungGeunMo', sans-serif;
  height: calc(110vh - 4rem);  
  overflow-y: auto;  
  margin-bottom: 2rem;
}
.arcade-map-container::-webkit-scrollbar {
  width: 8px;
}

.arcade-map-container::-webkit-scrollbar-track {
  background: rgba(255, 0, 255, 0.1);
  border-radius: 10px;
}

.arcade-map-container::-webkit-scrollbar-thumb {
  background: #f0f;
  border-radius: 10px;
  box-shadow: 0 0 10px #f0f;
}

.arcade-map-container::-webkit-scrollbar-thumb:hover {
  background: #f0f;
  box-shadow: 0 0 15px #f0f;
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

.sub-text {
  font-size: 1.2rem;
  color: #fff;
  text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
  margin-top: 0.5rem;
}

.search-panel {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #f0f;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.2);
}

.select-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.cyber-select {
  flex: 1;
  min-width: 200px;
}

.select-label {
  display: block;
  color: #f0f;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 5px rgba(255, 0, 255, 0.5);
}

.neon-select {
  width: 100%;
  padding: 0.8rem;
  background: rgba(0, 0, 0, 0.7);
  border: 2px solid #f0f;
  border-radius: 8px;
  color: #fff;
  font-family: 'DungGeunMo';
  outline: none;
}

.neon-select:focus {
  box-shadow: 0 0 15px #f0f;
}

.cyber-button {
  padding: 0.8rem 2rem;
  background: transparent;
  border: none;
  color: #fff;
  font-family: 'DungGeunMo';
  font-size: 1.2rem;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  min-width: 150px;
  margin-top: 1.5rem;
}

.button-line {
  position: absolute;
  background: #f0f;
}

.button-line:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  transform: translateX(-100%);
  animation: line1 2s infinite;
}

.button-line:nth-child(2) {
  top: 0;
  right: 0;
  width: 2px;
  height: 100%;
  transform: translateY(-100%);
  animation: line2 2s infinite;
}

.map-container {
  margin-top: 2rem;
}

.map-frame {
  position: relative;
  border: 2px solid #f0f;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.5);
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
  z-index: 1;
}

.map-content {
  width: 100%;
  height: 600px;
  position: relative;
  z-index: 0;
}

@keyframes scan {
  0% { top: 0; }
  100% { top: 100%; }
}

@keyframes line1 {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes line2 {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

@keyframes glitch {
  0% { text-shadow: 2px 2px #0ff; }
  25% { text-shadow: -2px 2px #f0f; }
  50% { text-shadow: 2px -2px #0ff; }
  75% { text-shadow: -2px -2px #f0f; }
  100% { text-shadow: 2px 2px #0ff; }
}

/* 인포윈도우 스타일 커스텀 */
:deep(.custom-infowindow) {
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #f0f;
  border-radius: 4px;
  padding: 8px 12px;
  color: #fff;
  font-family: 'DungGeunMo';
  box-shadow: 0 0 10px rgba(255, 0, 255, 0.3);
}

@media (max-width: 768px) {
  .select-group {
    flex-direction: column;
  }

  .cyber-select {
    width: 100%;
  }

  .map-content {
    height: 400px;
  }
}
</style>