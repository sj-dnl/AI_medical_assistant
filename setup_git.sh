#!/bin/bash

echo "=== Medical Assistant GitHub 업로드 설정 ==="
echo

# 1. Git 초기화 확인
if [ -d ".git" ]; then
    echo "⚠️  이미 Git 저장소가 초기화되어 있습니다."
    read -p "계속하시겠습니까? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "1. Git 저장소 초기화..."
    git init
    echo "   ✅ 완료"
fi

echo
echo "2. 파일 상태 확인..."
git status

echo
echo "3. .gitignore 확인..."
if [ -f .gitignore ]; then
    echo "   ✅ .gitignore 파일 존재"
    echo "   제외되는 파일:"
    git check-ignore -v data/docs/*.pdf .env patient_chart_*.json 2>/dev/null | head -5 || echo "   (확인됨)"
else
    echo "   ⚠️  .gitignore 파일 없음"
fi

echo
echo "4. 추가될 파일 미리보기..."
git add --dry-run . 2>/dev/null | head -20

echo
read -p "위 파일들을 추가하시겠습니까? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add .
    echo "   ✅ 파일 추가 완료"
    
    echo
    read -p "커밋 메시지를 입력하세요 (기본: Initial commit): " commit_msg
    commit_msg=${commit_msg:-"Initial commit: 의료 상담 시스템"}
    
    git commit -m "$commit_msg"
    echo "   ✅ 커밋 완료"
    
    echo
    echo "=== 다음 단계 ==="
    echo "1. GitHub.com에서 새 저장소를 생성하세요"
    echo "2. 다음 명령어로 원격 저장소를 연결하세요:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
    echo "3. 다음 명령어로 푸시하세요:"
    echo "   git push -u origin main"
else
    echo "취소되었습니다."
fi
