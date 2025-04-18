# config.py
import os

# Get the directory where config.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RESUME_FOLDER = os.path.join(BASE_DIR, "resumes")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")
LOG_FILE = os.path.join(BASE_DIR, "logs", "process_log.txt")

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"  # Replace with your email
SENDER_PASSWORD = "your_app_password"  # Replace with app password
DEFAULT_EMAIL = "backup@email.com"     # Replace with backup email