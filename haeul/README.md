# AI 장소 추천 빈칸 실습

## 배포
학생에게는 student 폴더만 배포하세요. instructor/main.py는 강사용 정답입니다.
student를 ai-place-demo로 이름을 바꾸어 VS Code에서 폴더를 여세요.
.env.example을 복사해 .env로 저장하고 키 2개를 넣으세요. 수업 모델은 gemini-flash-latest이며 .env.example에 미리 입력되어 있습니다.
.env는 main.py와 같은 폴더에 둡니다. 실제 키는 제출하지 않습니다.
기존 PC 폴더는 덮어쓰지 않았습니다. 이전 search_demo.py는 이번 실습에 필요 없습니다.

## 사전 설치
가상환경을 쓰면 먼저 생성합니다: `python3 -m venv .venv` (Windows: `python -m venv .venv`).
Mac: `source .venv/bin/activate`
Windows Git Bash: `source .venv/Scripts/activate`
`python -m pip install -r requirements.txt`
가상환경은 선택이며 생략한 경우 설치된 Python 명령을 사용합니다.

## 수업 진행
1. main.py의 📍1부터 📍3까지 채웁니다.
2. 📍 번호가 적힌 문자열의 따옴표까지 모두 교체합니다. PPT의 줄 번호는 새로 배포한 파일 기준입니다. 코드 들여쓰기는 유지합니다.
3. `python main.py`로 실행하고 지역·업종과 조건을 입력합니다.
4. 장소 목록을 확인하고 Gemini 실행 질문에는 Enter를 눌러 종료합니다.
5. 빈칸 4~6을 완성해 다시 실행하고 Gemini 실행 질문에 y를 입력합니다.
6. 후보와 추천 결과의 이름·주소·링크를 비교합니다.
7. rules에 아래 규칙을 덧붙이고 다시 실행해 표현 차이를 살펴봅니다.

추가 규칙 예시: 제공한 정보로만 추천 이유를 설명하세요. 분위기·가격·좌석·영업시간을 모르면 추가 확인 필요라고 쓰세요.
다시 실행하면 검색 후보가 달라질 수 있습니다. 이번 활동은 같은 후보를 고정한 실험이 아니라 결과를 살펴보는 활동입니다.

## 빈칸 안내

1. 검색어 전달

2. JSON 응답 읽기

3. 장소 목록 선택

4. 추천 규칙 작성

5. 후보를 JSON 문자열로 변환

6. Gemini에 프롬프트 전달
