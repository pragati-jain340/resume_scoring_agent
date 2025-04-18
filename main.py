import os
import json
import logging
from datetime import datetime
from config import RESUME_FOLDER, PROCESSED_FOLDER, OUTPUT_FOLDER, LOG_FILE, DEFAULT_EMAIL
from utils import extract_resume_data, extract_email  # Added extract_email import
from scoring import score_resume
from emailer import send_feedback_email

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def ensure_folders_exist():
    """Ensure all required folders exist"""
    for folder in [RESUME_FOLDER, PROCESSED_FOLDER, OUTPUT_FOLDER, 'logs']:
        os.makedirs(folder, exist_ok=True)

def process_resumes():
    ensure_folders_exist()
    resumes = [f for f in os.listdir(RESUME_FOLDER) if f.endswith(('.pdf', '.docx'))]
    
    if not resumes:
        logging.info("No resumes found in the folder.")
        return

    for resume in resumes:
        try:
            file_path = os.path.join(RESUME_FOLDER, resume)
            logging.info(f"Processing: {resume}")

            # Step 1: Extract data
            data = extract_resume_data(file_path)
            
            # Get and validate email
            real_email = data.get("raw_email") or extract_email(data["raw_text"]) or DEFAULT_EMAIL
            if not real_email or "@" not in real_email:
                logging.error(f"No valid email found in {resume}")
                continue

            # Step 2: Score Resume
            score_data = score_resume(data["raw_text"], data["ai_keywords"])

            # Step 3: Send Email Feedback
            send_feedback_email(
                to_email=real_email,  # Use actual email
                name=data["masked_name"],
                score_data=score_data
            )

            # Step 4: Save Output
            output_record = {
                "masked_name": data["masked_name"],
                "actual_email": real_email,  # Store actual email
                "masked_email": data["masked_email"],  # For display purposes
                "batch_year": data["batch_year"],
                "ai_keywords": data["ai_keywords"],
                "score": score_data["score"],
                "feedback": score_data["feedback"]
            }

            output_path = os.path.join(OUTPUT_FOLDER, f"{data['masked_name']}.json")
            with open(output_path, 'w') as outfile:
                json.dump(output_record, outfile, indent=4)

            # Move processed file
            processed_path = os.path.join(PROCESSED_FOLDER, resume)
            if os.path.exists(processed_path):
                os.remove(processed_path)
            os.rename(file_path, processed_path)
            
            logging.info(f"Successfully processed: {resume} | Sent to: {real_email}")

        except Exception as e:
            logging.error(f"Error processing {resume}: {str(e)}")
            # Move problematic files to error folder
            error_folder = os.path.join(RESUME_FOLDER, "errors")
            os.makedirs(error_folder, exist_ok=True)
            error_path = os.path.join(error_folder, resume)
            if os.path.exists(error_path):
                os.remove(error_path)
            os.rename(file_path, error_path)

if __name__ == "__main__":
    process_resumes()