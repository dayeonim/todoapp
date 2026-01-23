from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from typing import List, Dict, Optional

app = Flask(__name__)
CORS(app)

# 주요 저널의 샘플 Impact Factor 데이터 (2023-2024 기준)
JOURNAL_DATABASE = [
    # Medicine & Health Sciences
    {"name": "New England Journal of Medicine", "issn": "0028-4793", "impact_factor": 176.079, "category": "Medicine, General & Internal", "quartile": "Q1"},
    {"name": "The Lancet", "issn": "0140-6736", "impact_factor": 168.9, "category": "Medicine, General & Internal", "quartile": "Q1"},
    {"name": "JAMA", "issn": "0098-7484", "impact_factor": 120.8, "category": "Medicine, General & Internal", "quartile": "Q1"},
    {"name": "Nature Medicine", "issn": "1078-8956", "impact_factor": 82.9, "category": "Biochemistry & Molecular Biology", "quartile": "Q1"},
    {"name": "BMJ", "issn": "0959-8138", "impact_factor": 93.6, "category": "Medicine, General & Internal", "quartile": "Q1"},
    
    # Science & Nature
    {"name": "Nature", "issn": "0028-0836", "impact_factor": 64.8, "category": "Multidisciplinary Sciences", "quartile": "Q1"},
    {"name": "Science", "issn": "0036-8075", "impact_factor": 56.9, "category": "Multidisciplinary Sciences", "quartile": "Q1"},
    {"name": "Cell", "issn": "0092-8674", "impact_factor": 64.5, "category": "Cell Biology", "quartile": "Q1"},
    {"name": "Proceedings of the National Academy of Sciences", "issn": "0027-8424", "impact_factor": 11.1, "category": "Multidisciplinary Sciences", "quartile": "Q1"},
    
    # Chemistry
    {"name": "Chemical Reviews", "issn": "0009-2665", "impact_factor": 62.1, "category": "Chemistry, Multidisciplinary", "quartile": "Q1"},
    {"name": "Nature Chemistry", "issn": "1755-4330", "impact_factor": 24.2, "category": "Chemistry, Multidisciplinary", "quartile": "Q1"},
    {"name": "Journal of the American Chemical Society", "issn": "0002-7863", "impact_factor": 16.4, "category": "Chemistry, Multidisciplinary", "quartile": "Q1"},
    {"name": "Angewandte Chemie International Edition", "issn": "1433-7851", "impact_factor": 16.6, "category": "Chemistry, Multidisciplinary", "quartile": "Q1"},
    
    # Physics
    {"name": "Reviews of Modern Physics", "issn": "0034-6861", "impact_factor": 42.9, "category": "Physics, Multidisciplinary", "quartile": "Q1"},
    {"name": "Nature Physics", "issn": "1745-2473", "impact_factor": 19.6, "category": "Physics, Multidisciplinary", "quartile": "Q1"},
    {"name": "Physical Review Letters", "issn": "0031-9007", "impact_factor": 8.6, "category": "Physics, Multidisciplinary", "quartile": "Q1"},
    
    # Computer Science
    {"name": "Nature Machine Intelligence", "issn": "2522-5839", "impact_factor": 25.9, "category": "Computer Science, Artificial Intelligence", "quartile": "Q1"},
    {"name": "IEEE Transactions on Pattern Analysis and Machine Intelligence", "issn": "0162-8828", "impact_factor": 23.6, "category": "Computer Science, Artificial Intelligence", "quartile": "Q1"},
    {"name": "ACM Computing Surveys", "issn": "0360-0300", "impact_factor": 23.8, "category": "Computer Science, Theory & Methods", "quartile": "Q1"},
    
    # Engineering
    {"name": "Nature Energy", "issn": "2058-7546", "impact_factor": 56.0, "category": "Energy & Fuels", "quartile": "Q1"},
    {"name": "Advanced Materials", "issn": "0935-9648", "impact_factor": 29.4, "category": "Materials Science, Multidisciplinary", "quartile": "Q1"},
    
    # Biology
    {"name": "Nature Genetics", "issn": "1061-4036", "impact_factor": 30.8, "category": "Genetics & Heredity", "quartile": "Q1"},
    {"name": "Nature Biotechnology", "issn": "1087-0156", "impact_factor": 46.9, "category": "Biotechnology & Applied Microbiology", "quartile": "Q1"},
    {"name": "Genome Biology", "issn": "1474-760X", "impact_factor": 12.3, "category": "Genetics & Heredity", "quartile": "Q1"},
    
    # Economics & Business
    {"name": "Journal of Economic Literature", "issn": "0022-0515", "impact_factor": 12.4, "category": "Economics", "quartile": "Q1"},
    {"name": "Quarterly Journal of Economics", "issn": "0033-5533", "impact_factor": 11.8, "category": "Economics", "quartile": "Q1"},
    {"name": "Academy of Management Journal", "issn": "0001-4273", "impact_factor": 9.5, "category": "Business", "quartile": "Q1"},
    
    # Psychology
    {"name": "Psychological Bulletin", "issn": "0033-2909", "impact_factor": 17.9, "category": "Psychology, Multidisciplinary", "quartile": "Q1"},
    {"name": "Annual Review of Psychology", "issn": "0066-4308", "impact_factor": 23.6, "category": "Psychology, Multidisciplinary", "quartile": "Q1"},
    
    # Environmental Science
    {"name": "Nature Climate Change", "issn": "1758-678X", "impact_factor": 30.7, "category": "Environmental Sciences", "quartile": "Q1"},
    {"name": "Environmental Science & Technology", "issn": "0013-936X", "impact_factor": 11.4, "category": "Engineering, Environmental", "quartile": "Q1"},
    
    # Korean Journals
    {"name": "Journal of Korean Medical Science", "issn": "1011-8934", "impact_factor": 3.5, "category": "Medicine, General & Internal", "quartile": "Q2"},
    {"name": "Cancer Research and Treatment", "issn": "1598-2998", "impact_factor": 4.9, "category": "Oncology", "quartile": "Q2"},
]


def normalize_string(s: str) -> str:
    """문자열을 검색용으로 정규화"""
    return s.lower().strip().replace('-', '').replace(' ', '')


def search_journals(query: str) -> List[Dict]:
    """저널 이름 또는 ISSN으로 검색"""
    if not query:
        return []
    
    normalized_query = normalize_string(query)
    results = []
    
    for journal in JOURNAL_DATABASE:
        # 저널 이름으로 검색
        if normalized_query in normalize_string(journal['name']):
            results.append(journal)
        # ISSN으로 검색
        elif normalized_query in normalize_string(journal['issn']):
            results.append(journal)
    
    # Impact Factor 기준 내림차순 정렬
    results.sort(key=lambda x: x['impact_factor'], reverse=True)
    return results


@app.route('/')
def home():
    """API 정보"""
    return jsonify({
        'message': 'Journal Impact Factor API',
        'version': '1.0.0',
        'endpoints': {
            '/api/search': 'Search journals by name or ISSN',
            '/api/journals': 'Get all journals',
            '/api/stats': 'Get database statistics'
        }
    })


@app.route('/api/search', methods=['GET'])
def search():
    """저널 검색 API"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'error': 'Search query is required',
            'message': 'Please provide a search query using ?q=parameter'
        }), 400
    
    results = search_journals(query)
    
    return jsonify({
        'query': query,
        'count': len(results),
        'results': results
    })


@app.route('/api/journals', methods=['GET'])
def get_all_journals():
    """전체 저널 목록 조회"""
    # 카테고리 필터
    category = request.args.get('category', '').strip()
    
    if category:
        filtered = [j for j in JOURNAL_DATABASE if category.lower() in j['category'].lower()]
        journals = sorted(filtered, key=lambda x: x['impact_factor'], reverse=True)
    else:
        journals = sorted(JOURNAL_DATABASE, key=lambda x: x['impact_factor'], reverse=True)
    
    return jsonify({
        'count': len(journals),
        'journals': journals
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """데이터베이스 통계"""
    categories = {}
    for journal in JOURNAL_DATABASE:
        cat = journal['category']
        if cat not in categories:
            categories[cat] = {
                'count': 0,
                'avg_impact_factor': 0,
                'journals': []
            }
        categories[cat]['count'] += 1
        categories[cat]['journals'].append(journal['name'])
    
    # 평균 Impact Factor 계산
    for cat in categories:
        cat_journals = [j for j in JOURNAL_DATABASE if j['category'] == cat]
        avg_if = sum(j['impact_factor'] for j in cat_journals) / len(cat_journals)
        categories[cat]['avg_impact_factor'] = round(avg_if, 2)
    
    impact_factors = [j['impact_factor'] for j in JOURNAL_DATABASE]
    
    return jsonify({
        'total_journals': len(JOURNAL_DATABASE),
        'categories': len(categories),
        'category_breakdown': categories,
        'impact_factor_stats': {
            'min': min(impact_factors),
            'max': max(impact_factors),
            'avg': round(sum(impact_factors) / len(impact_factors), 2)
        }
    })


@app.route('/api/journal/<path:issn>', methods=['GET'])
def get_journal_by_issn(issn: str):
    """ISSN으로 특정 저널 조회"""
    normalized_issn = normalize_string(issn)
    
    for journal in JOURNAL_DATABASE:
        if normalize_string(journal['issn']) == normalized_issn:
            return jsonify(journal)
    
    return jsonify({
        'error': 'Journal not found',
        'message': f'No journal found with ISSN: {issn}'
    }), 404


if __name__ == '__main__':
    print("=" * 60)
    print("🔬 Journal Impact Factor API Server")
    print("=" * 60)
    print(f"📊 Total journals in database: {len(JOURNAL_DATABASE)}")
    print(f"🌐 Server running on: http://localhost:5001")
    print(f"🔍 Search endpoint: http://localhost:5001/api/search?q=nature")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5001)
