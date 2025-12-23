// DOM 요소 가져오기
const ratesGrid = document.getElementById('ratesGrid');
const searchInput = document.getElementById('searchInput');
const avgRateEl = document.getElementById('avgRate');
const maxRateEl = document.getElementById('maxRate');
const minRateEl = document.getElementById('minRate');

// 기준금리 카드 생성
function createRateCard(country) {
    const card = document.createElement('div');
    card.className = 'rate-card';
    
    const changeClass = country.change > 0 ? 'positive' : 
                       country.change < 0 ? 'negative' : 'neutral';
    const changeText = country.change > 0 ? `+${country.change}%` : 
                      country.change < 0 ? `${country.change}%` : '변동없음';
    
    card.innerHTML = `
        <div class="rate-card-header">
            <span class="country-name">${country.country}</span>
            <span class="country-flag">${country.flag}</span>
        </div>
        <div class="rate-value">${country.rate.toFixed(2)}%</div>
        <div class="rate-label">기준금리</div>
        <div class="rate-date">업데이트: ${country.date}</div>
        <div class="rate-change ${changeClass}">${changeText}</div>
    `;
    
    return card;
}

// 통계 계산
function calculateStats(rates) {
    const validRates = rates.filter(r => r.rate > -1); // 음수 금리 제외 (일본 등)
    const ratesOnly = validRates.map(r => r.rate);
    
    if (ratesOnly.length === 0) return { avg: 0, max: 0, min: 0 };
    
    const avg = ratesOnly.reduce((a, b) => a + b, 0) / ratesOnly.length;
    const max = Math.max(...ratesOnly);
    const min = Math.min(...ratesOnly);
    
    return { avg, max, min };
}

// 통계 업데이트
function updateStats(rates) {
    const stats = calculateStats(rates);
    avgRateEl.textContent = `${stats.avg.toFixed(2)}%`;
    maxRateEl.textContent = `${stats.max.toFixed(2)}%`;
    minRateEl.textContent = `${stats.min.toFixed(2)}%`;
}

// 기준금리 목록 렌더링
function renderRates(rates) {
    ratesGrid.innerHTML = '';
    rates.forEach(country => {
        const card = createRateCard(country);
        ratesGrid.appendChild(card);
    });
    updateStats(rates);
}

// 검색 기능
function filterRates(searchTerm) {
    const filtered = baseRates.filter(country => 
        country.country.toLowerCase().includes(searchTerm.toLowerCase()) ||
        country.flag.includes(searchTerm)
    );
    renderRates(filtered);
}

// 검색 입력 이벤트 리스너
searchInput.addEventListener('input', (e) => {
    filterRates(e.target.value);
});

// 초기 렌더링
renderRates(baseRates);

