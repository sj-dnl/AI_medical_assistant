# AI_medical_assistant
SNU Project – AI Medical Assistant for Hearing Loss

🏥 청각 장애 전문 의료 상담 시스템
이비인후과 청각 장애 전문 AI 의료 상담 시스템입니다. RAG(Retrieval-Augmented Generation) 기술을 활용하여 의학 문헌을 기반으로 정확한 상담을 제공합니다.

✨ 주요 기능
💬 대화형 의료 상담: AI 의사와 자연스러운 대화
🔍 증상 기반 진단: 수집된 증상을 분석하여 가능한 질환 추정
📊 환자 차트 자동 생성: 대화 내용에서 정보를 자동 추출
📋 최종 진단 보고서: RAG 기반 의학 문헌 참조 진단
💾 차트 저장/다운로드: JSON 형식으로 환자 정보 저장
🛠️ 설치 방법
1. 필수 패키지 설치
pip install -r requirements.txt
2. OpenAI API 키 설정
환경 변수로 설정:

export OPENAI_API_KEY='your-api-key-here'
또는 config.py 파일에서 직접 설정:

OPENAI_API_KEY = 'your-api-key-here'
3. PDF 문서 준비
ch47 hearing loss.pdf 파일을 프로젝트 디렉토리에 위치시키세요.

🚀 실행 방법
Streamlit 앱 실행
streamlit run streamlit_app.py
브라우저에서 자동으로 열립니다 (기본: http://localhost:8501)

📁 프로젝트 구조
의사도움/
├── config.py                  # 설정 및 상수
├── rag_system.py              # RAG 시스템 모듈
├── patient_management.py      # 환자 정보 관리
├── medical_consultation.py    # 의료 상담 로직
├── streamlit_app.py          # Streamlit UI 앱
├── requirements.txt          # 패키지 의존성
├── ch47 hearing loss.pdf     # 의학 문헌 (필요)
└── README.md                 # 프로젝트 설명
💡 사용 방법
상담 시작: 앱이 실행되면 자동으로 상담이 시작됩니다
정보 입력: 의사의 질문에 답변하며 증상을 설명합니다
정보 확인: 왼쪽 사이드바에서 수집된 정보를 실시간으로 확인
진단 보고서: 충분한 정보가 수집되면 진단 보고서 생성
차트 저장: 상담 종료 후 환자 차트를 저장/다운로드
⚠️ 주의사항
이 시스템은 보조 도구입니다
정확한 진단은 실제 의사의 진찰이 필요합니다
응급 상황 시 즉시 병원을 방문하세요
온라인 상담의 한계를 인지하고 사용하세요
🔧 설정 변경
config.py에서 다음 설정을 변경할 수 있습니다:

GPT_MODEL: 사용할 GPT 모델
CHUNK_SIZE: 문서 분할 크기
RETRIEVER_K: 검색할 문서 개수
DOCTOR_SYSTEM_PROMPT: 의사 AI 프롬프트
📄 라이선스
이 프로젝트는 교육 및 연구 목적으로만 사용하세요.

🤝 기여
버그 리포트나 기능 제안은 이슈로 등록해주세요.
