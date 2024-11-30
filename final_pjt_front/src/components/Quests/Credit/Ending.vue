<template>
  <div class="credits-container" ref="container">
    <div class="credits-content">
      <section class="credits-section">
        <h2>20대에 꼭 해야 할 10가지 일</h2>
        <div class="credit-item" v-for="(item, index) in twentyTips" :key="'twenty-'+index">
          <h3>{{ item.title }}</h3>
          <p>{{ item.content }}</p>
        </div>
      </section>

      <section class="credits-section">
        <h2>성공한 인생을 위해 30대에 시작해야 할 14가지</h2>
        <div class="credit-item" v-for="(item, index) in thirtyTips" :key="'thirty-'+index">
          <h3>{{ item.title }}</h3>
          <p>{{ item.content }}</p>
        </div>
      </section>

      <section class="credits-section cast">
        <h2>Dummy Data Cast</h2>
        <div class="cast-grid">
          <div class="cast-item" v-for="(user, index) in dummyDataCast" :key="'cast-'+index">
            <span>{{ user.role }}</span>
            <span class="cast-name">{{ user.name }}</span>
          </div>
        </div>
      </section>

      <section class="credits-section special">
        <h2>Special Guest</h2>
        <div class="special-item memory">故 정승권 😥</div>
        <div class="special-item">신 민석 강사님</div>
        <div class="special-item">김 혜빈 프로님</div>
      </section>

      <section class="credits-section team">
        <div class="team-member">
          <h3>Front</h3>
          <div class="special-item">⭐윤 희준🌈</div>
        </div>
        <div class="team-member">
          <h3>Back</h3>
          <div class="special-item">🌈신 희원 ⭐</div>
        </div>
      </section>

      <section class="credits-section sponsor">
        <h2>Logo Sponsor</h2>
        <div class="special-item">유 한슬 디자인팀장</div>
      </section>

      <div class="final-logos">
        <img src="/wg_line.png" alt="Team Logo" class="team-logo">
        <img src="/wg_controller_color.png" alt="Controller Logo" class="controller-logo">
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const twentyTips = [
  { 
    title: "1. 시급을 고려하지 말고 일하라.",
    content: "하고 싶은 일을 선택해서 그 일에서 보람을 찾아라. 정말 멋진 일이지만, 나중에 가족이 생기고 돈 나갈 일이 많이 생기면 도저히 할 수 없으니 20대에 꼭 해보라."
  },
  {
    title: "2. 사색하는 일상을 시작하라.",
    content: "창조와 상상의 시작은 사색이다. 조금이라도 빨리 <사색이 자본이다> 라는 책을 읽고 사색하며 살아가는 삶이 얼마나 자신을 강하게 만드는지 느껴보길 바란다."
  },
  {
    title: "3. 가장 매력적인 외모로 자신을 다듬자.",
    content: "20대의 매력은 외모다. 그냥 그 자체로도 아름답지만 조금만 더 다듬고 자신을 가꾸면 더 멋지게 만들 수 있다. 20대만 보여줄 수 있는 매력을 놓치지 말라."
  },
  {
    title: "4. 실천하는 자기계발 작가를 만나라.",
    content: "20대는 삶의 기초를 다지는 시기다. 책에는 다양한 장르가 있지만 나는 자기계발 작가를 만나 그들이 살아가는 일상을 관찰하길 바란다."
  },
  {
    title: "5. 매일 30분 글을 써라.",
    content: "글을 배우면 말은 저절로 잘하게 된다. 사색하며 글을 쓰는 동안 두뇌에 멋진 말이 저절로 저장되기 때문이다. 그을 써라. 제발 써라."
  },
  {
    title: "6. 당분간 자기 자신만 생각하라.",
    content: "고독은 좋은 것이다. 하지만 30대 이후의 삶은 쉽게 고독하기도 힘든 나날의 연속이다. 다양한 이유로 무리에 섞여 지내야한다."
  },
  {
    title: "7. 할 일을 찾았다면 대학은 빨리 그만두자.",
    content: "당신이 대학 4학년이라도 상관없다. 할 일을 찾았다면 졸업장은 쓸모없는 종이일 뿐이다. 나중에는 시간이 아쉬워진다."
  },
  {
    title: "8. 미치도록 신나게 슬프게 사랑하라.",
    content: "20대는 가장 몸과 마음이 뜨거운 시기다. 계절에는 나름의 특징이 있는 것 처럼, 20대는 그 뜨거운 것을 실천 하며 살아야 하는 시기다."
  }
]

const thirtyTips = [
  {
    title: "1. 담배를 끊는다.",
    content: "지금까지 흡연에 의한 피해를 취소할 수는 없지만, 연구에 따르면 40세 이전에 담배를 그만 둔 사람의 사망위험은 피우는 사람보다 훨씬 낮아진다."
  },
  {
    title: "2. 매일 같은 시간에 일어나고, 잔다.",
    content: "평소의 수면 부족을 되찾는다고 주말 등에 많이 자버리면, 몸의 사이클이 흐트러지는 위험이 있다고 전문가들은 말하고 있다."
  },
  {
    title: "3. 정기적으로 운동을 한다.",
    content: "30대부터 근육량이 떨어지기 시작하기 때문에, 이 나이에 운동은 특히 중요하다. 그렇지만 즐길 수 있는 운동을 선택하도록 하자."
  },
  {
    title: "4. 일기를 쓴다.",
    content: "생각과 느낌을 내보낼 수 있어 스트레스에 대한 대처법도 된다."
  },
  {
    title: "5. 저축을 시작한다.",
    content: "미래를 위한 저축은 30대부터 시작해야 한다."
  },
  {
    title: "6. 인생의 꿈을 쫓기 시작한다.",
    content: "진정한 꿈을 찾고 그것을 향해 나아가야 할 시기이다."
  },
  {
    title: "7. 지금의 자신을 긍정하는 것을 배운다.",
    content: "자신을 있는 그대로 받아들이고 긍정하는 것이 중요하다."
  },
  {
    title: "8. 모두를 만족시키려 한다.",
    content: "만나면 즐거운 사람들과의 시간을 늘리고 에너지를 현명하게 사용하는 것은 중요."
  },
  {
    title: "9. 누군가와 비교하는 것을 끝낸다.",
    content: "자신과 다른 사람을 비교하는 것은 비생산적인것. 과학적으로도 증명되고 있다."
  },
  {
    title: "10. 자신의 실수를 용서한다.",
    content: "자신에게 동정심을 가지는 것이 성공의 중요한 열쇠라고 지적하고 있다."
  },
  {
    title: "11. 자신의 가치를 명확하게 한다.",
    content: "자신이 중요하게 생각하는 가치를 정립하는 것이 필요하다."
  },
  {
    title: "12. 1일 1시간, 독서한다.",
    content: "1일 1시간 독서라면, 1년에 15일 동안 독서 한 것이다."
  },
  {
    title: "13. 정리",
    content: "혼란한 것은 다른 사람이나 가족에게 스트레스의 원인이 될 수있다. 하지만 사람은 지저분한 환경에서 창조적인 경향도 있다."
  },
  {
    title: "14. 다른 사람을 판단하는 것을 종료한다.",
    content: "타인에 대한 판단을 멈추고 이해하려 노력하는 것이 중요하다."
  }
]

const dummyDataCast = [
  { role: "user 1", name: "정 재혁" },
  { role: "user 2", name: "강 건준" },
  { role: "user 3", name: "한 이경" },
  { role: "user 4", name: "김 민철" },
  { role: "user 5", name: "김 지원" },
  { role: "user 6", name: "윤 재은" },
  { role: "user 7", name: "권 남희" },
  { role: "user 8", name: "유 한슬" },
  { role: "user 9", name: "이 지은" },
  { role: "user 10", name: "이 정인" },
  { role: "user 11", name: "황 학선" },
  { role: "user 12", name: "손 재민" },
  { role: "user 13", name: "김 세희" },
  { role: "user 14", name: "박 찬미" },
  { role: "user 15", name: "임 남기" },
  { role: "user 16", name: "정 수연" },
  { role: "user 17", name: "김 동해" },
  { role: "user 18", name: "신 우진" },
  { role: "user 19", name: "김 서린" },
  { role: "user 20", name: "박 성욱" }
]

onMounted(() => {
  startScrollAnimation()
})

const container = ref(null)

function startScrollAnimation() {
  if (container.value) {
    const duration = 120000 // 2분으로 단축
    const content = container.value.querySelector('.credits-content')
    const contentHeight = content.offsetHeight
    const windowHeight = window.innerHeight
    
    content.style.transform = 'translateY(' + windowHeight + 'px)'
    
    setTimeout(() => {
      content.style.transition = `transform ${duration}ms linear`
      content.style.transform = 'translateY(-' + (contentHeight + 100) + 'px)'
    }, 1000)
  }
}
</script>

<style scoped>
/* 이전 스타일 코드는 동일하게 유지 */
.credits-container {
  background: #000;
  color: #fff;
  min-height: 100vh;
  overflow: hidden;
  position: relative;
  font-family: 'DungGeunMo', sans-serif;
}

.credits-content {
  position: relative;
  padding: 2rem;
  width: 80%;
  max-width: 800px;
  margin: 0 auto;
}

.credits-section {
  margin-bottom: 4rem;
  text-align: center;
}

.credits-section h2 {
  color: #FFD700;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-transform: uppercase;
}

.credit-item {
  margin-bottom: 2rem;
}

.credit-item h3 {
  color: #fff;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.credit-item p {
  color: #ccc;
  line-height: 1.6;
}

.cast-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  justify-items: center;
}

.cast-item {
  display: flex;
  gap: 1rem;
  color: #ccc;
}

.cast-name {
  color: #fff;
}

.special-item {
  font-size: 1.3rem;
  color: #fff;
  margin: 1rem 0;
}

.special-item.memory {
  color: #FFD700;
  font-size: 1.5rem;
}

.team-member {
  margin: 2rem 0;
}

.team-member h3 {
  color: #FFD700;
  font-size: 1.5rem;
}

.final-logos {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  margin-top: 4rem;
  padding: 2rem;
}

.team-logo {
  width: 300px;
  height: auto;
  filter: brightness(1.2);
}

.controller-logo {
  width: 200px;
  height: auto;
  animation: glow 2s infinite alternate;
}

@keyframes glow {
  from {
    filter: drop-shadow(0 0 2px #fff) drop-shadow(0 0 4px #fff);
  }
  to {
    filter: drop-shadow(0 0 4px #fff) drop-shadow(0 0 8px #fff);
  }
}

@media (max-width: 768px) {
  .credits-content {
    width: 90%;
    padding: 1rem;
  }

  .credits-section h2 {
    font-size: 1.5rem;
  }

  .cast-grid {
    grid-template-columns: 1fr;
  }

  .team-logo, .controller-logo {
    width: 80%;
  }

  .credit-item h3 {
    font-size: 1rem;
  }

  .credit-item p {
    font-size: 0.9rem;
  }

  .special-item {
    font-size: 1.1rem;
  }
}
</style>