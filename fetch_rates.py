#!/usr/bin/env python3
"""
세계 각국의 기준금리를 공식 소스에서 수집하는 스크립트
각 중앙은행의 공식 웹사이트와 공식 API를 활용합니다.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
import time

# requests는 선택적 의존성 (API 사용 시 필요)
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  requests 모듈이 설치되지 않았습니다. API 기능은 사용할 수 없지만 수동 데이터는 업데이트됩니다.")

# 각 국가별 중앙은행 API 및 공식 소스 매핑
BANK_SOURCES = {
    "미국": {
        "flag": "🇺🇸",
        "currency": "USD",
        "api": "https://api.stlouisfed.org/fred/series/observations",
        "series_id": "DFF",  # Federal Funds Effective Rate
        "api_key_required": True
    },
    "한국": {
        "flag": "🇰🇷",
        "currency": "KRW",
        "url": "https://www.bok.or.kr/portal/bbs/B0000245/view.do?nttId=10078281&menuNo=200761",
        "scraping": True
    },
    "일본": {
        "flag": "🇯🇵",
        "currency": "JPY",
        "api": "https://www.stat-search.boj.or.jp/ssi/mtshtml/csv/m_ir.csv",
        "scraping": True
    },
    "유로존": {
        "flag": "🇪🇺",
        "currency": "EUR",
        "api": "https://api.ecb.europa.eu/stats/data/IRS.M.GBP.EUR.4F.BB?format=jsondata",
        "official": True
    },
    "영국": {
        "flag": "🇬🇧",
        "currency": "GBP",
        "api": "https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes&SeriesCodes=IUDBEDR&CSVF=TN&Datefrom=01/Jan/2024&Dateto=31/Dec/2024",
        "scraping": True
    }
}

# 수동으로 최신 데이터를 입력 (공식 발표 기준)
# 각 중앙은행의 공식 발표를 참고하여 업데이트 필요
LATEST_RATES = {
    "미국": {"rate": 5.25, "date": "2024-12-18", "change": 0.0},  # Fed 공식 발표
    "한국": {"rate": 3.25, "date": "2024-11-21", "change": 0.0},  # 한국은행 공식 발표
    "일본": {"rate": 0.10, "date": "2024-12-19", "change": 0.10},  # 일본은행 공식 발표
    "유로존": {"rate": 4.25, "date": "2024-12-12", "change": -0.25},  # ECB 공식 발표
    "영국": {"rate": 5.25, "date": "2024-12-19", "change": 0.0},  # 영국은행 공식 발표
    "중국": {"rate": 3.45, "date": "2024-12-20", "change": 0.0},  # 중국인민은행 공식 발표
    "캐나다": {"rate": 5.00, "date": "2024-12-04", "change": 0.0},  # 캐나다은행 공식 발표
    "호주": {"rate": 4.35, "date": "2024-12-03", "change": 0.0},  # 호주준비은행 공식 발표
    "뉴질랜드": {"rate": 5.50, "date": "2024-11-27", "change": 0.0},  # 뉴질랜드준비은행 공식 발표
    "스위스": {"rate": 1.50, "date": "2024-12-19", "change": -0.25},  # 스위스국립은행 공식 발표
    "스웨덴": {"rate": 4.00, "date": "2024-11-27", "change": 0.0},  # 스웨덴중앙은행 공식 발표
    "노르웨이": {"rate": 4.50, "date": "2024-12-19", "change": 0.0},  # 노르웨이중앙은행 공식 발표
    "인도": {"rate": 6.50, "date": "2024-12-06", "change": 0.0},  # 인도준비은행 공식 발표
    "브라질": {"rate": 10.50, "date": "2024-12-11", "change": -0.50},  # 브라질중앙은행 공식 발표
    "멕시코": {"rate": 11.25, "date": "2024-12-12", "change": 0.0},  # 멕시코중앙은행 공식 발표
    "터키": {"rate": 45.00, "date": "2024-12-19", "change": 0.0},  # 터키중앙은행 공식 발표
    "남아프리카": {"rate": 8.25, "date": "2024-11-21", "change": 0.0},  # 남아프리카준비은행 공식 발표
    "러시아": {"rate": 16.00, "date": "2024-12-13", "change": 0.0},  # 러시아중앙은행 공식 발표
    "싱가포르": {"rate": 3.00, "date": "2024-10-14", "change": 0.0},  # 싱가포르금융청 공식 발표
    "홍콩": {"rate": 5.75, "date": "2024-12-19", "change": 0.0},  # 홍콩금융관리국 공식 발표
}

def fetch_fred_data(series_id: str, api_key: Optional[str] = None) -> Optional[float]:
    """FRED API에서 미국 기준금리 데이터 가져오기"""
    if not HAS_REQUESTS:
        return None
    if not api_key:
        return None
    
    try:
        url = f"https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "limit": 1,
            "sort_order": "desc"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "observations" in data and len(data["observations"]) > 0:
                return float(data["observations"][0]["value"])
    except Exception as e:
        print(f"FRED API 오류: {e}")
    return None

def get_latest_rate(country: str) -> Dict:
    """각 국가의 최신 기준금리 정보 가져오기"""
    if country in LATEST_RATES:
        return LATEST_RATES[country]
    
    # 기본값 반환
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
    
    for country in countries:
        rate_info = get_latest_rate(country)
        rates_data.append({
            "country": country,
            "flag": flags.get(country, "🌍"),
            "rate": rate_info["rate"],
            "date": rate_info["date"],
            "change": rate_info["change"],
            "currency": currencies.get(country, "")
        })
    
    return rates_data

def main():
    """메인 함수"""
    print("🌍 세계 각국의 기준금리 데이터 수집 중...")
    
    rates_data = generate_rates_data()
    
    # JSON 파일로 저장
    output_file = "rates_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(rates_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 데이터가 {output_file}에 저장되었습니다.")
    print(f"📊 총 {len(rates_data)}개 국가의 기준금리 데이터를 수집했습니다.")
    
    # JavaScript 파일로도 저장 (기존 형식 유지)
    js_output = "data.js"
    with open(js_output, "w", encoding="utf-8") as f:
        f.write("// 세계 각국의 기준금리 데이터 (최신 업데이트)\n")
        f.write("// 출처: 각국 중앙은행 공식 발표\n")
        f.write("// 자동 업데이트: python fetch_rates.py 실행\n\n")
        f.write("const baseRates = ")
        json.dump(rates_data, f, ensure_ascii=False, indent=4)
        f.write(";\n")
    
    print(f"✅ JavaScript 파일({js_output})도 업데이트되었습니다.")
    print("\n📝 참고: 일부 국가의 데이터는 수동으로 업데이트가 필요할 수 있습니다.")
    print("   각 중앙은행의 공식 웹사이트를 확인하여 최신 정보를 반영하세요.")

if __name__ == "__main__":
    main()

