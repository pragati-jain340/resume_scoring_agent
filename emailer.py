import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
import logging

def create_feedback_template(name: str, score_data: dict) -> str:
    """Create a more professional email template"""
    score = score_data['score']
    feedback_items = score_data['feedback']
    
    # Determine score category
    if score >= 80:
        category = "Excellent"
        encouragement = "Your qualifications are outstanding!"
    elif score >= 60:
        category = "Good"
        encouragement = "You have strong qualifications with some room for improvement."
    else:
        category = "Needs Improvement"
        encouragement = "Consider enhancing your resume with more relevant experience and skills."
    
    # Create feedback sections
    strengths = [item for item in feedback_items if "✅" in item or "👍" in item]
    areas_for_improvement = [item for item in feedback_items if "❌" in item or "📝" in item]
    
    template = f"""
Dear {name},

Thank you for submitting your resume for evaluation. Below is your automated assessment:

🏆 **Overall Score**: {score}/100 ({category})

🔍 **Strengths**:
{'- ' + '\n- '.join(strengths) if strengths else '- No specific strengths identified'}

📌 **Areas for Improvement**:
{'- ' + '\n- '.join(areas_for_improvement) if areas_for_improvement else '- No major areas for improvement identified'}

💬 **Feedback**: {encouragement}

For any questions, please contact our HR department.

Best regards,
AI Resume Evaluation Team
"""
    return template.strip()

def send_feedback_email(to_email: str, name: str, score_data: dict) -> bool:
    """Send feedback email with improved error handling"""
    subject = "Your Resume Evaluation Results"
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        body = create_feedback_template(name, score_data)
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            logging.info(f"Email successfully sent to {to_email}")
            return True
            
    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {str(e)}")
        return False