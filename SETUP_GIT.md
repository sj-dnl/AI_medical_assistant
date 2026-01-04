# GitHub 업로드 가이드

## 1단계: Git 저장소 초기화

```bash
cd medical_assistant
git init
```

## 2단계: 파일 추가 및 커밋

```bash
# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: 의료 상담 시스템"
```

## 3단계: GitHub 저장소 생성

1. GitHub.com에 로그인
2. 우측 상단의 "+" 버튼 클릭 → "New repository" 선택
3. 저장소 이름 입력 (예: `medical-assistant`)
4. Public 또는 Private 선택
5. "Create repository" 클릭
   - ⚠️ **README, .gitignore, license 추가하지 말 것** (이미 있음)

## 4단계: 원격 저장소 연결 및 푸시

GitHub에서 제공하는 명령어를 사용하거나:

```bash
# 원격 저장소 추가 (YOUR_USERNAME과 YOUR_REPO_NAME을 변경)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 브랜치 이름을 main으로 설정 (필요한 경우)
git branch -M main

# 푸시
git push -u origin main
```

## 확인 사항

업로드 전에 다음을 확인하세요:

```bash
# 추가될 파일 확인
git status

# .gitignore가 제대로 작동하는지 확인
git status --ignored

# PDF 파일이 제외되는지 확인
git status | grep pdf
```

## 주의사항

- ✅ API 키는 환경 변수로 처리됨 (안전)
- ✅ .env 파일은 .gitignore에 포함됨
- ✅ PDF 파일은 .gitignore에 포함됨
- ✅ 환자 차트는 .gitignore에 포함됨

