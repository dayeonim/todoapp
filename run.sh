#!/bin/bash

echo "=================================="
echo "🚀 Journal Impact Factor 웹 시작"
echo "=================================="
echo ""

# 터미널 색상
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Backend 실행
echo -e "${BLUE}📡 Backend API 서버 시작 중...${NC}"
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

# Backend가 시작될 때까지 대기
echo "⏳ Backend 서버 준비 중..."
sleep 3

# Frontend 실행
echo -e "${GREEN}🎨 Frontend 개발 서버 시작 중...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "=================================="
echo "✅ 서버 실행 중!"
echo "=================================="
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "📡 Backend:  http://localhost:5000"
echo ""
echo "종료하려면: Ctrl+C"
echo ""

# 사용자가 Ctrl+C를 누르면 모든 프로세스 종료
trap "echo ''; echo '🛑 서버 종료 중...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM

# 프로세스가 종료될 때까지 대기
wait
