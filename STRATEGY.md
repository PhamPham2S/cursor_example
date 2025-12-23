# 최신 기준금리 데이터 수집 전략

## 🎯 목표
각국 중앙은행의 공식 발표를 기준으로 최신 기준금리 데이터를 자동으로 수집

## 📊 데이터 수집 전략 (우선순위별)

### 1️⃣ **공식 API 활용** (가장 권장) ⭐⭐⭐

#### 장점
- ✅ 공식 데이터, 신뢰성 높음
- ✅ 자동화 가능
- ✅ 실시간/준실시간 데이터

#### 단점
- ⚠️ API 키 필요 (무료)
- ⚠️ 국가별로 다른 API 구조

#### 구현 가능한 API 목록

**1. FRED API (미국 연방준비제도)**
- URL: https://api.stlouisfed.org
- API 키: https://fred.stlouisfed.org/docs/api/api_key.html (무료)
- Series ID: `DFF` (Federal Funds Effective Rate)
- 제한: 무료, 분당 120회 요청

**2. 한국은행 ECOS API**
- URL: https://ecos.bok.or.kr/api/
- API 키: https://ecos.bok.or.kr/api/ (무료 회원가입)
- 통계코드: `010Y002` (기준금리)
- 제한: 무료, 일일 10,000건

**3. ECB Statistical Data Warehouse (유로존)**
- URL: https://sdw.ecb.europa.eu/
- API: RESTful API 제공
- Series: `IRS.M.GBP.EUR.4F.BB` (기준금리)
- 제한: 무료, 공개 API

**4. Bank of England API (영국)**
- URL: https://www.bankofengland.co.uk/boeapps/database/
- CSV 다운로드 가능
- Series: `IUDBEDR` (기준금리)
- 제한: 무료

**5. Bank of Japan (일본)**
- URL: https://www.stat-search.boj.or.jp/
- CSV 다운로드 가능
- 제한: 무료

### 2️⃣ **웹 스크래핑** (보조 수단) ⭐⭐

#### 장점
- ✅ API가 없는 국가도 수집 가능
- ✅ 추가 설정 불필요

#### 단점
- ⚠️ 웹사이트 구조 변경 시 수정 필요
- ⚠️ 법적/윤리적 고려 필요
- ⚠️ 속도 제한 가능

#### 대상 국가
- 캐나다, 호주, 뉴질랜드, 중국, 인도 등

### 3️⃣ **공공 데이터 포털** ⭐

#### 장점
- ✅ 정부 공식 데이터
- ✅ 무료

#### 단점
- ⚠️ 업데이트 주기가 느릴 수 있음
- ⚠️ 국가별로 다른 포털

#### 예시
- 한국: data.go.kr
- 미국: data.gov

### 4️⃣ **하이브리드 접근** (권장) ⭐⭐⭐

**전략:**
1. API가 있는 국가 → API 활용
2. API가 없는 국가 → 웹 스크래핑 또는 수동 업데이트
3. 정기적 자동 실행 (cron job)

## 🛠️ 구현 계획

### Phase 1: 핵심 국가 API 연동
1. **미국 (FRED API)** - 가장 중요
2. **한국 (ECOS API)** - 국내 사용자 중요
3. **유로존 (ECB API)** - 주요 경제권
4. **일본 (BOJ CSV)** - 주요 경제권

### Phase 2: 확장
5. **영국 (BoE API)**
6. **기타 국가 웹 스크래핑**

### Phase 3: 자동화
- 스케줄러 설정 (매일 자동 실행)
- 오류 알림 시스템
- 데이터 검증 로직

## 📝 API 키 발급 가이드

### FRED API 키 발급
1. https://fred.stlouisfed.org 접속
2. 우측 상단 "My Account" → "Create Account"
3. 로그인 후 "API Keys" 메뉴
4. "Request API Key" 클릭
5. 발급된 키를 `.env` 파일에 저장

### 한국은행 ECOS API 키 발급
1. https://ecos.bok.or.kr 접속
2. 회원가입 (무료)
3. "마이페이지" → "Open API" 메뉴
4. "인증키 신청" 클릭
5. 발급된 키를 `.env` 파일에 저장

## 🔄 자동화 설정

### Linux/Mac (cron)
```bash
# 매일 오전 9시에 실행
0 9 * * * cd /path/to/project && python3 fetch_rates.py
```

### Windows (Task Scheduler)
- 작업 스케줄러에서 Python 스크립트 등록
- 매일 실행 설정

## ⚠️ 주의사항

1. **API 사용 제한**: 각 API의 사용 제한을 확인하고 준수
2. **에러 처리**: 네트워크 오류, API 변경 등에 대비
3. **데이터 검증**: 수집된 데이터의 합리성 검증
4. **법적 준수**: 각 웹사이트의 이용약관 확인

## 📈 예상 효과

- **정확도**: 95% 이상 (공식 API 사용 시)
- **최신성**: 실시간 ~ 1일 지연
- **자동화**: 90% 이상 자동 수집 가능
- **유지보수**: 주 1회 정도 점검

