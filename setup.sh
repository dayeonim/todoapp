#!/bin/bash

echo "=================================="
echo "🔬 Journal Impact Factor 웹 설치"
echo "=================================="
echo ""

# Python 버전 확인
echo "📌 Python 버전 확인 중..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3이 설치되어 있지 않습니다."
    exit 1
fi

# Node.js 버전 확인
echo "📌 Node.js 버전 확인 중..."
node --version
if [ $? -ne 0 ]; then
    echo "❌ Node.js가 설치되어 있지 않습니다."
    exit 1
fi

echo ""
echo "=================================="
echo "📦 Backend 설치 중..."
echo "=================================="
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Backend 의존성 설치 실패"
    exit 1
fi
cd ..

echo ""
echo "=================================="
echo "📦 Frontend 설치 중..."
echo "=================================="
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Frontend 의존성 설치 실패"
    exit 1
fi
cd ..

echo ""
echo "=================================="
echo "✅ 설치 완료!"
echo "=================================="
echo ""
echo "실행 방법:"
echo "  ./run.sh"
echo ""
