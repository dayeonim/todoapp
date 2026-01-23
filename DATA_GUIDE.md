# 데이터 준비 가이드

## 📁 데이터 디렉토리 구조

데이터를 아래와 같은 구조로 준비해주세요:

```
data/
├── raw/                    # 원본 영상 파일 (제공받은 CCTV 영상)
│   ├── fall/              # 전도 영상들
│   │   ├── video001.mp4
│   │   ├── video002.mp4
│   │   └── ...
│   ├── vandalism/         # 파손 영상들
│   ├── fire/              # 방화 영상들
│   ├── smoking/           # 흡연 영상들
│   ├── abandonment/       # 유기 영상들
│   ├── theft/             # 절도 영상들
│   ├── assault/           # 폭행 영상들
│   ├── vulnerable/        # 이동약자 영상들
│   └── normal/            # 정상 영상들
│
├── processed/             # 전처리된 데이터 (자동 생성)
│   ├── train/
│   ├── val/
│   └── test/
│
└── annotations/           # (선택) 라벨 정보 JSON 파일
    └── labels.json
```

## 📊 데이터 형식

### 1. 비디오 파일
- **지원 형식**: .mp4, .avi, .mov, .mkv
- **권장 해상도**: 640x480 이상
- **권장 FPS**: 15-30fps
- **권장 길이**: 3-10초 클립
  - 너무 긴 영상은 자동으로 세그먼트로 분할됩니다

### 2. 파일 이름 규칙 (선택사항)
```
{행동유형}_{장소}_{날짜}_{순번}.mp4

예시:
- fall_store1_20240115_001.mp4
- theft_store2_20240116_005.mp4
```

### 3. 라벨 정보 (annotations/labels.json)
JSON 형식으로 추가 정보를 제공할 수 있습니다:

```json
{
  "videos": [
    {
      "filename": "fall_store1_20240115_001.mp4",
      "label": "fall",
      "timestamp": "2024-01-15T14:30:00",
      "camera_id": "store1_cam01",
      "duration": 5.2,
      "severity": "high",
      "verified": true,
      "notes": "노인 전도 사고"
    }
  ]
}
```

## 🎯 클래스별 데이터 요구사항

| 클래스 | 최소 영상 수 | 권장 영상 수 | 특징 |
|--------|-------------|-------------|------|
| fall (전도) | 100 | 500+ | 넘어지는 순간 포함 |
| vandalism (파손) | 100 | 500+ | 물건 파손 행위 |
| fire (방화) | 50 | 300+ | 불, 연기 포함 |
| smoking (흡연) | 100 | 500+ | 담배 피우는 모습 |
| abandonment (유기) | 50 | 300+ | 물건/사람 방치 |
| theft (절도) | 100 | 500+ | 물건 가져가는 행위 |
| assault (폭행) | 100 | 500+ | 폭력 행위 |
| vulnerable (이동약자) | 100 | 500+ | 휠체어, 목발 사용자 등 |
| **normal (정상)** | **200** | **1000+** | **일반 활동** |

⚠️ **중요**: `normal` 클래스의 데이터가 충분해야 오탐지가 줄어듭니다!

## 📦 데이터 제공 방법

### 방법 1: 로컬 폴더 (권장)
```bash
# 1. data/raw/ 폴더에 영상 파일들을 클래스별로 분류하여 복사
cp /path/to/your/videos/fall/*.mp4 data/raw/fall/
cp /path/to/your/videos/theft/*.mp4 data/raw/theft/
# ... 반복

# 2. 전처리 스크립트 실행
python backend/preprocess_data.py
```

### 방법 2: 압축 파일
```bash
# 1. 데이터를 위의 구조로 압축
tar -czf cctv_dataset.tar.gz data/

# 2. 압축 해제
tar -xzf cctv_dataset.tar.gz

# 3. 전처리 실행
python backend/preprocess_data.py
```

### 방법 3: 클라우드 스토리지 (대용량)
Google Drive, AWS S3 등에서 다운로드:
```bash
# Google Drive 예시
pip install gdown
gdown --folder YOUR_GOOGLE_DRIVE_FOLDER_ID -O data/raw/

# AWS S3 예시
aws s3 sync s3://your-bucket/cctv-data/ data/raw/
```

## 🔄 데이터 전처리 과정

전처리 스크립트(`preprocess_data.py`)가 자동으로 수행:

1. **영상 로드 및 검증**
   - 손상된 파일 제거
   - 해상도/FPS 확인

2. **프레임 추출**
   - 영상을 프레임 시퀀스로 변환
   - 일정 간격으로 샘플링

3. **데이터 증강** (선택)
   - 좌우 반전
   - 밝기 조절
   - 노이즈 추가

4. **Train/Val/Test 분할**
   - Train: 70%
   - Validation: 15%
   - Test: 15%

5. **정규화 및 저장**
   - NumPy 배열로 저장
   - 메타데이터 생성

## 📈 데이터 품질 체크리스트

- [ ] 모든 클래스에 최소 요구사항 이상의 데이터가 있는가?
- [ ] 영상이 선명하고 주요 행동이 잘 보이는가?
- [ ] 다양한 각도/조명 조건의 데이터가 포함되어 있는가?
- [ ] 정상 클래스 데이터가 충분한가?
- [ ] 라벨이 정확한가?
- [ ] 중복 영상이 없는가?

## 🚀 빠른 시작

```bash
# 1. 데이터 폴더 생성
mkdir -p data/raw/{fall,vandalism,fire,smoking,abandonment,theft,assault,vulnerable,normal}

# 2. 영상 파일 복사
# 각 행동별 폴더에 해당하는 CCTV 영상을 복사

# 3. 데이터 전처리
python backend/preprocess_data.py

# 4. 모델 학습
python backend/train_model.py

# 5. 학습된 모델로 웹 서버 시작
python backend/app.py
```

## ❓ FAQ

**Q: 영상이 너무 길어요 (30초 이상)**
A: 전처리 스크립트가 자동으로 짧은 클립으로 분할합니다.

**Q: 한 영상에 여러 행동이 있어요**
A: 주요 행동 하나를 선택하거나, 영상 편집 도구로 분리하세요.

**Q: 데이터가 부족해요**
A: 데이터 증강 옵션을 활성화하거나, 공개 데이터셋을 추가로 활용하세요.

**Q: 라벨링이 애매한 영상이 있어요**
A: 확실하지 않은 영상은 제외하는 것이 좋습니다.
