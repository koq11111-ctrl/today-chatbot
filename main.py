import os
from fastapi import FastAPI, Request
from openai import OpenAI

app = FastAPI()

# OpenAI API Key 설정 (서버 환경 변수에서 가져옴)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE"))

# 오늘통신 선불폰 개통 전용 AI 상담원 프롬프트
SYSTEM_PROMPT = """
너는 선불폰 개통 전문 브랜드 '오늘통신'의 친절하고 스마트한 24시간 AI 상담원이야.
아래 오늘통신의 핵심 안내 규정과 지식을 바탕으로 고객의 질문에 명확하고 친절하게 답변해줘.

[오늘통신 개통 핵심 규정 및 지식]
1. 선불폰이란?
   - 통화, 문자, 데이터 요금을 미리 충전하여 사용하는 합리적인 요금제.
   - 통신 연체, 미납, 신용회복, 개인회생 중이거나 신용불량 상태여도 본인 명의 인증서만 있다면 100% 개통 가능.
2. 개통 방식 (비대면 셀프 개통):
   - 필수 인증서: 카카오, 토스, 국민, PASS, 삼성패스, 신한, 페이코 중 1가지 필수.
   - 개통 사이트: 개통홈페이지 (오늘통신.com) 접속 -> '개통하기' 클릭 -> KT망 또는 LG망 선택 -> 본인인증 -> 유심 정보 입력 -> 개통 완료 후 재부팅 2~3회.
3. 번호이동 주의사항:
   - 기존 통신사에 연체나 미납이 있는 경우 번호이동 불가능 (신규개통으로 진행해야 함).
4. 망별 유심(USIM) 구입 가이드:
   - K망 (KT망): '바로유심' (8,800원) - 이마트24, CU, GS25 편의점에서 구매 (민트색 배경에 고양이 그림).
   - L망 (LG망): '모두의원칩' (8,800원) - 이마트24 편의점, 배민B마트에서 구매 (검정색 사각형 디자인).
5. 대표 요금제:
   - 선불 396 10.3GB: 월 39,600원 / 데이터 10.3GB + 3Mbps 무제한 / 통화·문자 기본제공 (가장 인기)
   - 선불 459 20.3GB: 월 45,900원 / 데이터 20.3GB + 3Mbps 무제한 / 데이터 다량 사용자용
6. 개통 후 세팅 & 요금 충전:
   - 개통 완료 후 단말기에 유심을 넣고 2~3회 재부팅 필수.
   - 요금 충전: 홈페이지 또는 앤텔레콤 멤버십 앱 이용.

[답변 작성 가이드]
- 카카오톡 화면에서 읽기 쉽도록 너무 길지 않고 깔끔한 단락으로 작성할 것.
- 핵심 키워드는 강조하고 필요 시 이모지를 적절히 사용할 것.
- 친절하고 전문적인 어조 유지.
"""

@app.post("/kakao-chat")
async def kakao_chat(request: Request):
    try:
        body = await request.json()
        # 고객이 카카오톡 채널에 입력한 메시지 추출
        user_message = body.get("userRequest", {}).get("utterance", "")
        
        if not user_message:
            user_message = "안녕하세요"

        # OpenAI ChatGPT API 호출 (gpt-4o-mini 가성비 모델 사용)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3
        )

        ai_answer = response.choices[0].message.content

    except Exception as e:
        ai_answer = f"죄송합니다. 서비스 처리 중 오류가 발생했습니다: {str(e)}"

    # 카카오톡 오픈빌더 규격에 맞춘 JSON 응답 구조
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": ai_answer
                    }
                }
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```[cite: 2]

3. 메모장 상단 **[파일] ➔ [다른 이름으로 저장]**을 누릅니다.
   * **파일 이름**: `main.py`
   * **파일 형식**: `모든 파일 (*.*)`로 변경 **(★매우 중요)**
4. **[저장]**을 누릅니다.

---

## ✅ 점검하기

여기까지 완료하셨다면, `today_chatbot` 폴더 안에 **딱 2개의 파일**이 존재하게 됩니다.

* `requirements.txt`[cite: 1]
* `main.py`[cite: 2]

이 두 개의 파일이 준비되셨다면 **"2단계 준비"는 완벽하게 끝난 것입니다!**

다음으로 이 파일들을 인터넷 상에 올리기 위한 **'3단계: GitHub에 코드 올려서 Render.com 서버 연결하기'** 단계로 진행할까요?