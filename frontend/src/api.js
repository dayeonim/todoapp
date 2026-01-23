// OpenAlex API 연동
const OPENALEX_API = 'https://api.openalex.org';

/**
 * OpenAlex API로 저널 검색
 * @param {string} query - 검색어 (저널 이름 또는 ISSN)
 * @returns {Promise<Array>} 검색 결과
 */
export async function searchJournalsAPI(query) {
  if (!query || query.trim().length < 2) {
    return [];
  }

  try {
    // ISSN 형식인지 확인
    const isISSN = /^\d{4}-?\d{3}[\dxX]$/.test(query.replace(/\s/g, ''));
    
    let url;
    if (isISSN) {
      // ISSN으로 검색
      const cleanISSN = query.replace(/\s/g, '');
      url = `${OPENALEX_API}/sources?filter=issn:${cleanISSN}`;
    } else {
      // 저널 이름으로 검색
      url = `${OPENALEX_API}/sources?search=${encodeURIComponent(query)}&per-page=20`;
    }

    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error('API 요청 실패');
    }

    const data = await response.json();
    
    // OpenAlex 데이터를 우리 형식으로 변환
    return data.results.map(source => ({
      name: source.display_name,
      issn: source.issn_l || source.issn?.[0] || 'N/A',
      impact_factor: calculateImpactFactor(source),
      category: source.type || 'Journal',
      quartile: getQuartile(source),
      h_index: source.summary_stats?.h_index || 0,
      citations: source.summary_stats?.['2yr_mean_citedness'] || 0,
      works_count: source.works_count || 0,
      cited_by_count: source.cited_by_count || 0,
      homepage_url: source.homepage_url,
      is_oa: source.is_oa,
      country_code: source.country_code
    })).filter(journal => journal.name && journal.name !== '');
    
  } catch (error) {
    console.error('API 검색 오류:', error);
    throw error;
  }
}

/**
 * Impact Factor 대체 지표 계산
 * OpenAlex의 2년 평균 인용도를 사용
 */
function calculateImpactFactor(source) {
  const citedness = source.summary_stats?.['2yr_mean_citedness'];
  if (citedness && citedness > 0) {
    return parseFloat(citedness.toFixed(3));
  }
  
  // h-index 기반 추정
  const hIndex = source.summary_stats?.h_index;
  if (hIndex && hIndex > 0) {
    return parseFloat((hIndex / 10).toFixed(3));
  }
  
  return 0;
}

/**
 * Quartile 추정
 */
function getQuartile(source) {
  const citedness = source.summary_stats?.['2yr_mean_citedness'] || 0;
  const hIndex = source.summary_stats?.h_index || 0;
  
  // 간단한 quartile 추정 로직
  if (citedness >= 10 || hIndex >= 100) return 'Q1';
  if (citedness >= 5 || hIndex >= 50) return 'Q2';
  if (citedness >= 2 || hIndex >= 25) return 'Q3';
  return 'Q4';
}

/**
 * 저널 상세 정보 가져오기
 */
export async function getJournalDetails(openalex_id) {
  try {
    const response = await fetch(`${OPENALEX_API}/sources/${openalex_id}`);
    
    if (!response.ok) {
      throw new Error('저널 정보를 가져올 수 없습니다');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('저널 상세 정보 오류:', error);
    throw error;
  }
}

/**
 * 인기 저널 목록 가져오기
 */
export async function getTopJournals(limit = 20) {
  try {
    const url = `${OPENALEX_API}/sources?sort=cited_by_count:desc&per-page=${limit}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error('인기 저널 목록을 가져올 수 없습니다');
    }

    const data = await response.json();
    
    return data.results.map(source => ({
      name: source.display_name,
      issn: source.issn_l || source.issn?.[0] || 'N/A',
      impact_factor: calculateImpactFactor(source),
      category: source.type || 'Journal',
      quartile: getQuartile(source),
      h_index: source.summary_stats?.h_index || 0,
      citations: source.summary_stats?.['2yr_mean_citedness'] || 0,
      works_count: source.works_count || 0
    }));
  } catch (error) {
    console.error('인기 저널 목록 오류:', error);
    throw error;
  }
}
