import smtplib
from email.mime.text import MIMEText

# Use the same credentials from your config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "jainpragati4566@gmail.com"
SENDER_PASSWORD = "gtoi wyvh lqym hnij"  # Your app password
RECIPIENT_EMAIL = "pragatijain841@gmail.com"  # Send to yourself for testing

def send_test_email():
    try:
        # Create message
        msg = MIMEText("This is a test email from your resume scanner.")
        msg['Subject'] = "Resume Scanner Test"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print("✅ Test email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")

if __name__ == "__main__":
    send_test_email()