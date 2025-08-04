# triage_questions.py

"""
This file defines the structured flow of triage questions.
Each dictionary key is a unique question ID.
- 'question': The text displayed to the user.
- 'type': The expected answer format ('open-text', 'multiple-choice').
- 'next_question_logic': Determines the next question ID based on the answer.
    - For 'open-text', it's usually a single next step.
    - For 'multiple-choice', it maps specific answers to the next step.
"""

TRIAGE_FLOW = {
    'start': {
        'question': "Hello! I'm here to ask a few preliminary questions. To begin, please tell me your main symptom in a few words (e.g., 'headache', 'stomach pain', 'cough').",
        'type': 'open-text',
        'next_question_logic': 'duration'
    },
    'duration': {
        'question': "Thank you. How long have you been experiencing this symptom?",
        'type': 'open-text',
        'next_question_logic': 'severity'
    },
    'severity': {
        'question': "On a scale of 1 to 10, with 10 being the most severe, how would you rate your discomfort?",
        'type': 'multiple-choice',
        'options': ['1-3 (Mild)', '4-6 (Moderate)', '7-10 (Severe)'],
        'next_question_logic': {
            '1-3 (Mild)': 'mild_follow_up',
            '4-6 (Moderate)': 'moderate_follow_up',
            '7-10 (Severe)': 'severe_follow_up'
        }
    },
    'severe_follow_up': {
        'question': "Given the severity, I recommend seeking medical attention promptly. Please contact your doctor or visit the nearest urgent care center. Is there anything else I can help you document?",
        'type': 'open-text',
        'next_question_logic': 'final_summary'
    },
    'moderate_follow_up': {
        'question': "Thank you. Please monitor your symptoms closely. If they worsen, consider contacting a healthcare provider. Is there anything else you'd like to add?",
        'type': 'open-text',
        'next_question_logic': 'final_summary'
    },
    'mild_follow_up': {
        'question': "Okay. For mild symptoms, rest and hydration can be helpful. Please consult a doctor if the symptom persists or worsens. Is there anything else I can add?",
        'type': 'open-text',
        'next_question_logic': 'final_summary'
    },
    'final_summary': {
        'question': "Thank you. I have recorded your responses. A healthcare professional will review this information shortly. This concludes our session.",
        'type': 'final',
        'next_question_logic': None
    }
}