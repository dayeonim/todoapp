# 🔗 n8n 연동 가이드

CCTV 이상행동 감지 시스템을 n8n과 연동하여 자동화 워크플로우를 구축하는 방법입니다.

---

## 📋 목차

1. [n8n이란?](#n8n이란)
2. [연동 방법](#연동-방법)
3. [n8n 워크플로우 설정](#n8n-워크플로우-설정)
4. [활용 예시](#활용-예시)
5. [테스트](#테스트)

---

## 🤔 n8n이란?

n8n은 강력한 워크플로우 자동화 도구입니다. CCTV에서 이상행동이 감지되면 자동으로:
- 📧 이메일 발송
- 💬 Slack/Discord/Telegram 알림
- 📱 SMS 발송
- 💾 데이터베이스 저장
- 🚨 관리자 호출
- 📊 통계 수집

등 다양한 액션을 자동으로 실행할 수 있습니다!

---

## 🔌 연동 방법

### 1단계: n8n 설치 (이미 있다면 생략)

#### 로컬 설치:
```bash
npx n8n
# 또는
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```

#### 클라우드 사용:
https://n8n.io/cloud 에서 무료 계정 생성

---

### 2단계: n8n에서 Webhook 생성

1. **n8n 접속** (http://localhost:5678 또는 클라우드 URL)

2. **새 워크플로우 생성**
   - 좌측 상단 "+" 버튼 클릭

3. **Webhook 노드 추가**
   - 노드 추가 → "Webhook" 검색
   - Webhook 노드 클릭

4. **Webhook 설정**
   ```
   HTTP Method: POST
   Path: cctv-alert (원하는 경로)
   Authentication: None (또는 원하는 인증 방식)
   Response Mode: Respond Immediately
   ```

5. **Webhook URL 복사**
   ```
   예시: https://your-n8n.com/webhook/cctv-alert
   또는: http://localhost:5678/webhook/cctv-alert
   ```

---

### 3단계: CCTV 시스템에 Webhook URL 설정

#### 방법 1: 환경변수 (권장)

```bash
# 터미널에서:
export N8N_WEBHOOK_URL="https://your-n8n.com/webhook/cctv-alert"

# 그 다음 서버 실행:
cd backend
python3 app.py
```

#### 방법 2: 코드에 직접 입력

`backend/app.py` 파일 수정:
```python
# 15번째 줄 근처
N8N_WEBHOOK_URL = 'https://your-n8n.com/webhook/cctv-alert'
```

#### 방법 3: API로 설정

서버 실행 후:
```bash
curl -X POST http://localhost:5000/api/n8n/config \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://your-n8n.com/webhook/cctv-alert"}'
```

---

## 🎨 n8n 워크플로우 설정

### 기본 워크플로우 (이메일 알림)

```
Webhook → Email
```

**Email 노드 설정:**
- To: manager@company.com
- Subject: `🚨 [긴급] {{$json.detection.action_korean}} 감지!`
- Message: 
  ```
  이상행동이 감지되었습니다.

  📹 카메라: {{$json.detection.camera_id}}
  ⚠️  행동: {{$json.detection.action_korean}}
  📊 신뢰도: {{$json.detection.confidence}}%
  🚨 심각도: {{$json.detection.severity}}
  ⏰ 시간: {{$json.detection.timestamp}}

  즉시 확인이 필요합니다.
  ```

---

### 고급 워크플로우 (조건부 알림)

```
Webhook → Switch (심각도 체크) → 
    ├─ Critical: Slack + SMS + Email
    ├─ High: Slack + Email
    └─ Medium: Email만
```

**Switch 노드 설정:**
```javascript
// Critical (방화, 폭행)
{{ $json.detection.severity === "critical" }}

// High (전도, 파손, 절도)
{{ $json.detection.severity === "high" }}

// Medium (흡연, 유기, 이동약자)
{{ $json.detection.severity === "medium" }}
```

---

### Slack 알림 예시

**Slack 노드 추가:**
- Channel: #cctv-alerts
- Message:
  ```
  :rotating_light: *이상행동 감지!*
  
  *행동:* {{$json.detection.action_korean}}
  *카메라:* {{$json.detection.camera_id}}
  *신뢰도:* {{$json.detection.confidence}}
  *시간:* {{$json.detection.timestamp}}
  
  <http://your-dashboard.com|대시보드 보기>
  ```

---

### Discord Webhook 예시

**HTTP Request 노드:**
```json
{
  "method": "POST",
  "url": "YOUR_DISCORD_WEBHOOK_URL",
  "body": {
    "embeds": [{
      "title": "🚨 이상행동 감지",
      "color": 15158332,
      "fields": [
        {"name": "행동", "value": "{{$json.detection.action_korean}}", "inline": true},
        {"name": "카메라", "value": "{{$json.detection.camera_id}}", "inline": true},
        {"name": "신뢰도", "value": "{{$json.detection.confidence}}", "inline": true},
        {"name": "심각도", "value": "{{$json.detection.severity}}", "inline": true}
      ],
      "timestamp": "{{$json.detection.timestamp}}"
    }]
  }
}
```

---

## 💡 활용 예시

### 예시 1: 관리자 호출 시스템

```
Webhook → 
  IF 심각도 = critical → 
    ├─ Twilio (SMS 발송)
    ├─ Slack (관리자 멘션)
    └─ Google Sheets (로그 기록)
```

### 예시 2: 통계 수집

```
Webhook → 
  ├─ Airtable (데이터 저장)
  ├─ Google Sheets (통계)
  └─ Notion (일일 리포트)
```

### 예시 3: 다중 채널 알림

```
Webhook → 
  ├─ Slack (팀 알림)
  ├─ Discord (보안팀 알림)
  ├─ Email (매니저)
  ├─ Telegram (모바일)
  └─ Microsoft Teams (본사)
```

### 예시 4: AI 기반 의사결정

```
Webhook → 
  OpenAI (상황 분석) → 
    Switch (AI 판단) → 
      ├─ 긴급: 즉시 통보
      └─ 일반: 로그만 기록
```

---

## 🧪 테스트

### 1. n8n 연결 테스트

```bash
# API로 테스트
curl -X POST http://localhost:5000/api/n8n/test
```

**예상 결과:**
```json
{
  "success": true,
  "message": "n8n 테스트 전송 완료",
  "webhook_url": "https://your-n8n.com/webhook/cctv-alert"
}
```

### 2. 실제 감지 테스트

1. 웹 대시보드 실행 (http://localhost:3000)
2. "스트림 시작" 클릭
3. 카메라 앞에서 이상행동 시뮬레이션
4. n8n 워크플로우 실행 확인!

### 3. 수동 테스트 (curl)

```bash
curl -X POST http://localhost:5000/api/analyze-frame \
  -H "Content-Type: application/json" \
  -d '{
    "frame": "BASE64_ENCODED_IMAGE",
    "camera_id": "test_camera"
  }'
```

---

## 📊 전송되는 데이터 구조

```json
{
  "event_type": "abnormal_behavior_detected",
  "detection": {
    "id": 123,
    "timestamp": "2024-01-23T14:30:00.123456",
    "camera_id": "camera_1",
    "action": "theft",
    "action_korean": "절도",
    "confidence": 0.92,
    "severity": "high"
  },
  "metadata": {
    "system": "CCTV Abnormal Detection System",
    "version": "1.0.0"
  }
}
```

---

## 🔒 보안 고려사항

### 1. Webhook 인증

n8n Webhook 노드에서 인증 설정:
- Header Auth
- Basic Auth
- Custom Authentication

### 2. HTTPS 사용

프로덕션 환경에서는 반드시 HTTPS 사용:
```bash
export N8N_WEBHOOK_URL="https://your-n8n.com/webhook/cctv-alert"
```

### 3. 환경변수 사용

코드에 직접 입력하지 말고 환경변수 사용:
```bash
# .env 파일
N8N_WEBHOOK_URL=https://your-n8n.com/webhook/cctv-alert

# 또는 시스템 환경변수
export N8N_WEBHOOK_URL="..."
```

---

## 🎯 실전 배포 체크리스트

- [ ] n8n 워크플로우 생성 및 활성화
- [ ] Webhook URL 복사
- [ ] 환경변수 설정 (`N8N_WEBHOOK_URL`)
- [ ] 연결 테스트 (`/api/n8n/test`)
- [ ] 실제 감지 테스트
- [ ] 알림 채널 확인 (Slack, Email 등)
- [ ] 심각도별 분기 로직 검증
- [ ] HTTPS 사용 확인
- [ ] 인증 설정 (프로덕션)
- [ ] 에러 처리 확인

---

## 📱 모바일 알림 설정

### Telegram 봇

1. BotFather에서 봇 생성
2. n8n에서 Telegram 노드 추가
3. 메시지 템플릿:
   ```
   🚨 *이상행동 감지*
   
   행동: {{$json.detection.action_korean}}
   카메라: {{$json.detection.camera_id}}
   시간: {{$json.detection.timestamp}}
   ```

### Twilio SMS

1. Twilio 계정 생성
2. n8n에서 Twilio 노드 추가
3. 전화번호: +82 10-XXXX-XXXX
4. 메시지: 짧고 명확하게

---

## 🔄 실시간 모니터링

### n8n 실행 로그

n8n 워크플로우에서 "Executions" 탭 확인:
- 성공/실패 여부
- 실행 시간
- 전송된 데이터
- 에러 메시지

### CCTV 시스템 로그

터미널에서 확인:
```
✅ n8n 전송 성공: theft
❌ n8n 전송 실패: 404
⚠️  n8n Webhook URL이 설정되지 않았습니다.
```

---

## 🚀 빠른 시작

```bash
# 1. n8n 실행
npx n8n
# → http://localhost:5678 접속

# 2. Webhook 생성
# → URL 복사: http://localhost:5678/webhook/cctv-alert

# 3. 환경변수 설정
export N8N_WEBHOOK_URL="http://localhost:5678/webhook/cctv-alert"

# 4. CCTV 시스템 실행
cd backend
python3 app.py

# 5. 테스트
curl -X POST http://localhost:5000/api/n8n/test
```

완료! 🎉

---

## ❓ FAQ

**Q: n8n이 꼭 필요한가요?**
A: 아니요. n8n 없이도 웹 대시보드에서 알림을 볼 수 있습니다. n8n은 추가 자동화를 위한 선택사항입니다.

**Q: 무료인가요?**
A: n8n 오픈소스는 무료입니다. 셀프호스팅도 무료이고, 클라우드는 제한적 무료 플랜이 있습니다.

**Q: 다른 자동화 도구도 가능한가요?**
A: 네! Zapier, Make(Integromat), Power Automate 등 Webhook을 지원하는 모든 도구와 호환됩니다.

**Q: 여러 개의 n8n 워크플로우를 사용할 수 있나요?**
A: 네, 하나의 Webhook에서 여러 경로로 분기하거나, 여러 Webhook URL을 설정할 수 있습니다.

---

## 📚 더 알아보기

- **n8n 공식 문서**: https://docs.n8n.io
- **n8n 커뮤니티**: https://community.n8n.io
- **예제 워크플로우**: https://n8n.io/workflows

---

이제 CCTV 시스템과 n8n이 완벽하게 연동되었습니다! 🎊
