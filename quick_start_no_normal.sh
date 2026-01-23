#!/bin/bash

echo "======================================"
echo "🚀 정상 데이터 없이 빠른 시작"
echo "======================================"
echo ""
echo "이 스크립트는 정상 데이터 없이 시스템을 실행합니다."
echo ""

# 색상
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}선택하세요:${NC}"
echo ""
echo "1. 배경 영상 생성 + 학습 (추천, 15분)"
echo "2. 정상 없이 바로 학습 (5분, 정확도 낮음)"
echo "3. 웹캠으로 정상 데이터 촬영 + 학습 (20분, 최고 품질)"
echo ""
read -p "선택 (1/2/3): " choice

cd backend

case $choice in
    1)
        echo ""
        echo -e "${BLUE}[1단계] 배경 영상 생성 중...${NC}"
        python3 generate_normal_data.py --method background --num 50
        
        echo ""
        echo -e "${BLUE}[2단계] 데이터 전처리 중...${NC}"
        python3 preprocess_data.py
        
        echo ""
        echo -e "${BLUE}[3단계] 모델 학습 중...${NC}"
        python3 train_model.py --epochs 30
        
        echo ""
        echo -e "${GREEN}✨ 완료!${NC}"
        echo ""
        echo "서버 시작: python3 app.py"
        ;;
    
    2)
        echo ""
        echo -e "${YELLOW}⚠️  경고: 정상 데이터 없이 학습합니다.${NC}"
        echo "   오탐률이 높을 수 있습니다."
        echo ""
        read -p "계속하시겠습니까? (y/n): " confirm
        
        if [ "$confirm" = "y" ]; then
            echo ""
            echo -e "${BLUE}[1단계] 데이터 전처리 중...${NC}"
            python3 preprocess_data.py
            
            echo ""
            echo -e "${BLUE}[2단계] 모델 학습 중 (정상 없음)...${NC}"
            python3 train_model_no_normal.py
            
            echo ""
            echo -e "${GREEN}✨ 완료!${NC}"
            echo ""
            echo -e "${YELLOW}app.py 수정 필요:${NC}"
            echo "  model_handler = ModelHandler(use_no_normal_model=True)"
            echo ""
            echo "서버 시작: python3 app.py"
        fi
        ;;
    
    3)
        echo ""
        echo -e "${BLUE}[1단계] 배경 영상 30개 생성...${NC}"
        python3 generate_normal_data.py --method background --num 30
        
        echo ""
        echo -e "${BLUE}[2단계] 웹캠 촬영 시작${NC}"
        echo "평범한 활동을 촬영해주세요 (걷기, 서있기 등)"
        python3 generate_normal_data.py --method webcam
        
        echo ""
        echo -e "${BLUE}[3단계] 데이터 전처리 중...${NC}"
        python3 preprocess_data.py
        
        echo ""
        echo -e "${BLUE}[4단계] 모델 학습 중...${NC}"
        python3 train_model.py
        
        echo ""
        echo -e "${GREEN}✨ 완료!${NC}"
        echo ""
        echo "서버 시작: python3 app.py"
        ;;
    
    *)
        echo -e "${RED}잘못된 선택입니다.${NC}"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo -e "${GREEN}🎉 설정 완료!${NC}"
echo "======================================"
echo ""
echo "다음 단계:"
echo "  1. 터미널 1: cd backend && python3 app.py"
echo "  2. 터미널 2: cd frontend && npm start"
echo "  3. 브라우저: http://localhost:3000"
echo ""
