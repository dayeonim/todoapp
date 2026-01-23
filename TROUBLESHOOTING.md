# 🔧 문제 해결 가이드

## localhost:3000이 실행되지 않는 경우

### 단계 1: 프론트엔드 의존성 설치

```bash
cd frontend
npm install
```

이 작업은 처음 한 번만 하면 됩니다 (약 2-3분 소요).

### 단계 2: 백엔드 의존성 설치

```bash
cd backend
pip3 install -r requirements.txt
```

### 단계 3: 백엔드 서버 먼저 실행

**터미널 1번:**
```bash
cd backend
python3 app.py
```

**결과 확인:**
```
Starting CCTV Abnormal Behavior Detection Server...
Server running on http://localhost:5000
```

이 메시지가 보이면 성공!

### 단계 4: 프론트엔드 실행

**터미널 2번 (새 터미널 열기):**
```bash
cd frontend
npm start
```

**결과 확인:**
```
Compiled successfully!
You can now view ... in the browser.
Local: http://localhost:3000
```

자동으로 브라우저가 열립니다!

---

## 자주 발생하는 문제들

### ❌ 오류 1: "npm: command not found"

**원인:** Node.js가 설치되지 않음

**해결:**
```bash
# macOS
brew install node

# 또는 https://nodejs.org 에서 다운로드
```

---

### ❌ 오류 2: "port 3000 already in use"

**원인:** 3000번 포트가 이미 사용 중

**해결 1:** 기존 프로세스 종료
```bash
lsof -ti:3000 | xargs kill
```

**해결 2:** 다른 포트 사용
```bash
PORT=3001 npm start
```

그러면 http://localhost:3001 에서 접속

---

### ❌ 오류 3: "port 5000 already in use"

**원인:** 5000번 포트가 이미 사용 중

**해결:** backend/app.py 수정
```python
# 마지막 줄 변경
socketio.run(app, host='0.0.0.0', port=5001, debug=True)
```

그리고 frontend/src/App.js에서도 수정:
```javascript
const API_URL = 'http://localhost:5001';  // 5000 → 5001
```

---

### ❌ 오류 4: "No module named 'flask'"

**원인:** Python 패키지가 설치되지 않음

**해결:**
```bash
cd backend
pip3 install -r requirements.txt
```

---

### ❌ 오류 5: 백엔드는 실행되지만 프론트엔드에서 연결 안 됨

**원인:** CORS 또는 네트워크 오류

**확인:**
1. 백엔드가 실행 중인지 확인: http://localhost:5000/api/health
2. 브라우저 콘솔(F12) 확인

**해결:** 
- 브라우저를 새로고침 (Cmd+Shift+R)
- 백엔드를 재시작

---

### ❌ 오류 6: "Module not found: Can't resolve 'socket.io-client'"

**원인:** npm install이 제대로 안 됨

**해결:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 완전 초기화 후 다시 시작

모든 게 꼬였다면 처음부터:

```bash
# 1. 프론트엔드 초기화
cd frontend
rm -rf node_modules package-lock.json
npm install

# 2. 백엔드 초기화
cd ../backend
pip3 install -r requirements.txt

# 3. 백엔드 실행 (터미널 1)
python3 app.py

# 4. 프론트엔드 실행 (터미널 2)
cd ../frontend
npm start
```

---

## 실행 순서 요약

```
1. backend 의존성 설치 (처음 1회)
   └─ pip3 install -r requirements.txt

2. frontend 의존성 설치 (처음 1회)
   └─ npm install

3. 백엔드 실행 (항상 먼저!)
   └─ python3 backend/app.py

4. 프론트엔드 실행
   └─ npm start (frontend 폴더에서)

5. 브라우저 접속
   └─ http://localhost:3000
```

---

## 빠른 실행 스크립트 사용

매번 명령어 치기 귀찮다면:

```bash
# 한 번만 실행
./setup.sh

# 이후 실행할 때마다
./run.sh
```

---

## 포트 확인 방법

```bash
# 5000번 포트 사용 중인지 확인
lsof -i :5000

# 3000번 포트 사용 중인지 확인
lsof -i :3000

# 강제 종료
lsof -ti:5000 | xargs kill
lsof -ti:3000 | xargs kill
```

---

## 여전히 안 되나요?

체크리스트:
- [ ] Node.js 설치됨? (`node --version`)
- [ ] Python 설치됨? (`python3 --version`)
- [ ] backend 폴더에서 `pip3 install -r requirements.txt` 실행함?
- [ ] frontend 폴더에서 `npm install` 실행함?
- [ ] 백엔드가 먼저 실행됨? (http://localhost:5000/api/health 확인)
- [ ] 프론트엔드 실행함? (`npm start`)
- [ ] 터미널에 에러 메시지가 있나요? (메시지를 확인하세요)

에러 메시지를 알려주시면 더 정확한 도움을 드릴 수 있습니다!
