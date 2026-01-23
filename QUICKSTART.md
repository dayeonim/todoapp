# 🚀 빠른 시작 가이드

CCTV 이상행동 감지 시스템을 빠르게 실행하는 방법입니다.

## 📋 사전 요구사항

- Python 3.8 이상
- Node.js 16 이상
- 웹캠 (실시간 테스트용, 선택사항)

## 🎯 방법 1: 실제 데이터로 시작하기 (권장)

### 1단계: 데이터 준비

```bash
# 데이터 폴더 생성
mkdir -p data/raw/{fall,vandalism,fire,smoking,abandonment,theft,assault,vulnerable,normal}

# 보유하고 있는 CCTV 영상을 해당 폴더에 복사
# 예: 전도 영상들을 data/raw/fall/ 폴더에 복사
```

**데이터 요구사항:**
- 각 클래스별 최소 50개 이상의 영상
- 지원 형식: .mp4, .avi, .mov, .mkv
- 권장 길이: 3-10초

자세한 내용은 [DATA_GUIDE.md](DATA_GUIDE.md)를 참고하세요.

### 2단계: 백엔드 설정

```bash
# 의존성 설치
cd backend
pip install -r requirements.txt

# 데이터 전처리
python preprocess_data.py

# 모델 학습 (30분~2시간 소요)
python train_model.py
```

### 3단계: 프론트엔드 설정

```bash
# 새 터미널 열기
cd frontend
npm install
```

### 4단계: 실행

```bash
# 터미널 1: 백엔드 서버
cd backend
python app.py

# 터미널 2: 프론트엔드
cd frontend
npm start
```

브라우저에서 http://localhost:3000 접속!

---

## 🧪 방법 2: 샘플 데이터로 빠른 테스트 (5분)

실제 데이터가 없거나 빠르게 테스트하고 싶을 때 사용하세요.

### 1단계: 샘플 데이터 생성

```bash
cd backend
pip install -r requirements.txt
python generate_sample_data.py
```

이렇게 하면 90개의 테스트용 합성 영상이 생성됩니다.

### 2단계: 데이터 전처리 및 학습

```bash
python preprocess_data.py
python train_model.py
```

### 3단계: 프론트엔드 설정

```bash
cd frontend
npm install
```

### 4단계: 실행

```bash
# 터미널 1: 백엔드
cd backend
python app.py

# 터미널 2: 프론트엔드
cd frontend
npm start
```

---

## 🎮 사용 방법

### 실시간 모니터링
1. 웹 대시보드에서 "스트림 시작" 버튼 클릭
2. 웹캠 접근 허용
3. 실시간으로 이상행동 감지 시작!

### 비디오 분석
1. "비디오 업로드" 버튼 클릭
2. CCTV 영상 파일 선택
3. 자동으로 전체 영상 분석 후 결과 표시

### 알림 확인
- 오른쪽 패널에서 실시간 알림 확인
- 감지된 이상행동의 심각도(severity)에 따라 색상 표시
  - 🔴 Critical: 방화, 폭행
  - 🟠 High: 전도, 파손, 절도
  - 🟡 Medium: 흡연, 유기, 이동약자
  - 🟢 Low: 정상

---

## 📊 디렉토리 구조

```
todo app 만들기/
├── backend/                    # 백엔드 (Flask + AI 모델)
│   ├── app.py                 # 메인 서버
│   ├── model_handler.py       # 모델 로딩 및 추론
│   ├── preprocess_data.py     # 데이터 전처리
│   ├── train_model.py         # 모델 학습
│   ├── generate_sample_data.py # 샘플 데이터 생성
│   └── requirements.txt       # Python 의존성
├── frontend/                   # 프론트엔드 (React)
│   ├── src/
│   │   ├── App.js            # 메인 컴포넌트
│   │   └── App.css           # 스타일
│   ├── public/
│   └── package.json          # Node.js 의존성
├── data/                       # 데이터
│   ├── raw/                   # 원본 영상
│   └── processed/             # 전처리된 데이터
├── models/                     # 학습된 모델
│   └── abnormal_detector.h5  # 최종 모델
├── README.md                  # 프로젝트 개요
├── DATA_GUIDE.md              # 데이터 준비 상세 가이드
└── QUICKSTART.md              # 이 파일
```

---

## 🔧 문제 해결

### "No module named 'tensorflow'" 오류
```bash
pip install tensorflow==2.15.0
```

### 포트 충돌 (5000번 포트가 사용 중)
`backend/app.py` 마지막 줄의 포트 번호 변경:
```python
socketio.run(app, host='0.0.0.0', port=5001, debug=True)
```

### 웹캠 접근 불가
- 브라우저 설정에서 카메라 권한 확인
- HTTPS 환경에서만 작동하는 경우가 있으므로 localhost 사용 확인

### 모델 학습이 너무 느림
`backend/train_model.py`에서 epochs 줄이기:
```python
epochs=20  # 기본값 50에서 감소
```

---

## 📚 추가 리소스

- **데이터 준비**: [DATA_GUIDE.md](DATA_GUIDE.md)
- **전체 문서**: [README.md](README.md)
- **API 문서**: 서버 실행 후 http://localhost:5000/api/health

---

## 💡 팁

1. **정확도 향상**: 더 많은 데이터와 긴 학습 시간이 정확도를 높입니다
2. **실시간 성능**: GPU를 사용하면 훨씬 빠른 추론 가능
3. **다중 카메라**: 여러 카메라 동시 모니터링 지원
4. **알림 커스터마이징**: `backend/app.py`에서 알림 조건 수정 가능

---

## 🤝 도움이 필요하신가요?

시스템이 제대로 작동하지 않으면:
1. 터미널의 에러 메시지 확인
2. 브라우저 콘솔(F12) 확인
3. `python --version` (3.8 이상 필요)
4. `node --version` (16 이상 필요)

즐거운 개발 되세요! 🎉
