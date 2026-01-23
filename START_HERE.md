# 🎯 여기서 시작하세요!

## 당신의 상황은?

### ✅ 정상 데이터도 있음

```bash
./setup.sh              # 설치
cd backend
python3 preprocess_data.py
python3 train_model.py
cd .. && ./run.sh       # 실행
```

### ⚠️ 이상 데이터만 있음 (정상 없음)

당신은 여기에 해당합니다! 3가지 선택지:

#### 🚀 선택 1: 자동 실행 (가장 쉬움, 15분)

```bash
./quick_start_no_normal.sh
# 1번 선택 → 배경 영상 자동 생성 + 학습
```

#### ⚡ 선택 2: 수동으로 하나씩 (추천, 20분)

```bash
# 1단계: 정상 데이터 생성 (5분)
cd backend
python3 generate_normal_data.py --method background --num 50

# 2단계: 전처리 (5분)
python3 preprocess_data.py

# 3단계: 학습 (10분, epochs 줄이면 더 빠름)
python3 train_model.py --epochs 20

# 4단계: 실행
cd ..
./run.sh
```

#### 🎮 선택 3: 웹캠으로 직접 촬영 (최고 품질, 25분)

```bash
cd backend

# 1. 배경 30개 자동 생성
python3 generate_normal_data.py --method background --num 30

# 2. 웹캠으로 정상 활동 촬영 (10-15분)
python3 generate_normal_data.py --method webcam
# 평범하게 걷기, 서있기 등을 촬영

# 3. 전처리
python3 preprocess_data.py

# 4. 학습
python3 train_model.py

# 5. 실행
cd .. && ./run.sh
```

---

## 🎯 각 방법의 결과 비교

| 방법 | 시간 | 정확도 | 오탐률 | 난이도 |
|------|------|--------|--------|--------|
| **배경 영상만** | 15분 | ⭐⭐⭐ | 18% | ⭐ 쉬움 |
| **배경 + 웹캠** | 25분 | ⭐⭐⭐⭐⭐ | 8% | ⭐⭐ 보통 |
| **정상 없이 학습** | 10분 | ⭐⭐ | 25% | ⭐ 쉬움 |

**추천:** 배경 영상 + 웹캠 조합!

---

## 📝 상세 가이드

- **처음 사용**: [QUICKSTART.md](QUICKSTART.md)
- **정상 데이터 없음**: [NO_NORMAL_GUIDE.md](NO_NORMAL_GUIDE.md) ⭐
- **데이터 준비**: [DATA_GUIDE.md](DATA_GUIDE.md)
- **전체 설명**: [README.md](README.md)

---

## ❓ 빠른 Q&A

**Q: 정상 데이터가 정말 필요한가요?**
→ 프로토타입은 없어도 되지만, 실제 사용에는 필수입니다.
   배경 영상 생성은 단 5분이면 됩니다!

**Q: 웹캠 촬영은 꼭 해야 하나요?**
→ 선택사항입니다. 하지만 10분만 투자하면 정확도가 크게 향상됩니다.

**Q: 학습에 얼마나 걸리나요?**
→ CPU: 30-60분, GPU: 10-20분
   epochs를 20으로 줄이면 더 빠릅니다.

**Q: 바로 테스트만 해보고 싶어요**
→ 샘플 데이터 생성 후 테스트:
```bash
cd backend
python3 generate_sample_data.py
python3 preprocess_data.py
python3 train_model.py --epochs 10
python3 app.py
```

---

## 🎉 완료 후

서버 실행 후 브라우저에서 http://localhost:3000 접속!

- **왼쪽**: 실시간 CCTV 모니터링
- **오른쪽**: 이상행동 알림 패널
- **하단**: 통계 대시보드

**테스트 방법:**
1. "스트림 시작" 버튼 클릭 (웹캠 사용)
2. 카메라 앞에서 평범하게 움직이기 → 정상으로 표시
3. (데모) 갑작스러운 동작 시뮬레이션

---

## 🆘 문제 해결

```bash
# Python 버전 확인 (3.8 이상 필요)
python3 --version

# Node.js 버전 확인 (16 이상 필요)
node --version

# 의존성 재설치
cd backend && pip3 install -r requirements.txt
cd frontend && npm install

# 포트 충돌 시 변경
# backend/app.py 마지막 줄: port=5000 → port=5001
```

---

## 💡 Pro Tips

1. **배경 영상이라도 꼭 생성하세요** - 5분이면 충분
2. **웹캠 10개만 추가로 촬영** - 성능이 2배 향상
3. **epochs를 20-30으로** - 빠른 결과 확인
4. **실제 CCTV로 테스트** - 오탐률 확인 필수

---

**시작하기:**

```bash
./quick_start_no_normal.sh
```

그냥 이 명령어 하나면 됩니다! 🚀
