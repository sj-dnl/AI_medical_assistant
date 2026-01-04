#!/bin/bash

# 의료 상담 시스템 실행 스크립트

cd "$(dirname "$0")"

# 환경 변수 확인
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY 환경 변수가 설정되지 않았습니다."
    echo "다음 중 하나를 실행하세요:"
    echo "  export OPENAI_API_KEY='your-api-key'"
    echo "또는 .env 파일을 생성하세요."
    exit 1
fi

# Streamlit 앱 실행
echo "🚀 의료 상담 시스템을 시작합니다..."
streamlit run app/streamlit_app.py

