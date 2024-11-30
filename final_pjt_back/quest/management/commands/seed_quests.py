# 11-20 윤희준 퀘스트, 훈련장 쓸 장고 작성

from django.core.management.base import BaseCommand
from quest.models import QuestCategory, Quest

data = {
    "예적금": [
        {"question": "예금과 적금중 매달 일정 금액을 납입하는 것은 ?", "answer": "적금"},
        {"question": "적금의 이자 계산 방식은 단리와 복리중 무엇이 일반적인가요?", "answer": "단리"},
        {"question": "예금과 적금 중 목돈을 한 번에 예치하는 방식은 ?", "answer": "예금"},
        {"question": "예금이나 적금으로 받은 이자에 부과되는 세금은 무엇인가요 ?", "answer": "이자소득세"},
        {
            "question": "적금 가입 시 이자율에 영향을 미치는 우대 조건이 아닌것은 ?",
            "answer": "4",
            "choices": ["1. 자동이체", "2. 신규 가입", "3. 급여 이체", "4. 부채유무"],
        },
    ],
    "달러": [
        {"question": "전 세계의 외환거래 시장에서 외환을 거래하는 행위는 ?", "answer": "딜링"},
        {
            "question": "달러화 가치를 보여주는 지표인 ‘달러인덱스’에 영향을 미치지 않는 화폐는?",
            "answer": "4",
            "choices": ["1. 유로", "2. 엔", "3. 파운드", "4. 위안"],
        },
        {"question": "보안이나 자산의 매수 가격과 매도 가격 사이의 차이를 의미하는 단어는 ?", "answer": "스프레드"},
        {"question": "저금리로 돈을 빌려 고금리로 투자하는 거래 전략을 뜻하는 단어는 ?", "answer": "캐리 트레이드"},
        {"question": "트레이더가 거래 계정에 보유한 금융 상품들의 모음을 의미하는 단어는 ?", "answer": "포트폴리오"},
    ],
    "청약": [
        {
            "question": "주택청약종합저축 통장의 가입 조건으로 올바른 것은 무엇인가요?",
            "answer": "4",
            "choices": ["1. 18세 이상", "2. 무주택자", "3. 소득 제한 없음", "4. 모두 해당"],
        },
        {
            "question": "주택청약제도에서 청약 가점을 계산하는 기준이 아닌 것은 무엇인가요 ?",
            "answer": "3",
            "choices": ["1. 무주택 기간", "2. 부양 가족 수", "3. 소득 수준", "4. 청약 통장 가입 기간"],
        },
        {
            "question": "주택청약제도에서 1순위 자격을 얻기 위한 최소 가입 기간은 얼마인가요?",
            "answer": "2",
            "choices": ["1. 6개월", "2. 12개월", "3. 24개월", "4. 36개월"],
        },
        {
            "question": "1순위 자격을 얻기 위해 필요한 최소 무주택 기간은 얼마인가요?",
            "answer": "2",
            "choices": ["1. 1년", "2. 2년", "3. 3년", "4. 4년"],
        },
        {
            "question": "‘특별공급’이란 무엇을 의미하나요?",
            "answer": "1",
            "choices": [
                "1. 장애인, 다자녀 가구 등을 위한 우선 공급",
                "2. 무주택자 우선 공급",
                "3. 고소득층 우선 공급",
                "4. 청년층 우선 공급",
            ],
        },
    ],
    "주식": [
        {
            "question": "코스피지수나 코스닥지수가 각각 8%, 15%, 20% 하락할 때마다 거래를 정지하는 제도는?",
            "answer": "2",
            "choices": ["1. 사이드카", "2. 서킷브레이커", "3. 빅스텝", "4. 자이언트스텝"],
        },
        {
            "question": "주식을 대량으로 보유한 쪽이 사전에 매수자를 구해 지분을 넘기는 거래는?",
            "answer": "1",
            "choices": ["1. 블록딜", "2. 메가딜", "3. 자전거래", "4. 공정무역"],
        },
        {
            "question": "주식을 쪼개 한 주당 가격을 낮추는 조치는?",
            "answer": "3",
            "choices": ["1. 상장폐지", "2. 인적분할", "3. 액면분할", "4. 물적분할"],
        },
        {
            "question": "한 주 가격이 1000원이 안 되는 주식을 가리키는 별명은?",
            "answer": "4",
            "choices": ["1. 황제주", "2. 배당주", "3. 우선주", "4. 동전주"],
        },
        {
            "question": "‘매그니피센트 세븐’에 해당하지 않는 종목은?",
            "answer": "4",
            "choices": ["1. 마이크로소프트", "2. 테슬라", "3. 아마존", "4. 토요타"],
        },
    ],
    "부동산": [
        {
            "question": "경매에서 가장 높은 금액을 제출한 사람에게 매각허가 결정이 나는 절차는?",
            "answer": "낙찰",
        },
        {
            "question": "매수자가 없을 경우 다음 매각기일에 저감하여 다시 실시하는 것을 무엇이라 하는가?",
            "answer": "1",
            "choices": ["1. 유찰", "2. 연기", "3. 낙찰", "4. 상계"],
        },
        {
            "question": "채무자 소유의 부동산을 압류하고 매각대금으로 채권자의 만족을 얻는 절차는?",
            "answer": "1",
            "choices": ["1. 강제경매", "2. 부동산인도명령", "3. 이중경매", "4. 임의경매"],
        },
        {
            "question": "다음 중 부동산 거래세로 볼 수 있는 것은?",
            "answer": "1",
            "choices": ["1. 취득세", "2. 부가가치세", "3. 상속세", "4. 주민세"],
        },
        {
            "question": "경매 입찰 시 최저매각가격에 몇 퍼센트를 입찰 보증금으로 내야 하는가?",
            "answer": "3",
            "choices": ["1. 3%", "2. 5%", "3. 10%", "4. 15%"],
        },
    ],
}
class Command(BaseCommand): # BaseCommand를 상ㄹ속받아 새로 정의한 커스텀 명령어 클래스 , Command << 이름은 정해져있음 Django 의 규칙
    help = "Seed quest data" # help 는 써도되고 안써도되는듯? 

    def handle(self, *args, **kwargs):
        for category_name, quests in data.items():
            category, created = QuestCategory.objects.get_or_create(name=category_name)
            for quest in quests:
                Quest.objects.get_or_create(
                    category=category, 
                    question=quest["question"], 
                    answer=quest["answer"], 
                    choices=quest.get("choices", None)
                    )
        self.stdout.write(self.style.SUCCESS("Quest data seeded successfully!")) # 데이터 넣기 성공하면 " " 문구 나옴

