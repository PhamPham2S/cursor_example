# Global Base Rate

세계 각국의 기준금리를 한눈에 확인할 수 있는 웹 애플리케이션입니다.

## 기능

- 🌍 20개 국가의 최신 기준금리 정보 표시
- 🔍 국가명으로 검색 기능
- 📊 평균/최고/최저 기준금리 통계
- 📱 반응형 디자인
- 🔄 최신 데이터 자동 업데이트

## 데이터 출처

각 국가의 기준금리는 해당 중앙은행의 공식 발표를 기준으로 합니다:

- **미국**: 연방준비제도(Federal Reserve)
- **한국**: 한국은행(Bank of Korea)
- **일본**: 일본은행(Bank of Japan)
- **유로존**: 유럽중앙은행(European Central Bank)
- **영국**: 영국은행(Bank of England)
- 기타 국가: 각국 중앙은행 공식 발표

## 사용 방법

### 1. 웹 애플리케이션 실행

브라우저에서 `index.html` 파일을 열면 됩니다.

### 2. 최신 데이터 업데이트

#### 기본 모드 (수동 데이터)
```bash
# Python 패키지 설치 (최초 1회)
pip install -r requirements.txt

# 최신 데이터 수집 및 업데이트
python3 fetch_rates.py
```

#### 고급 모드 (API 자동 수집) ⭐ 권장
```bash
# 추가 라이브러리 설치
pip install -r requirements.txt

# API 키 설정 (선택사항)
# .env 파일을 생성하고 API 키를 입력하세요
# FRED_API_KEY=your_key (미국 데이터)
# BOK_API_KEY=your_key (한국 데이터)

# API를 통한 자동 데이터 수집
python3 fetch_rates_advanced.py
```

**API 키 발급:**
- **FRED API** (미국): https://fred.stlouisfed.org/docs/api/api_key.html (무료)
- **한국은행 ECOS API**: https://ecos.bok.or.kr/api/ (무료 회원가입)

> 📖 **자세한 전략은 `STRATEGY.md` 파일을 참고하세요.**

## 파일 구조

- `index.html` - 메인 HTML 파일
- `styles.css` - 스타일시트
- `app.js` - 애플리케이션 로직
- `data.js` - 기준금리 데이터 (자동 생성)
- `fetch_rates.py` - 기본 데이터 수집 스크립트
- `fetch_rates_advanced.py` - 고급 API 기반 데이터 수집 스크립트 ⭐
- `STRATEGY.md` - 최신 데이터 수집 전략 가이드
- `requirements.txt` - Python 의존성
- `.env.example` - API 키 설정 예시 파일

## 최신 데이터 수집 전략

### 🎯 권장 접근 방법

1. **공식 API 활용** (가장 권장)
   - 미국: FRED API (무료 API 키 필요)
   - 한국: 한국은행 ECOS API (무료 회원가입)
   - 유로존: ECB API (공개 API)
   - 일본: BOJ CSV 다운로드

2. **하이브리드 접근**
   - API가 있는 국가는 API 사용
   - API가 없는 국가는 웹 스크래핑 또는 수동 업데이트
   - 정기적 자동 실행 (cron job)

3. **자동화 설정**
   ```bash
   # 매일 오전 9시에 자동 실행 (Linux/Mac)
   0 9 * * * cd /path/to/project && python3 fetch_rates_advanced.py
   ```

자세한 내용은 `STRATEGY.md` 파일을 참고하세요.

## 참고사항

- 기준금리는 정기적으로 변경될 수 있으므로, 주기적으로 스크립트를 실행하여 최신 데이터로 업데이트하는 것을 권장합니다.
- API 키를 설정하면 더 정확하고 최신의 데이터를 자동으로 수집할 수 있습니다.
- 일부 국가의 데이터는 수동으로 업데이트가 필요할 수 있습니다. 각 중앙은행의 공식 웹사이트를 확인하세요.