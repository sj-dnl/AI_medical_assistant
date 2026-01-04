# 의료 상담 시스템 (Medical Assistant)

이비인후과 청각 장애 전문 상담 시스템입니다. RAG(Retrieval-Augmented Generation) 기술을 활용하여 의학 문헌 기반 상담을 제공합니다.

## 프로젝트 구조

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

## 설치 방법

1. 저장소 클론 또는 다운로드
2. 의존성 설치:
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

또는 `.env` 파일 생성:
```
OPENAI_API_KEY=your-api-key-here
```

## 실행 방법

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

**중요**: 실행 전에 `OPENAI_API_KEY` 환경 변수가 설정되어 있어야 합니다.

## 주요 기능

- **RAG 기반 상담**: PDF 의학 문헌을 기반으로 한 전문적인 상담
- **환자 정보 관리**: 대화를 통해 환자 정보 자동 추출 및 관리
- **진단 지원**: 증상 분석 및 진단 보고서 생성
- **대화형 UI**: Streamlit 기반 사용자 친화적 인터페이스

## 주의사항

⚠️ **이 시스템은 보조 도구이며, 실제 의사의 진찰을 대체할 수 없습니다.**
- 정확한 진단을 위해서는 전문의의 진료가 필요합니다.
- 응급 상황이라고 판단되면 즉시 병원을 방문하세요.

## 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.

