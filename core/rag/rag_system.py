"""
RAG (Retrieval-Augmented Generation) 시스템 모듈
노트북 버전과 동일하게 langchain_community 없이 구현
"""

from openai import OpenAI
import pypdf
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.config import OPENAI_API_KEY, GPT_MODEL


class RAGSystem:
    """RAG 시스템 클래스 (노트북과 동일한 방식)"""
    
    def __init__(self, pdf_path: str):
        """
        RAG 시스템 초기화
        
        Args:
            pdf_path: PDF 파일 경로
        """
        self.pdf_path = pdf_path
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.pdf_text = ""
        self.pages = []
        
    def load_and_build(self):
        """PDF 로드 및 텍스트 추출"""
        # PDF 읽기
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            
            # 모든 페이지 텍스트 추출
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                self.pages.append({
                    'page_number': page_num,
                    'text': page_text
                })
                self.pdf_text += page_text + "\n\n"
        
        return len(self.pages)
    
    def query(self, query_text: str) -> dict:
        """
        RAG 쿼리 실행 (노트북의 rag_query와 동일)
        
        Args:
            query_text: 질문 텍스트
            
        Returns:
            dict: 답변, 입력, 컨텍스트 포함
        """
        if not self.pdf_text:
            raise ValueError("RAG 시스템이 초기화되지 않았습니다. load_and_build()를 먼저 실행하세요.")
        
        # 1. 컨텍스트로 전체 PDF 텍스트 사용 (간단한 구현)
        context = self.pdf_text
        
        # 2. 프롬프트 생성
        system_prompt = f"""당신은 청각 장애(hearing loss) 전문 의료 지식 어시스턴트입니다. 
제공된 의학 문헌을 바탕으로 정확하고 전문적인 답변을 제공하세요. 
답변은 명확하고 이해하기 쉽게 작성하되, 의학 용어가 필요한 경우 설명을 덧붙이세요.

참고 문헌:
{context}
"""
        
        # 3. LLM 호출
        response = self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query_text}
            ],
            temperature=0.3
        )
        
        answer = response.choices[0].message.content
        
        # 4. 결과 반환
        return {
            "input": query_text,
            "answer": answer,
            "context": self.pages  # 페이지 정보 반환
        }
    
    def get_symptoms_analysis(self, symptom_description: str) -> dict:
        """증상 분석 (RAG 쿼리)"""
        query = f"다음 증상과 관련된 청각 장애 유형, 원인, 그리고 관련 질환을 알려주세요: {symptom_description}"
        return self.query(query)
    
    def get_disease_info(self, disease_name: str) -> dict:
        """질병 정보 조회"""
        query = f"{disease_name}에 대해 설명해주세요. 증상, 원인, 진단 방법, 치료법을 포함해주세요."
        return self.query(query)
    
    def get_differential_diagnosis_questions(self, suspected_diseases: list) -> dict:
        """감별 진단 질문 생성"""
        diseases_str = ", ".join(suspected_diseases)
        query = f"다음 질환들을 감별하기 위해 환자에게 물어봐야 할 중요한 질문들을 알려주세요: {diseases_str}"
        return self.query(query)

