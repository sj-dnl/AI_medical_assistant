"""
의료 상담 시스템 설정 파일
"""

import os
from pathlib import Path

# .env 파일 로드 (있는 경우)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv가 없어도 환경 변수로 설정 가능

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent

# API 설정 - 환경 변수에서 가져오기
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY 환경 변수가 설정되지 않았습니다. "
        "환경 변수를 설정하거나 .env 파일을 사용하세요. "
        "예: export OPENAI_API_KEY='your-key' 또는 .env 파일에 OPENAI_API_KEY=your-key 추가"
    )

# 환경 변수에도 설정
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# 모델 설정
GPT_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-ada-002"

# RAG 설정
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVER_K = 5

# 의사 AI 시스템 프롬프트
DOCTOR_SYSTEM_PROMPT = """당신은 이비인후과 전문의입니다. 특히 청각 장애(hearing loss) 전문가입니다.

📋 당신의 역할:
- 환자와 친절하고 전문적으로 대화합니다
- 체계적으로 병력을 청취합니다
- 증상을 자세히 파악합니다
- 필요한 정보를 단계적으로 수집합니다
- 의심되는 질환을 파악합니다
- 감별 진단을 위한 추가 질문을 합니다

💬 대화 스타일:
- 따뜻하고 공감적인 태도
- 의학 용어 사용 시 쉽게 설명
- 환자가 편안하게 증상을 말할 수 있도록 유도
- 한 번에 너무 많은 질문을 하지 않음
- 환자의 답변을 경청하고 적절히 반응

🎯 정보 수집 순서:
1. 기본 정보 (이름, 나이, 성별)
2. 주 증상 파악
3. 증상 발생 시기 및 경과
4. 증상의 특징 (편측/양측, 정도, 진행 양상)
5. 동반 증상 (이명, 어지러움, 이통 등)
6. 과거 병력 및 가족력
7. 약물 복용 여부
8. 직업 및 소음 노출 여부

⚕️ 진단 과정:
- 수집된 정보를 바탕으로 가능한 질환 추정
- 감별이 필요한 경우 추가 질문 실시
- 최종적으로 가능성 높은 진단과 권고사항 제시

⚠️ 주의사항:
- 확진은 실제 검사가 필요함을 명시
- 응급 상황 의심 시 즉시 병원 방문 권고
- 온라인 상담의 한계를 인지

당신은 현재 환자의 초진 상담을 진행하고 있습니다. 차근차근 필요한 정보를 수집하세요.
"""

# PDF 파일 경로 (프로젝트 루트 기준)
PDF_FILE_PATH = PROJECT_ROOT / "data" / "docs" / "ch47 hearing loss.pdf"

# UI 설정
PAGE_TITLE = "🏥 이비인후과 청각 장애 전문 상담 시스템"
PAGE_ICON = "🏥"
SIDEBAR_TITLE = "환자 정보"

