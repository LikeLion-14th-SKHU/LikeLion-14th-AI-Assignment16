"""AI 장소 추천 실습: 📍1~6을 채우세요. 실행: python main.py"""
import json
import os
import re
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv(Path(__file__).resolve().parent / ".env")


def search_places(query):
    key = os.getenv("KAKAO_REST_API_KEY", "").strip()
    if not key:
        raise ValueError(".env의 KAKAO_REST_API_KEY를 확인하세요.")
    response = requests.get(
        "https://dapi.kakao.com/v2/local/search/keyword.json",
        headers={"Authorization": f"KakaoAK {key}"},
        # 📍1: 함수가 받은 검색어 변수를 전달하세요.
        params={"query": query, "size": 5},
        timeout=10,
    )
    response.raise_for_status()
    # 📍2: 응답을 Python 자료형으로 읽으세요.
    data = response.json()
    # 📍3: data에서 장소 목록을 선택하세요.
    documents = data["documents"]
    return [
        {"name": d["place_name"],
         "address": d["road_address_name"] or d["address_name"],
         "category": d["category_name"],
         "url": d["place_url"]}
        for d in documents
    ]


def build_prompt(user_request, places):
    # 📍4: 후보 안에서 최대 3곳 추천, 이름·주소·링크·이유를 요청하세요.
    rules = "후보 중 최대 3곳을 추천하고 이름·주소·링크·이유를 한국어로 쓰세요"\
        "제공된 정보로만 설명하고 모르는 특징은 추가 확인 필요라고 쓰세요."
    # 📍5: places를 한글이 유지되는 JSON 문자열로 바꾸세요.
    candidates = json.dumps(places,ensure_ascii=False)
    return (
        rules
        + "\n사용자 조건: " + user_request
        + "\n후보 데이터: " + candidates
    )


def generate_with_retry(prompt):
    # 재시도 처리는 제공된 코드를 사용합니다.
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise ValueError(".env의 GEMINI_API_KEY를 확인하세요.")
    model = os.getenv("GEMINI_MODEL", "").strip()
    if not model:
        raise ValueError(".env의 GEMINI_MODEL에 사전 확인한 모델을 입력하세요.")
    with genai.Client(api_key=key) as client:
        for attempt in range(3):
            try:
                return client.models.generate_content(
                    model=model,
                    # 📍6: 완성한 프롬프트를 전달하세요.
                    contents=prompt,
                )
            except errors.ServerError as error:
                if error.code != 503 or attempt == 2:
                    raise
                seconds = 5 * (2 ** attempt)
                print(f"서버 혼잡: {seconds}초 후 재시도합니다.")
                time.sleep(seconds)


def main():
    # 덜 채운 코드로 API를 호출하지 않도록 확인합니다.
    source = Path(__file__).read_text(encoding="utf-8")
    missing = re.findall(r'"📍([1-6])"', source)
    if any(number in missing for number in ("1", "2", "3")):
        print("아직 남은 빈칸:", ", ".join(missing))
        print('📍 표시 문자열 전체를 PPT 답안으로 바꾸세요. 따옴표도 포함합니다.')
        return
    query = input("검색어 (기본: 성수역 카페): ").strip() or "성수역 카페"
    user_request = input("추천 조건 (예: 혼자 방문할 곳): ").strip()
    try:
        places = search_places(query)
        print("\n카카오 검색 후보:")
        for place in places:
            print(place["name"], place["address"], place["url"], sep="\n")
        if not places:
            print("검색 결과가 없습니다. 검색어를 바꾸세요.")
            return
        # 빈칸 1~3을 채운 뒤에는 여기까지 확인할 수 있습니다.
        if input("Gemini 추천도 실행할까요? [y/N]: ").strip().lower() != "y":
            return
        if missing:
            print("추천 전 빈칸 4~6을 채워주세요.")
            print("남은 빈칸:", ", ".join(missing))
            return
        prompt = build_prompt(user_request, places)
        result = generate_with_retry(prompt)
        print("\nGemini 추천:\n", result.text or "텍스트 응답이 없습니다.")
    except requests.RequestException:
        print("카카오 요청 실패: REST 키, 사용 설정, 네트워크를 확인하세요.")
    except errors.APIError as error:
        print("Gemini 오류 코드:", error.code)
        print("503: 잠시 후 재실행 / 429: 사용량 확인 / 404: 모델 설정 확인")
    except (ValueError, TypeError, KeyError) as error:
        print("설정 또는 빈칸의 답을 확인하세요:", error)


if __name__ == "__main__":
    main()
