import React, { useState, useEffect } from 'react';
import './App.css';
import { searchJournals, getStats } from './journalData';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  // 통계 데이터 로드
  useEffect(() => {
    const statsData = getStats();
    setStats(statsData);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    
    if (!searchQuery.trim()) {
      setError('검색어를 입력해주세요');
      return;
    }

    setLoading(true);
    setError(null);
    setHasSearched(true);

    // 약간의 지연을 추가해서 로딩 효과
    setTimeout(() => {
      const results = searchJournals(searchQuery);
      setSearchResults(results);
      
      if (results.length === 0) {
        setError('검색 결과가 없습니다. 다른 키워드로 시도해보세요.');
      }
      
      setLoading(false);
    }, 300);
  };

  const getIFColor = (impactFactor) => {
    if (impactFactor >= 50) return '#ff4757';
    if (impactFactor >= 20) return '#ff6348';
    if (impactFactor >= 10) return '#ffa502';
    if (impactFactor >= 5) return '#2ed573';
    return '#1e90ff';
  };

  const getQuartileColor = (quartile) => {
    const colors = {
      'Q1': '#ff4757',
      'Q2': '#ffa502',
      'Q3': '#2ed573',
      'Q4': '#1e90ff'
    };
    return colors[quartile] || '#999';
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1 className="title">🔬 Journal Impact Factor 조회</h1>
          <p className="subtitle">논문 저널의 Impact Factor를 실시간으로 검색하세요</p>
        </header>

        {stats && (
          <div className="stats-bar">
            <div className="stat-item">
              <span className="stat-label">전체 저널</span>
              <span className="stat-value">{stats.total_journals}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">카테고리</span>
              <span className="stat-value">{stats.categories}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">평균 IF</span>
              <span className="stat-value">{stats.impact_factor_stats.avg}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">최고 IF</span>
              <span className="stat-value">{stats.impact_factor_stats.max}</span>
            </div>
          </div>
        )}

        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-wrapper">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="저널 이름 또는 ISSN을 입력하세요 (예: Nature, 0028-0836)"
              className="search-input"
            />
            <button type="submit" className="search-button" disabled={loading}>
              {loading ? '검색 중...' : '🔍 검색'}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message">
            <span>⚠️ {error}</span>
          </div>
        )}

        {hasSearched && !loading && searchResults.length > 0 && (
          <div className="results-header">
            <h2>검색 결과: {searchResults.length}개</h2>
          </div>
        )}

        <div className="results-grid">
          {searchResults.map((journal, index) => (
            <div key={index} className="journal-card">
              <div className="journal-header">
                <h3 className="journal-name">{journal.name}</h3>
                <span 
                  className="quartile-badge"
                  style={{ backgroundColor: getQuartileColor(journal.quartile) }}
                >
                  {journal.quartile}
                </span>
              </div>
              
              <div className="journal-issn">
                ISSN: {journal.issn}
              </div>
              
              <div className="journal-category">
                📚 {journal.category}
              </div>
              
              <div className="impact-factor-section">
                <div className="if-label">Impact Factor</div>
                <div 
                  className="if-value"
                  style={{ color: getIFColor(journal.impact_factor) }}
                >
                  {journal.impact_factor.toFixed(3)}
                </div>
              </div>
              
              <div className="if-bar-container">
                <div 
                  className="if-bar"
                  style={{ 
                    width: `${Math.min(journal.impact_factor / 2, 100)}%`,
                    backgroundColor: getIFColor(journal.impact_factor)
                  }}
                />
              </div>
            </div>
          ))}
        </div>

        {!hasSearched && (
          <div className="welcome-section">
            <div className="info-card">
              <h3>💡 사용 방법</h3>
              <ul>
                <li>저널 이름으로 검색: "Nature", "Science", "Cell" 등</li>
                <li>ISSN으로 검색: "0028-0836" (Nature의 ISSN)</li>
                <li>부분 검색 가능: "Journal of" 입력 시 관련 모든 저널 표시</li>
              </ul>
            </div>
            
            <div className="info-card">
              <h3>📊 Impact Factor란?</h3>
              <p>
                Impact Factor(IF)는 학술지의 영향력을 나타내는 지표입니다. 
                최근 2년간 발표된 논문이 해당 연도에 인용된 평균 횟수를 의미합니다.
              </p>
              <div className="if-guide">
                <div className="if-guide-item">
                  <span className="if-dot" style={{ backgroundColor: '#ff4757' }}></span>
                  <span>IF ≥ 50: 최상위 저널</span>
                </div>
                <div className="if-guide-item">
                  <span className="if-dot" style={{ backgroundColor: '#ff6348' }}></span>
                  <span>IF ≥ 20: 최고 수준</span>
                </div>
                <div className="if-guide-item">
                  <span className="if-dot" style={{ backgroundColor: '#ffa502' }}></span>
                  <span>IF ≥ 10: 우수</span>
                </div>
                <div className="if-guide-item">
                  <span className="if-dot" style={{ backgroundColor: '#2ed573' }}></span>
                  <span>IF ≥ 5: 양호</span>
                </div>
                <div className="if-guide-item">
                  <span className="if-dot" style={{ backgroundColor: '#1e90ff' }}></span>
                  <span>IF &lt; 5: 보통</span>
                </div>
              </div>
            </div>
          </div>
        )}

        <footer className="footer">
          <p>데이터 기준: 2023-2024 | 총 {stats?.total_journals || 0}개 저널 등록</p>
          <p className="footer-note">
            💡 샘플 데이터로 제공되며, 실제 Impact Factor는 
            <a href="https://jcr.clarivate.com" target="_blank" rel="noopener noreferrer"> Clarivate JCR</a>에서 확인하세요
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
