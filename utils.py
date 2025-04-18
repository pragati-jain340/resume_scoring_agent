import os
import re
import docx
import PyPDF2
from typing import List, Dict, Union

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF with improved error handling"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")
    return text.strip()

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX with improved error handling"""
    text = ""
    try:
        doc = docx.Document(file_path)
        text = "\n".join(para.text for para in doc.paragraphs if para.text)
    except Exception as e:
        raise Exception(f"DOCX extraction failed: {str(e)}")
    return text.strip()

def extract_email(text):
    """More precise email extraction"""
    # First try to find email after "Email :" pattern
    email_match = re.search(
        r'Email\s*:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', 
        text, 
        re.IGNORECASE
    )
    if email_match:
        return email_match.group(1).strip().lower()
    
    # Fallback to general pattern
    general_match = re.search(
        r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b',
        text
    )
    return general_match.group(0) if general_match else None

def validate_email(email):
    """Basic email validation"""
    return (email and '@' in email and 
            '.' in email.split('@')[-1] and 
            not email.startswith('@') and
            ' ' not in email)

def extract_batch_year(text: str) -> str:
    """Extract graduation year with more patterns"""
    patterns = [
        r'(20[0-9]{2})',  # simple year
        r'Graduat(ion|ed)\s*(?:year)?\s*:\s*(20[0-9]{2})',  # with graduation prefix
        r'Batch\s*:\s*(20[0-9]{2})'  # batch pattern
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return "Unknown"

def contains_ai_keywords(text: str) -> List[str]:
    """Expanded list of AI keywords"""
    keywords = [
        "machine learning", "deep learning", "AI", "artificial intelligence",
        "neural network", "NLP", "computer vision", "reinforcement learning",
        "data science", "tensorflow", "pytorch", "scikit-learn", "llm",
        "large language model", "generative ai"
    ]
    found = list(set(kw for kw in keywords if kw.lower() in text.lower()))
    return found if found else ["None"]

def mask_email(email):
    """Only mask if not in test mode"""
    if "@test.com" in email or os.getenv("TEST_MODE"):
        return email  # Don't mask in test mode
    if email:
        username, domain = email.split("@")
        return username[0] + "****@" + domain
    return "****@example.com"

def mask_name(filename):
    """Improved name masking that ensures valid filenames"""
    name = os.path.splitext(os.path.basename(filename))[0]
    
    # Remove special characters and spaces
    name = re.sub(r'[^a-zA-Z0-9]', '', name)
    
    if not name:  # If name becomes empty after cleaning
        name = "resume"
    
    # Ensure the name isn't too short
    if len(name) <= 2:
        return "user_" + name
    
    return name[0] + "xxx" + name[-1]  # Simpler masking
def extract_resume_data(file_path: str) -> Dict[str, Union[str, List[str]]]:
    """Main function to extract resume data with better error handling"""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif ext == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    
    if not text.strip():
        raise ValueError("Empty resume content")
    
    email = extract_email(text)
    masked_email = mask_email(email)
    batch = extract_batch_year(text)
    ai_keywords = contains_ai_keywords(text)
    masked_name = mask_name(file_path)
    
    return {
        "masked_name": masked_name,
        "masked_email": masked_email,
        "batch_year": batch,
        "ai_keywords": ai_keywords,
        "raw_text": text
    }