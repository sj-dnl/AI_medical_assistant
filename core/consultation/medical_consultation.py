"""
의료 상담 로직 모듈
"""

from openai import OpenAI
from datetime import datetime
from typing import Dict, Any, List
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.config import DOCTOR_SYSTEM_PROMPT, GPT_MODEL, OPENAI_API_KEY
from core.patient.patient_management import extract_patient_info, get_symptoms_summary
from core.rag.rag_system import RAGSystem


class MedicalConsultation:
    """의료 상담 클래스"""
    
    def __init__(self, rag_system: RAGSystem):
        """
        의료 상담 초기화
        
        Args:
            rag_system: RAG 시스템 인스턴스
        """
        self.rag_system = rag_system
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = [{"role": "system", "content": DOCTOR_SYSTEM_PROMPT}]
        self.diagnosis_stage = False
        
    def get_initial_greeting(self) -> str:
        """초기 인사말 반환"""
        return """안녕하세요, 환자분. 저는 이비인후과 전문의입니다. 
오늘 어떤 증상으로 방문하셨나요? 편하게 말씀해 주세요.

먼저 기본적인 정보를 여쭤봐도 될까요?
성함과 나이, 성별을 알려주시겠어요?"""
    
    def process_user_message(
        self, 
        user_input: str, 
        patient_info: Dict[str, Any],
        conversation_count: int
    ) -> tuple[str, Dict[str, Any], bool]:
        """
        사용자 메시지 처리 및 응답 생성
        
        Args:
            user_input: 사용자 입력
            patient_info: 환자 정보
            conversation_count: 대화 횟수
            
        Returns:
            tuple: (의사 응답, 업데이트된 환자 정보, 진단 단계 여부)
        """
        # 사용자 메시지 추가
        self.messages.append({"role": "user", "content": user_input})
        patient_info['conversation_history'].append({
            "role": "patient",
            "content": user_input,
            "timestamp": datetime.now().strftime('%H:%M:%S')
        })
        
        # 정보 자동 추출
        patient_info = extract_patient_info(
            self.messages, 
            patient_info, 
            self.client
        )
        
        # 충분한 정보가 수집되었는지 확인하여 진단 단계로 전환
        if (not self.diagnosis_stage and 
            patient_info['chief_complaint'] and 
            patient_info['symptoms'] and
            len(patient_info['symptoms']) >= 2 and
            conversation_count >= 3):
            
            # RAG로 진단 정보 가져오기
            symptoms_summary = get_symptoms_summary(patient_info)
            diagnosis_result = self.rag_system.get_symptoms_analysis(symptoms_summary)
            diagnosis_text = diagnosis_result['answer']
            
            # AI에게 진단 결과를 컨텍스트로 제공
            context_message = f"""
[의학 지식 데이터베이스 참조 결과]
{diagnosis_text}

위 정보를 바탕으로:
1. 환자의 증상과 가장 일치하는 질환을 2-3가지 제시하세요
2. 각 질환을 감별하기 위해 필요한 추가 질문을 하세요
3. 환자가 이해하기 쉽게 설명하세요
"""
            self.messages.append({"role": "system", "content": context_message})
            self.diagnosis_stage = True
        
        # AI 응답 생성
        response = self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=self.messages,
            temperature=0.7,
            max_tokens=600
        )
        
        doctor_response = response.choices[0].message.content
        
        # 대화 기록 저장
        self.messages.append({"role": "assistant", "content": doctor_response})
        patient_info['conversation_history'].append({
            "role": "doctor",
            "content": doctor_response,
            "timestamp": datetime.now().strftime('%H:%M:%S')
        })
        
        return doctor_response, patient_info, self.diagnosis_stage
    
    def generate_final_diagnosis(self, patient_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        최종 진단 보고서 생성
        
        Args:
            patient_info: 환자 정보
            
        Returns:
            진단 결과 딕셔너리
        """
        if not patient_info['chief_complaint']:
            return None
        
        # RAG 기반 진단 분석
        symptoms_summary = get_symptoms_summary(patient_info)
        diagnosis_result = self.rag_system.get_symptoms_analysis(symptoms_summary)
        
        return diagnosis_result
    
    def reset(self):
        """상담 상태 초기화"""
        self.messages = [{"role": "system", "content": DOCTOR_SYSTEM_PROMPT}]
        self.diagnosis_stage = False

