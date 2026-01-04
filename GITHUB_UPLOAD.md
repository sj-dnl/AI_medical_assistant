# GitHub 업로드 가이드

## ✅ 완료된 작업
- Git 저장소 초기화 완료
- 파일 추가 및 커밋 완료
- 민감한 파일(.env, PDF, 환자 차트) 제외 확인

## 다음 단계: GitHub에 업로드

### 방법 1: GitHub 웹사이트에서 저장소 생성 후 연결

1. **GitHub.com 접속 및 로그인**
   - https://github.com 접속
   - 로그인

2. **새 저장소 생성**
   - 우측 상단 "+" 버튼 클릭 → "New repository" 선택
   - Repository name 입력 (예: `medical-assistant`)
   - Description 입력 (선택사항): "이비인후과 청각 장애 전문 상담 시스템"
   - Public 또는 Private 선택
   - ⚠️ **중요**: "Add a README file", "Add .gitignore", "Choose a license" 모두 체크 해제
     (이미 파일들이 있으므로)
   - "Create repository" 클릭

3. **로컬 저장소와 연결**
   ```bash
   cd medical_assistant
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### 방법 2: GitHub CLI 사용 (설치되어 있는 경우)

```bash
cd medical_assistant
gh repo create medical-assistant --public --source=. --remote=origin --push
```

## 확인

업로드 후 GitHub에서 확인:
- ✅ 모든 파일이 올라갔는지 확인
- ✅ PDF 파일이 제외되었는지 확인
- ✅ .env 파일이 없는지 확인
- ✅ README.md가 제대로 표시되는지 확인

## 문제 해결

### 이미 원격 저장소가 있는 경우
```bash
git remote -v  # 원격 저장소 확인
git remote remove origin  # 기존 원격 저장소 제거
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 브랜치 이름이 다른 경우
```bash
git branch  # 현재 브랜치 확인
git branch -M main  # main으로 변경
```

