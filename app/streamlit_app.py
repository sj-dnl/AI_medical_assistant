"""
Streamlit 의료 상담 앱
"""

import streamlit as st
import os
import sys
from datetime import datetime
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.config import (
    PAGE_TITLE,
    PAGE_ICON,
    SIDEBAR_TITLE,
    PDF_FILE_PATH,
    OPENAI_API_KEY
)
from core.rag.rag_system import RAGSystem
from core.patient.patient_management import (
    initialize_patient_info,
    generate_patient_summary,
    save_patient_chart
)
from core.consultation.medical_consultation import MedicalConsultation


# 페이지 설정
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
    }
    .doctor-message {
        background-color: #f1f8e9;
        margin-right: 2rem;
    }
    .info-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """세션 상태 초기화"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    
    if 'patient_info' not in st.session_state:
        st.session_state.patient_info = initialize_patient_info()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'consultation' not in st.session_state:
        st.session_state.consultation = None
    
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0
    
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    
    if 'diagnosis_generated' not in st.session_state:
        st.session_state.diagnosis_generated = False


def initialize_rag_system():
    """RAG 시스템 초기화"""
    if st.session_state.rag_system is None:
        with st.spinner('📄 PDF 문서 로딩 및 RAG 시스템 구축 중...'):
            try:
                # PDF_FILE_PATH가 Path 객체인 경우 문자열로 변환
                pdf_path = str(PDF_FILE_PATH) if isinstance(PDF_FILE_PATH, Path) else PDF_FILE_PATH
                rag = RAGSystem(pdf_path)
                num_pages = rag.load_and_build()
                st.session_state.rag_system = rag
                st.session_state.consultation = MedicalConsultation(rag)
                st.session_state.initialized = True
                
                # 초기 인사말 추가
                greeting = st.session_state.consultation.get_initial_greeting()
                st.session_state.chat_history.append({
                    "role": "doctor",
                    "content": greeting
                })
                
                st.success(f'✅ RAG 시스템 구축 완료! ({num_pages} 페이지 로드됨)')
                return True
            except Exception as e:
                st.error(f'❌ 오류 발생: {e}')
                pdf_path = str(PDF_FILE_PATH) if isinstance(PDF_FILE_PATH, Path) else PDF_FILE_PATH
                st.error('PDF 파일 경로를 확인해주세요: ' + pdf_path)
                return False
    return True


def display_chat_history():
    """채팅 기록 표시"""
    for message in st.session_state.chat_history:
        if message['role'] == 'doctor':
            with st.chat_message("assistant", avatar="👨‍⚕️"):
                st.markdown(message['content'])
        else:
            with st.chat_message("user", avatar="🗣️"):
                st.markdown(message['content'])


def display_patient_info_sidebar():
    """사이드바에 환자 정보 표시"""
    st.sidebar.title(SIDEBAR_TITLE)
    
    patient_info = st.session_state.patient_info
    
    # 기본 정보
    st.sidebar.subheader("📋 기본 정보")
    name = patient_info['basic_info'].get('name', 'N/A')
    age = patient_info['basic_info'].get('age', 'N/A')
    gender = patient_info['basic_info'].get('gender', 'N/A')
    
    st.sidebar.text(f"이름: {name}")
    st.sidebar.text(f"나이: {age}")
    st.sidebar.text(f"성별: {gender}")
    
    st.sidebar.divider()
    
    # 주 증상
    st.sidebar.subheader("🩺 주 증상")
    chief_complaint = patient_info.get('chief_complaint', 'N/A')
    st.sidebar.text(chief_complaint if chief_complaint else '아직 파악되지 않음')
    
    st.sidebar.divider()
    
    # 증상 목록
    if patient_info['symptoms']:
        st.sidebar.subheader("📝 증상 목록")
        for symptom in patient_info['symptoms']:
            st.sidebar.text(f"• {symptom}")
        st.sidebar.divider()
    
    # 대화 통계
    st.sidebar.subheader("📊 상담 통계")
    st.sidebar.text(f"대화 횟수: {st.session_state.conversation_count}")
    st.sidebar.text(f"수집된 증상: {len(patient_info['symptoms'])}개")
    
    st.sidebar.divider()
    
    # 상담 재시작 버튼
    if st.sidebar.button("🔄 상담 재시작"):
        st.session_state.patient_info = initialize_patient_info()
        st.session_state.chat_history = []
        st.session_state.conversation_count = 0
        st.session_state.diagnosis_generated = False
        if st.session_state.consultation:
            st.session_state.consultation.reset()
            greeting = st.session_state.consultation.get_initial_greeting()
            st.session_state.chat_history.append({
                "role": "doctor",
                "content": greeting
            })
        st.rerun()


def display_diagnosis_section():
    """진단 섹션 표시"""
    st.sidebar.divider()
    st.sidebar.subheader("📋 최종 진단")
    
    patient_info = st.session_state.patient_info
    
    # 진단 생성 조건 확인
    can_generate = (
        patient_info['chief_complaint'] and 
        len(patient_info['symptoms']) >= 2
    )
    
    if can_generate:
        if st.sidebar.button("📊 최종 진단 보고서 생성"):
            with st.spinner('🔍 진단 분석 중...'):
                try:
                    diagnosis_result = st.session_state.consultation.generate_final_diagnosis(
                        patient_info
                    )
                    
                    if diagnosis_result:
                        st.session_state.diagnosis_result = diagnosis_result
                        st.session_state.diagnosis_generated = True
                        st.rerun()
                except Exception as e:
                    st.error(f'오류 발생: {e}')
    else:
        st.sidebar.info("최소 2개 이상의 증상이 수집되어야 진단 보고서를 생성할 수 있습니다.")


def display_diagnosis_report():
    """진단 보고서 표시"""
    if st.session_state.diagnosis_generated and 'diagnosis_result' in st.session_state:
        st.header("📋 최종 진단 보고서")
        
        # 환자 차트
        st.subheader("환자 진료 차트")
        summary = generate_patient_summary(st.session_state.patient_info)
        st.code(summary, language=None)
        
        # 진단 분석 결과
        st.subheader("진단 분석 결과")
        diagnosis_result = st.session_state.diagnosis_result
        st.info(diagnosis_result['answer'])
        
        # 참고 문헌
        st.subheader("📚 참고 문헌 (PDF 출처)")
        context = diagnosis_result['context']
        
        # context가 리스트인 경우 (rag_system.py의 pages)
        if context and isinstance(context, list):
            if isinstance(context[0], dict):
                # 딕셔너리 형태 (우리가 수정한 버전)
                for i, page_info in enumerate(context[:3], 1):
                    page_num = page_info.get('page_number', i-1)
                    text = page_info.get('text', '')
                    with st.expander(f"참고 문헌 [{i}] - 페이지 {page_num}"):
                        st.text(text[:500] + "..." if len(text) > 500 else text)
            else:
                # Document 객체 형태 (원래 버전)
                for i, doc in enumerate(context[:3], 1):
                    with st.expander(f"참고 문헌 [{i}] - 페이지 {doc.metadata.get('page', i-1)}"):
                        st.text(doc.page_content[:500] + "...")
        
        # 권고사항
        st.subheader("⚕️ 권고사항")
        st.warning("""
1. 정확한 진단을 위해 이비인후과 전문의 진료를 받으세요
2. 청력 검사(순음청력검사, 어음청력검사)가 필요할 수 있습니다
3. 필요시 영상 검사(CT, MRI)가 권장될 수 있습니다
4. 증상이 악화되거나 갑작스러운 변화가 있으면 즉시 병원을 방문하세요
        """)
        
        # 차트 다운로드
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 차트 저장"):
                try:
                    filename = save_patient_chart(st.session_state.patient_info)
                    st.success(f'✅ 차트가 저장되었습니다: {filename}')
                except Exception as e:
                    st.error(f'저장 오류: {e}')
        
        with col2:
            # JSON 다운로드 버튼
            import json
            chart_json = json.dumps(
                st.session_state.patient_info, 
                ensure_ascii=False, 
                indent=2
            )
            st.download_button(
                label="📥 JSON 다운로드",
                data=chart_json,
                file_name=f"patient_chart_{st.session_state.patient_info['patient_id']}.json",
                mime="application/json"
            )


def main():
    """메인 앱"""
    initialize_session_state()
    
    # 헤더
    st.markdown(f'<div class="main-header">{PAGE_TITLE}</div>', unsafe_allow_html=True)
    
    # 경고 메시지
    st.markdown("""
    <div class="warning-box">
        ⚠️ <b>주의사항</b><br>
        이것은 보조 도구이며, 정확한 진단은 실제 의사의 진찰이 필요합니다.
        응급 상황이라고 판단되면 즉시 병원을 방문하세요.
    </div>
    """, unsafe_allow_html=True)

    # API 키 확인 (config.py에서 이미 검증되지만, 사용자 친화적 메시지 표시)
    try:
        api_key = OPENAI_API_KEY
        if not api_key:
            st.error("❌ OpenAI API 키가 설정되지 않았습니다.")
            st.info("""
            **설정 방법:**
            1. 환경 변수 설정: `export OPENAI_API_KEY='your-api-key'`
            2. .env 파일 생성: 프로젝트 루트에 `.env` 파일을 만들고 `OPENAI_API_KEY=your-api-key` 추가
            """)
            st.stop()
    except ValueError as e:
        st.error(f"❌ 설정 오류: {e}")
        st.stop()
    
    # RAG 시스템 초기화
    if not st.session_state.initialized:
        if not initialize_rag_system():
            st.stop()
    
    # 사이드바 - 환자 정보
    display_patient_info_sidebar()
    display_diagnosis_section()
    
    # 메인 컨텐츠
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 상담 대화")
        
        # 채팅 기록 표시
        display_chat_history()
        
        # 사용자 입력
        user_input = st.chat_input("증상이나 답변을 입력하세요...")
        
        if user_input:
            # 사용자 메시지 표시
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            with st.spinner('👨‍⚕️ 의사 선생님이 생각 중...'):
                try:
                    # 의사 응답 생성
                    doctor_response, updated_patient_info, diagnosis_stage = \
                        st.session_state.consultation.process_user_message(
                            user_input,
                            st.session_state.patient_info,
                            st.session_state.conversation_count
                        )
                    
                    # 상태 업데이트
                    st.session_state.patient_info = updated_patient_info
                    st.session_state.conversation_count += 1
                    
                    # 의사 메시지 추가
                    st.session_state.chat_history.append({
                        "role": "doctor",
                        "content": doctor_response
                    })
                    
                    # 진단 단계 진입 시 알림
                    if diagnosis_stage and st.session_state.conversation_count == 4:
                        st.info("🔍 충분한 정보가 수집되어 진단 단계로 진입했습니다.")
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f'오류 발생: {e}')
    
    with col2:
        # 진단 보고서 표시 (생성된 경우)
        if st.session_state.diagnosis_generated:
            display_diagnosis_report()
        else:
            st.info("""
            💡 **상담 진행 방법**
            
            1. 의사의 질문에 답변해주세요
            2. 증상을 자세히 설명해주세요
            3. 충분한 정보가 모이면 진단 보고서를 생성할 수 있습니다
            
            왼쪽 사이드바에서 수집된 정보를 확인할 수 있습니다.
            """)


if __name__ == "__main__":
    main()

