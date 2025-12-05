"""
Smart response formatter for GST IntelliGuide
IMPORTANT: Only restructure when absolutely necessary
Most responses should be returned AS-IS from the LLM
"""
import re


def format_gst_response(raw_answer: str) -> str:
    """
    Smart formatter that PRESERVES most responses as-is.
    Only restructures truly unstructured educational content.
    
    The LLM has been prompted to format responses correctly.
    We should trust the LLM output in most cases.
    """
    
    if "**🔹" in raw_answer:
        return raw_answer
    
    if "| " in raw_answer and "|---" in raw_answer:
        return raw_answer
    
    if len(raw_answer) < 500:
        return raw_answer
    
    if re.search(r'\n\d+\.', raw_answer):
        return raw_answer
    
    if raw_answer.count('**') >= 2:
        return raw_answer
    
    if '•' in raw_answer or '- ' in raw_answer:
        return raw_answer
    
    conversation_patterns = [
        'previous question', 'you asked', 'your question', 
        'conversation', 'earlier', 'before', 'history',
        'welcome', 'hello', 'hi there', 'goodbye',
        'thank', 'glad to help', 'how can i help',
        'i\'m gst intelliguide', 'specialized in',
        'tell me more', 'continue', 'follow-up'
    ]
    lower_answer = raw_answer.lower()
    if any(pattern in lower_answer for pattern in conversation_patterns):
        return raw_answer
    

    if 'section' in lower_answer or 'cgst' in lower_answer or 'igst' in lower_answer:
        return raw_answer
    

    return raw_answer
