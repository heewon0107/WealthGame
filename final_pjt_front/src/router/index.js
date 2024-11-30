import { createRouter, createWebHistory } from 'vue-router'
//회원가입, 로그인, 찜콩목록
import SignUpView from '@/views/Accounts/SignUpView.vue'
import SignInView from '@/views/Accounts/SignInView.vue'


// 시작화면
import StartView from '@/views/StartView.vue'

// 프로필 - 관리, 추천상품, 찜콩목록
import ProfileView from '@/views/Accounts/ProfileView.vue'
import ProfileManagement from '@/components/Profiles/ProfileManagement.vue'
import ProfileSaveItem from '@/components/Profiles/ProfileSaveItem.vue'
import ProfileEdit from '@/components/Profiles/ProfileEdit.vue'
import ProfileRecommendItem from '@/components/Profiles/ProfileRecommendItem.vue'

// 캐시샵
import CashShopView from '@/views/MainFunctions/CashShopView.vue'

// 아이템 - 예적금
import ItemListView from '@/views/MainFunctions/ItemListView.vue'

import ItemDetail from '@/components/Items/ItemDetail.vue'

import ItemDetailDescription from '@/components/Items/ItemDetailConstruct/ItemDetailDescription.vue'
import ItemNearShop from '@/components/Items/ItemDetailConstruct/ItemNearShop.vue'
import ItemCommunity from '@/components/Items/ItemDetailConstruct/ItemCommunity.vue'
import ItemNews from '@/components/Items/ItemDetailConstruct/ItemNews.vue'

// 퀴즈 - 리스트 - 디테일
import QuestView from '@/views/MainFunctions/QuestView.vue'
import QuestList from '@/components/Quests/QuestList.vue'
import QuestListDetail from '@/components/Quests/QuestListDetail.vue'
import QuestCredit from '@/components/Quests/QuestCredit.vue'

// 훈련장 - 리스트 - 디테일(미정 추가예정)
import AcademyView from '@/views/MainFunctions/AcademyView.vue'
import AcademyList from '@/components/Academys/AcademyList.vue'
import Ending from '@/components/Quests/Credit/Ending.vue'





const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 11-18 신희원 회원가입 View 생성.
    // 11-19 윤희준 찜콩목록 View 생성.
    // 회원가입, 로그인, 찜콩목록
    {
      path : '/profile/register',
      name : 'SignUpView',
      component : SignUpView
    },
    {
      path : '/profile/login',
      name : 'SignInView',
      component : SignInView
    },

    //------------------------------- 
    
    // 시작 화면
    {
      path : '/',
      name : 'StartView',
      component : StartView
    },

    //------------------------------- 
    
    // 프로필 - 관리, 추천상품, 찜콩목록
    {
      path : '/profile',
      name : 'ProfileView',
      component : ProfileView,
      children : [
        {
          path : '/profile/management',
          name : 'ProfileManagement',
          component : ProfileManagement
        },
        {
          path : '/profile/recommend/item',
          name : 'ProfileRecommendItem',
          component : ProfileRecommendItem,
          
        },
        {
          path : '/profile/save/item',
          name : 'ProfileSaveItem',
          component : ProfileSaveItem
        },
      ]
    },
    {
      path: '/profile/edit',
      name: 'ProfileEdit',
      component: ProfileEdit
    },

    //------------------------------- 

    // 11-19 신희원 캐시샵 기능 추가
    // 캐시샵
    {
      path : '/cashshop',
      name : 'CashShopView',
      component : CashShopView
    },
    
    //------------------------------- 

    // 11-18 신희원 예적금, 달러 컴포넌트 라우트 생성
    // 11-20 신희원 아이템 디테일 구조 생성
    // 상품리스트, 디테일, 추천, 검색 
    {
      path : '/item_list',
      name : 'ItemListView',
      component : ItemListView,
    },
    {
      path : '/item/:fin_prdt_cd',
      name : 'ItemDetail',
      component : ItemDetail,
      children: [
        {
          path: 'description',
          name: 'ItemDetailDescription',
          component: ItemDetailDescription,
        },
        {
          path: 'near-shop',
          name: 'ItemNearShop',
          component: ItemNearShop,
        },
        {
          path: 'community/:productId',
          name: 'ItemCommunity',
          component: ItemCommunity,
          props: true
        },
        {
          path: 'news/:fin_prdt_nm',
          name: 'ItemNews',
          component: ItemNews,
          props: true
        },
      ]
    },
    
    //------------------------------- 
    

    // 퀴즈(퀘스트) - 리스트, 리스트 디테일 << 수정요망
    // success , fail 어케 띄울까 
    {
      path : '/quest',
      name : 'QuestView',
      component : QuestView,
      children : [
        {
          path : '/quest_list',
          name : 'QuestList',
          component : QuestList
        },
      ]
    },
    
    {
      path : '/quest/detail',
      name : 'QuestListDetail',
      component : QuestListDetail
    },
    {
      path : '/quest/credit',
      name : 'QuestCredit',
      component : QuestCredit
    },

    // ------------------------------
    
    // 훈련장 - 리스트 11-20 윤희준 작성완료
    {
      path : '/academy',
      name : 'AcademyView',
      component : AcademyView,
      children : [
        {
          path : '/academy_list',
          name : 'AcademyList',
          component : AcademyList
        },
      ]
    },

    // 크레딧
    {
      path : '/ending',
      name : 'Ending',
      component : Ending
    }
    

  ],
})

export default router
