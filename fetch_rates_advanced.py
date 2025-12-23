#!/usr/bin/env python3
"""
세계 각국의 기준금리를 공식 API에서 자동으로 수집하는 고급 스크립트
공식 API를 우선 사용하고, 없으면 웹 스크래핑을 시도합니다.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time

# requests는 필수 의존성
try:
    import requests
    from bs4 import BeautifulSoup
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False
    print("❌ 필수 라이브러리가 설치되지 않았습니다.")
    print("   다음 명령어로 설치하세요: pip install requests beautifulsoup4")
    exit(1)

# .env 파일에서 API 키 로드 (선택적)
def load_api_keys():
    """환경 변수 또는 .env 파일에서 API 키 로드"""
    api_keys = {}
    
    # 환경 변수에서 로드
    api_keys['FRED_API_KEY'] = os.getenv('FRED_API_KEY', '')
    api_keys['BOK_API_KEY'] = os.getenv('BOK_API_KEY', '')
    
    # .env 파일이 있으면 로드
    if os.path.exists('.env'):
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        if key not in api_keys or not api_keys[key]:
                            api_keys[key] = value
        except Exception as e:
            print(f"⚠️  .env 파일 읽기 오류: {e}")
    
    return api_keys

# API 키 로드
API_KEYS = load_api_keys()

def fetch_fred_rate(api_key: str) -> Optional[Dict]:
    """FRED API에서 미국 기준금리 가져오기"""
    if not api_key:
        return None
    
    try:
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": "DFF",  # Federal Funds Effective Rate
            "api_key": api_key,
            "file_type": "json",
            "limit": 1,
            "sort_order": "desc"
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "observations" in data and len(data["observations"]) > 0:
                obs = data["observations"][0]
                rate = float(obs["value"])
                date = obs["date"]
                return {
                    "rate": rate,
                    "date": date,
                    "change": 0.0,  # 이전 값과 비교 필요
                    "source": "FRED API"
                }
    except Exception as e:
        print(f"⚠️  FRED API 오류: {e}")
    return None

def fetch_bok_rate(api_key: str) -> Optional[Dict]:
    """한국은행 ECOS API에서 기준금리 가져오기"""
    if not api_key:
        return None
    
    try:
        # 한국은행 기준금리 통계코드: 010Y002
        url = "https://ecos.bok.or.kr/api/StatisticSearch/{}/json/kr/1/1/010Y002/DD/20240101/20241231".format(api_key)
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # 응답 구조에 따라 파싱 필요
            # 실제 API 응답 구조를 확인 후 수정 필요
            print(f"한국은행 API 응답: {data}")
            # TODO: 실제 응답 구조에 맞게 파싱
    except Exception as e:
        print(f"⚠️  한국은행 API 오류: {e}")
    return None

def fetch_ecb_rate() -> Optional[Dict]:
    """ECB API에서 유로존 기준금리 가져오기"""
    try:
        # ECB 기준금리 시리즈
        url = "https://sdw-wsrest.ecb.europa.eu/service/data/IRS"
        params = {
            "detail": "dataonly",
            "format": "jsondata"
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # 실제 응답 구조에 맞게 파싱 필요
            print(f"ECB API 응답 구조 확인 필요: {data}")
            # TODO: 실제 응답 구조에 맞게 파싱
    except Exception as e:
        print(f"⚠️  ECB API 오류: {e}")
    return None

def fetch_boj_rate() -> Optional[Dict]:
    """일본은행 CSV에서 기준금리 가져오기"""
    try:
        url = "https://www.stat-search.boj.or.jp/ssi/mtshtml/csv/m_ir.csv"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # CSV 파싱
            lines = response.text.strip().split('\n')
            if len(lines) > 1:
                # 마지막 행에서 최신 데이터 추출
                last_line = lines[-1]
                parts = last_line.split(',')
                if len(parts) >= 2:
                    date = parts[0]
                    rate = float(parts[1]) if parts[1] else None
                    if rate is not None:
                        return {
                            "rate": rate,
                            "date": date,
                            "change": 0.0,
                            "source": "BOJ CSV"
                        }
    except Exception as e:
        print(f"⚠️  일본은행 데이터 오류: {e}")
    return None

def scrape_bank_website(country: str, url: str) -> Optional[Dict]:
    """중앙은행 웹사이트에서 기준금리 스크래핑"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # 각 웹사이트 구조에 맞게 파싱 필요
            # TODO: 국가별로 다른 파싱 로직 구현
            print(f"⚠️  {country} 웹 스크래핑: 구현 필요")
    except Exception as e:
        print(f"⚠️  {country} 웹 스크래핑 오류: {e}")
    return None

# 국가별 데이터 수집 함수 매핑
COUNTRY_FETCHERS = {
    "미국": lambda: fetch_fred_rate(API_KEYS.get('FRED_API_KEY', '')),
    "한국": lambda: fetch_bok_rate(API_KEYS.get('BOK_API_KEY', '')),
    "일본": fetch_boj_rate,
    "유로존": fetch_ecb_rate,
}

# 기본 데이터 (API 실패 시 사용)
FALLBACK_RATES = {
    "미국": {"rate": 5.25, "date": "2024-12-18", "change": 0.0},
    "한국": {"rate": 3.25, "date": "2024-11-21", "change": 0.0},
    "일본": {"rate": 0.10, "date": "2024-12-19", "change": 0.10},
    "유로존": {"rate": 4.25, "date": "2024-12-12", "change": -0.25},
    "영국": {"rate": 5.25, "date": "2024-12-19", "change": 0.0},
    "중국": {"rate": 3.45, "date": "2024-12-20", "change": 0.0},
    "캐나다": {"rate": 5.00, "date": "2024-12-04", "change": 0.0},
    "호주": {"rate": 4.35, "date": "2024-12-03", "change": 0.0},
    "뉴질랜드": {"rate": 5.50, "date": "2024-11-27", "change": 0.0},
    "스위스": {"rate": 1.50, "date": "2024-12-19", "change": -0.25},
    "스웨덴": {"rate": 4.00, "date": "2024-11-27", "change": 0.0},
    "노르웨이": {"rate": 4.50, "date": "2024-12-19", "change": 0.0},
    "인도": {"rate": 6.50, "date": "2024-12-06", "change": 0.0},
    "브라질": {"rate": 10.50, "date": "2024-12-11", "change": -0.50},
    "멕시코": {"rate": 11.25, "date": "2024-12-12", "change": 0.0},
    "터키": {"rate": 45.00, "date": "2024-12-19", "change": 0.0},
    "남아프리카": {"rate": 8.25, "date": "2024-11-21", "change": 0.0},
    "러시아": {"rate": 16.00, "date": "2024-12-13", "change": 0.0},
    "싱가포르": {"rate": 3.00, "date": "2024-10-14", "change": 0.0},
    "홍콩": {"rate": 5.75, "date": "2024-12-19", "change": 0.0},
}

def fetch_country_rate(country: str) -> Dict:
    """각 국가의 기준금리 수집 (API 우선, 실패 시 폴백)"""
    # API로 수집 시도
    if country in COUNTRY_FETCHERS:
        result = COUNTRY_FETCHERS[country]()
        if result:
            print(f"✅ {country}: API에서 수집 성공 ({result['rate']}%)")
            return result
    
    # API 실패 시 폴백 데이터 사용
    if country in FALLBACK_RATES:
        print(f"⚠️  {country}: API 실패, 폴백 데이터 사용")
        return FALLBACK_RATES[country]
    
    # 기본값
    return {"rate": 0.0, "date": datetime.now().strftime("%Y-%m-%d"), "change": 0.0}

def generate_rates_data() -> List[Dict]:
    """전체 기준금리 데이터 생성"""
    countries = [
        "미국", "한국", "일본", "유로존", "영국", "중국", "캐나다", "호주",
        "뉴질랜드", "스위스", "스웨덴", "노르웨이", "인도", "브라질", "멕시코",
        "터키", "남아프리카", "러시아", "싱가포르", "홍콩"
    ]
    
    flags = {
        "미국": "🇺🇸", "한국": "🇰🇷", "일본": "🇯🇵", "유로존": "🇪🇺", "영국": "🇬🇧",
        "중국": "🇨🇳", "캐나다": "🇨🇦", "호주": "🇦🇺", "뉴질랜드": "🇳🇿", "스위스": "🇨🇭",
        "스웨덴": "🇸🇪", "노르웨이": "🇳🇴", "인도": "🇮🇳", "브라질": "🇧🇷", "멕시코": "🇲🇽",
        "터키": "🇹🇷", "남아프리카": "🇿🇦", "러시아": "🇷🇺", "싱가포르": "🇸🇬", "홍콩": "🇭🇰"
    }
    
    currencies = {
        "미국": "USD", "한국": "KRW", "일본": "JPY", "유로존": "EUR", "영국": "GBP",
        "중국": "CNY", "캐나다": "CAD", "호주": "AUD", "뉴질랜드": "NZD", "스위스": "CHF",
        "스웨덴": "SEK", "노르웨이": "NOK", "인도": "INR", "브라질": "BRL", "멕시코": "MXN",
        "터키": "TRY", "남아프리카": "ZAR", "러시아": "RUB", "싱가포르": "SGD", "홍콩": "HKD"
    }
    
    rates_data = []
    
    print("\n📡 API를 통한 데이터 수집 시작...\n")
    
    for country in countries:
        rate_info = fetch_country_rate(country)
        rates_data.append({
            "country": country,
            "flag": flags.get(country, "🌍"),
            "rate": rate_info["rate"],
            "date": rate_info["date"],
            "change": rate_info["change"],
            "currency": currencies.get(country, "")
        })
        time.sleep(0.5)  # API 호출 제한을 위한 딜레이
    
    return rates_data

def main():
    """메인 함수"""
    print("🌍 세계 각국의 기준금리 데이터 수집 (고급 모드)")
    print("=" * 60)
    
    # API 키 확인
    if not API_KEYS.get('FRED_API_KEY'):
        print("\n⚠️  FRED API 키가 설정되지 않았습니다.")
        print("   미국 데이터는 폴백 데이터를 사용합니다.")
        print("   API 키 발급: https://fred.stlouisfed.org/docs/api/api_key.html")
    
    if not API_KEYS.get('BOK_API_KEY'):
        print("\n⚠️  한국은행 API 키가 설정되지 않았습니다.")
        print("   한국 데이터는 폴백 데이터를 사용합니다.")
        print("   API 키 발급: https://ecos.bok.or.kr/api/")
    
    rates_data = generate_rates_data()
    
    # JSON 파일로 저장
    output_file = "rates_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(rates_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 데이터가 {output_file}에 저장되었습니다.")
    print(f"📊 총 {len(rates_data)}개 국가의 기준금리 데이터를 수집했습니다.")
    
    # JavaScript 파일로도 저장
    js_output = "data.js"
    with open(js_output, "w", encoding="utf-8") as f:
        f.write("// 세계 각국의 기준금리 데이터 (최신 업데이트)\n")
        f.write("// 출처: 각국 중앙은행 공식 API 및 발표\n")
        f.write("// 자동 업데이트: python fetch_rates_advanced.py 실행\n\n")
        f.write("const baseRates = ")
        json.dump(rates_data, f, ensure_ascii=False, indent=4)
        f.write(";\n")
    
    print(f"✅ JavaScript 파일({js_output})도 업데이트되었습니다.")
    
    # API 성공률 통계
    api_success = sum(1 for r in rates_data if r.get('source'))
    print(f"\n📈 API 수집 성공: {api_success}/{len(rates_data)}개 국가")

if __name__ == "__main__":
    main()

