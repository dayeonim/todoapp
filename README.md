# 🔬 Journal Impact Factor 조회 시스템

논문 저널의 Impact Factor를 검색하고 조회할 수 있는 웹 애플리케이션입니다.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![React](https://img.shields.io/badge/react-18.2-blue)
![Flask](https://img.shields.io/badge/flask-3.0-red)

## ✨ 주요 기능

- 📚 **저널 이름 검색**: 저널 이름으로 Impact Factor 조회
- 🔢 **ISSN 검색**: ISSN 번호로 정확한 저널 찾기
- 📊 **시각화**: Impact Factor를 직관적인 차트로 표시
- 🎯 **Quartile 표시**: Q1-Q4 등급 표시
- 📈 **통계 대시보드**: 전체 데이터베이스 통계
- 🎨 **모던 UI**: 반응형 디자인과 아름다운 인터페이스

## 📋 시스템 요구사항

- **Python**: 3.8 이상
- **Node.js**: 16.0 이상
- **npm**: 8.0 이상

## 🚀 빠른 시작

### 1. 설치

```bash
# 프로젝트 클론 또는 다운로드 후
./setup.sh
```

### 2. 실행

```bash
./run.sh
```

### 3. 접속

브라우저에서 http://localhost:3000 으로 접속하세요!

## 📖 상세 사용법

### 검색 방법

1. **저널 이름으로 검색**
   ```
   Nature
   Science
   Cell
   Journal of the American Chemical Society
   ```

2. **ISSN으로 검색**
   ```
   0028-0836 (Nature)
   0036-8075 (Science)
   ```

3. **부분 검색**
   ```
   "nature" 입력 → Nature, Nature Medicine, Nature Physics 등 표시
   ```

### API 엔드포인트

Backend API는 다음 엔드포인트를 제공합니다:

- `GET /api/search?q={query}` - 저널 검색
- `GET /api/journals` - 전체 저널 목록
- `GET /api/stats` - 데이터베이스 통계
- `GET /api/journal/{issn}` - 특정 저널 조회

## 📊 데이터베이스

현재 **30개 이상**의 주요 학술지 데이터를 포함하고 있습니다:

### 포함된 분야
- 의학 및 보건과학 (Medicine & Health Sciences)
- 자연과학 (Nature & Science)
- 화학 (Chemistry)
- 물리학 (Physics)
- 컴퓨터 과학 (Computer Science)
- 공학 (Engineering)
- 생물학 (Biology)
- 경제 및 경영 (Economics & Business)
- 심리학 (Psychology)
- 환경과학 (Environmental Science)

### Impact Factor 등급

- **IF ≥ 50**: 🔴 최상위 저널
- **IF ≥ 20**: 🟠 최고 수준
- **IF ≥ 10**: 🟡 우수
- **IF ≥ 5**: 🟢 양호
- **IF < 5**: 🔵 보통

## 🏗️ 프로젝트 구조

```
journal-impact-factor/
├── backend/
│   ├── app.py              # Flask API 서버
│   └── requirements.txt    # Python 의존성
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js         # 메인 React 컴포넌트
│   │   ├── App.css        # 스타일
│   │   ├── index.js
│   │   └── index.css
│   └── package.json       # Node.js 의존성
├── setup.sh               # 설치 스크립트
├── run.sh                 # 실행 스크립트
└── README.md
```

## 🔧 수동 실행 방법

### Backend 실행

```bash
cd backend
pip3 install -r requirements.txt
python3 app.py
# 서버가 http://localhost:5000 에서 실행됩니다
```

### Frontend 실행

```bash
cd frontend
npm install
npm start
# 브라우저가 자동으로 http://localhost:3000 을 엽니다
```

## 📝 데이터 추가 및 수정

`backend/app.py`의 `JOURNAL_DATABASE` 리스트에 저널을 추가할 수 있습니다:

```python
{
    "name": "저널 이름",
    "issn": "ISSN 번호",
    "impact_factor": IF 값,
    "category": "분야",
    "quartile": "Q1/Q2/Q3/Q4"
}
```

## 🎨 스크린샷

### 메인 화면
- 깔끔한 검색 인터페이스
- 실시간 통계 대시보드

### 검색 결과
- Impact Factor 시각화
- Quartile 등급 표시
- 저널 상세 정보

## 🔍 기술 스택

### Backend
- **Flask**: 경량 Python 웹 프레임워크
- **Flask-CORS**: Cross-Origin Resource Sharing 지원

### Frontend
- **React**: 사용자 인터페이스 라이브러리
- **Axios**: HTTP 클라이언트
- **CSS3**: 모던 스타일링

## 📌 주의사항

⚠️ **중요**: 이 애플리케이션은 **샘플 데이터**를 사용합니다. 실제 Impact Factor는 다음 공식 출처에서 확인하세요:

- [Clarivate Journal Citation Reports (JCR)](https://jcr.clarivate.com)
- [Scopus CiteScore](https://www.scopus.com/sources)
- [SCImago Journal Rank (SJR)](https://www.scimagojr.com)

## 🛠️ 문제 해결

### 포트 충돌
- **Backend**: `app.py`에서 포트 변경 (`port=5000` → `port=5001`)
- **Frontend**: `package.json`에서 `PORT=3001` 환경변수 설정

### 의존성 오류
```bash
# Backend 재설치
cd backend && pip3 install -r requirements.txt

# Frontend 재설치
cd frontend && rm -rf node_modules && npm install
```

### CORS 오류
- Backend가 실행 중인지 확인
- `flask-cors`가 설치되어 있는지 확인

## 📄 라이선스

MIT License

## 👨‍💻 개발자

이 프로젝트는 학술 연구를 지원하기 위해 개발되었습니다.

## 🤝 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다!

## 📞 문의

문제가 있거나 질문이 있으시면 Issue를 열어주세요.

---

**Made with ❤️ for Researchers**
# project_34
