# 🏥 의료 상담 시스템 (Medical Assistant)

SNU Project – AI Medical Assistant for Hearing Loss

이비인후과 청각 장애 전문 상담 시스템입니다. RAG 기술을 활용하여 의학 문헌 기반 상담을 제공합니다.

## ✨ 주요 기능

- 💬 **대화형 의료 상담**: AI 의사와 자연스러운 대화
- 🔍 **증상 기반 진단**: 수집된 증상을 분석하여 가능한 질환 추정
- 📊 **환자 차트 자동 생성**: 대화 내용에서 정보를 자동 추출
- 📋 **최종 진단 보고서**: RAG 기반 의학 문헌 참조 진단
- 💾 **차트 저장/다운로드**: JSON 형식으로 환자 정보 저장

## 📁 프로젝트 구조

```
medical_assistant/
├── app/
│   └── streamlit_app.py        # Streamlit UI 엔트리포인트
│
├── core/
│   ├── rag/
│   │   └── rag_system.py       # RAG 검색·응답 로직
│   │
│   ├── consultation/
│   │   └── medical_consultation.py   # 의료 상담 흐름 / 대화 로직
│   │
│   └── patient/
│       └── patient_management.py     # 환자 정보 관리
│
├── config/
│   └── config.py               # 설정, 상수, 환경 변수
│
├── data/
│   └── docs/
│       └── ch47_hearing_loss.pdf   # 의학 문헌 (RAG 소스)
│
├── requirements.txt
└── README.md
```

## 🛠️ 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/sj-dnl/AI_medical_assistant.git
cd AI_medical_assistant
```

### 2. 필수 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. OpenAI API 키 설정

환경 변수로 설정:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

또는 `.env` 파일 생성:

```bash
# .env 파일 생성
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 4. PDF 문서 준비

`data/docs/` 디렉토리에 `ch47 hearing loss.pdf` 파일을 위치시키세요.

## 🚀 실행 방법

### 방법 1: 실행 스크립트 사용 (권장)

```bash
cd medical_assistant
./run.sh
```

### 방법 2: 직접 실행

```bash
cd medical_assistant
streamlit run app/streamlit_app.py
```

### 방법 3: 프로젝트 루트에서 실행

```bash
cd medical_assistant
python -m streamlit run app/streamlit_app.py
```

브라우저에서 자동으로 열립니다 (기본: http://localhost:8501)

**중요**: 실행 전에 `OPENAI_API_KEY` 환경 변수가 설정되어 있어야 합니다.

## 💡 사용 방법

1. **상담 시작**: 앱이 실행되면 자동으로 상담이 시작됩니다
2. **정보 입력**: 의사의 질문에 답변하며 증상을 설명합니다
3. **정보 확인**: 왼쪽 사이드바에서 수집된 정보를 실시간으로 확인
4. **진단 보고서**: 충분한 정보가 수집되면 진단 보고서 생성
5. **차트 저장**: 상담 종료 후 환자 차트를 저장/다운로드

## 🔧 설정 변경

`config/config.py`에서 다음 설정을 변경할 수 있습니다:

- `GPT_MODEL`: 사용할 GPT 모델 (기본: "gpt-4o")
- `CHUNK_SIZE`: 문서 분할 크기
- `RETRIEVER_K`: 검색할 문서 개수
- `DOCTOR_SYSTEM_PROMPT`: 의사 AI 프롬프트

## ⚠️ 주의사항

⚠️ **이 시스템은 보조 도구이며, 실제 의사의 진찰을 대체할 수 없습니다.**

- 정확한 진단을 위해서는 전문의의 진료가 필요합니다.
- 응급 상황이라고 판단되면 즉시 병원을 방문하세요.
- 온라인 상담의 한계를 인지하고 사용하세요.

## 📄 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.

## 🤝 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.

## 📚 참고

- RAG(Retrieval-Augmented Generation) 기술을 활용한 의료 상담 시스템
- OpenAI GPT-4o 모델 사용
- Streamlit 기반 웹 인터페이스
