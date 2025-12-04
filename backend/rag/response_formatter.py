"""
Format LLM responses into structured GST format
"""
import re


def format_gst_response(raw_answer: str) -> str:
    """
    Ensure the response follows the 5-section structured format.
    If already formatted, return as-is. Otherwise, intelligently restructure.
    """
    
    # Check if already has the emoji header format
    if "**🔹 Meaning" in raw_answer and "**🔹 Key Takeaway" in raw_answer:
        return raw_answer
    
    # If not formatted, parse and restructure intelligently
    lines = [line.strip() for line in raw_answer.split('\n') if line.strip()]
    
    # Try to extract meaningful content
    definition = []
    applies = []
    rules = []
    example = []
    takeaway = []
    
    current_section = definition
    
    for line in lines:
        # Detect section changes based on keywords
        lower = line.lower()
        
        if any(word in lower for word in ['definition', 'meaning', 'what is', 'refers to']):
            current_section = definition
        elif any(word in lower for word in ['applies', 'when', 'used for', 'applicable']):
            current_section = applies
        elif any(word in lower for word in ['rule', 'condition', 'limitation', 'section', 'requirement']):
            current_section = rules
        elif any(word in lower for word in ['example', 'instance', 'scenario', 'case']):
            current_section = example
        elif any(word in lower for word in ['takeaway', 'summary', 'conclusion', 'key point']):
            current_section = takeaway
        else:
            current_section.append(line)
    
    # Build structured response
    formatted = "**🔹 Meaning / Definition**\n"
    if definition:
        for item in definition[:3]:  # Max 3 points
            formatted += f"• {item}\n"
    else:
        formatted += f"• {lines[0] if lines else 'Information not available'}\n"
    
    formatted += "\n**🔹 When it Applies**\n"
    if applies:
        for item in applies[:4]:
            formatted += f"• {item}\n"
    else:
        formatted += "• Refer to context provided in GST documents\n"
    
    formatted += "\n**🔹 Rules / Conditions**\n"
    if rules:
        for item in rules[:5]:
            formatted += f"• {item}\n"
    else:
        formatted += "• See detailed information above\n"
    
    formatted += "\n**🔹 Example**\n"
    if example:
        for item in example[:4]:
            formatted += f"• {item}\n"
    else:
        formatted += "• Practical application depends on specific business scenario\n"
    
    formatted += "\n**🔹 Key Takeaway**\n"
    if takeaway:
        formatted += f"• {takeaway[0]}\n"
    elif lines:
        formatted += f"• {lines[-1]}\n"
    else:
        formatted += "• Refer to GST Act for complete details\n"
    
    # Append original response for reference
    formatted += f"\n---\n**Detailed Information:**\n{raw_answer}"
    
    return formatted
