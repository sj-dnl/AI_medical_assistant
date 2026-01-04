"""
환자 정보 관리 모듈
"""

import json
from datetime import datetime
from typing import Dict, Any


def initialize_patient_info() -> Dict[str, Any]:
    """환자 정보 초기화"""
    return {
        "patient_id": f"P{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "basic_info": {
            "name": None,
            "age": None,
            "gender": None
        },
        "chief_complaint": None,  # 주 증상
        "symptoms": [],  # 증상 리스트
        "symptom_details": {  # 증상 상세 정보
            "onset": None,  # 발병 시기
            "duration": None,  # 지속 기간
            "severity": None,  # 심각도
            "affected_side": None,  # 영향받은 쪽 (편측/양측)
            "progression": None,  # 진행 양상 (갑작스러운/점진적)
        },
        "medical_history": [],  # 병력
        "family_history": [],  # 가족력
        "medications": [],  # 복용 약물
        "additional_symptoms": [],  # 추가 증상 (이명, 어지러움 등)
        "lifestyle": {  # 생활습관
            "noise_exposure": None,
            "occupation": None
        },
        "suspected_diagnosis": [],  # 의심 질환
        "differential_diagnosis": [],  # 감별 진단
        "conversation_history": []  # 대화 기록
    }


def extract_patient_info(conversation_history: list, patient_info: Dict[str, Any], client) -> Dict[str, Any]:
    """
    대화 내용을 분석하여 환자 정보 자동 추출
    
    Args:
        conversation_history: 대화 기록
        patient_info: 현재 환자 정보
        client: OpenAI 클라이언트
        
    Returns:
        업데이트된 환자 정보
    """
    if len(conversation_history) < 2:
        return patient_info
    
    # 최근 대화 내용 추출
    recent_conversation = "\n".join([
        f"{msg['role']}: {msg['content']}" 
        for msg in conversation_history[-4:]
    ])
    
    extraction_prompt = f"""
다음 대화에서 환자 정보를 추출하여 JSON 형식으로 반환하세요.

대화 내용:
{recent_conversation}

추출해야 할 정보:
- 이름, 나이, 성별
- 주 증상
- 증상 발생 시기, 지속 기간
- 영향받은 부위 (왼쪽/오른쪽/양쪽)
- 심각도
- 추가 증상 (이명, 어지러움 등)
- 과거 병력
- 약물 복용

정보가 언급되지 않은 항목은 null로 반환하세요.
JSON만 반환하고 다른 텍스트는 포함하지 마세요.

형식:
{{
    "name": "이름",
    "age": 나이,
    "gender": "성별",
    "chief_complaint": "주 증상",
    "symptoms": ["증상1", "증상2"],
    "onset": "발생 시기",
    "duration": "지속 기간",
    "affected_side": "영향 부위",
    "severity": "심각도",
    "additional_symptoms": ["추가증상1"],
    "medical_history": ["병력1"],
    "progression": "진행양상"
}}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 의료 정보 추출 전문가입니다."},
                {"role": "user", "content": extraction_prompt}
            ],
            temperature=0.1
        )
        
        content = response.choices[0].message.content.strip()
        
        # JSON 파싱
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
        
        extracted_info = json.loads(content)
        
        # 환자 정보 업데이트
        if extracted_info.get('name'):
            patient_info['basic_info']['name'] = extracted_info['name']
        if extracted_info.get('age'):
            patient_info['basic_info']['age'] = extracted_info['age']
        if extracted_info.get('gender'):
            patient_info['basic_info']['gender'] = extracted_info['gender']
        if extracted_info.get('chief_complaint'):
            patient_info['chief_complaint'] = extracted_info['chief_complaint']
        if extracted_info.get('symptoms'):
            for symptom in extracted_info['symptoms']:
                if symptom not in patient_info['symptoms']:
                    patient_info['symptoms'].append(symptom)
        if extracted_info.get('onset'):
            patient_info['symptom_details']['onset'] = extracted_info['onset']
        if extracted_info.get('duration'):
            patient_info['symptom_details']['duration'] = extracted_info['duration']
        if extracted_info.get('affected_side'):
            patient_info['symptom_details']['affected_side'] = extracted_info['affected_side']
        if extracted_info.get('severity'):
            patient_info['symptom_details']['severity'] = extracted_info['severity']
        if extracted_info.get('progression'):
            patient_info['symptom_details']['progression'] = extracted_info['progression']
        if extracted_info.get('additional_symptoms'):
            for symptom in extracted_info['additional_symptoms']:
                if symptom not in patient_info['additional_symptoms']:
                    patient_info['additional_symptoms'].append(symptom)
        if extracted_info.get('medical_history'):
            for history in extracted_info['medical_history']:
                if history not in patient_info['medical_history']:
                    patient_info['medical_history'].append(history)
        
    except Exception as e:
        print(f"[정보 추출 오류: {e}]")
    
    return patient_info


def generate_patient_summary(patient_info: Dict[str, Any]) -> str:
    """환자 정보 요약 생성"""
    summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    환자 진료 차트                            ║
╠══════════════════════════════════════════════════════════════╣
║ 환자 ID: {patient_info['patient_id']}
║ 작성 일시: {patient_info['timestamp']}
╠══════════════════════════════════════════════════════════════╣
║ [기본 정보]
║ • 이름: {patient_info['basic_info'].get('name', 'N/A')}
║ • 나이: {patient_info['basic_info'].get('age', 'N/A')}세
║ • 성별: {patient_info['basic_info'].get('gender', 'N/A')}
╠══════════════════════════════════════════════════════════════╣
║ [주 증상]
║ {patient_info.get('chief_complaint', 'N/A')}
╠══════════════════════════════════════════════════════════════╣
║ [증상 상세]
║ • 발병 시기: {patient_info['symptom_details'].get('onset', 'N/A')}
║ • 지속 기간: {patient_info['symptom_details'].get('duration', 'N/A')}
║ • 심각도: {patient_info['symptom_details'].get('severity', 'N/A')}
║ • 영향 부위: {patient_info['symptom_details'].get('affected_side', 'N/A')}
║ • 진행 양상: {patient_info['symptom_details'].get('progression', 'N/A')}
╠══════════════════════════════════════════════════════════════╣
"""
    
    if patient_info['symptoms']:
        summary += "║ [주요 증상 목록]\n"
        for symptom in patient_info['symptoms']:
            summary += f"║ • {symptom}\n"
        summary += "╠══════════════════════════════════════════════════════════════╣\n"
    
    if patient_info['additional_symptoms']:
        summary += "║ [추가 증상]\n"
        for symptom in patient_info['additional_symptoms']:
            summary += f"║ • {symptom}\n"
        summary += "╠══════════════════════════════════════════════════════════════╣\n"
    
    if patient_info['medical_history']:
        summary += "║ [과거 병력]\n"
        for history in patient_info['medical_history']:
            summary += f"║ • {history}\n"
        summary += "╠══════════════════════════════════════════════════════════════╣\n"
    
    if patient_info['suspected_diagnosis']:
        summary += "║ [의심 질환]\n"
        for i, diagnosis in enumerate(patient_info['suspected_diagnosis'], 1):
            summary += f"║ {i}. {diagnosis}\n"
        summary += "╠══════════════════════════════════════════════════════════════╣\n"
    
    summary += "╚══════════════════════════════════════════════════════════════╝"
    
    return summary


def save_patient_chart(patient_info: Dict[str, Any], filename: str = None) -> str:
    """환자 차트를 JSON 파일로 저장"""
    if filename is None:
        filename = f"patient_chart_{patient_info['patient_id']}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(patient_info, f, ensure_ascii=False, indent=2)
    
    return filename


def get_symptoms_summary(patient_info: Dict[str, Any]) -> str:
    """환자 증상 요약 텍스트 생성"""
    symptoms_summary = f"""
환자 정보:
- 나이: {patient_info['basic_info'].get('age', 'N/A')}세
- 주 증상: {patient_info.get('chief_complaint', 'N/A')}
- 증상 목록: {', '.join(patient_info['symptoms'])}
- 발생 시기: {patient_info['symptom_details'].get('onset', 'N/A')}
- 영향 부위: {patient_info['symptom_details'].get('affected_side', 'N/A')}
- 진행 양상: {patient_info['symptom_details'].get('progression', 'N/A')}
- 추가 증상: {', '.join(patient_info['additional_symptoms'])}
"""
    return symptoms_summary

