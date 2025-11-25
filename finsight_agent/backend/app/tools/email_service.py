import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(to_address: str, subject: str, body: str):
    """
    Sends an email using SMTP.
    """
    if not all([EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD]):
        raise ValueError("Email environment variables not fully set.")

    message = MIMEMultipart()
    message["From"] = EMAIL_USER
    message["To"] = to_address
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = message.as_string()
        server.sendmail(EMAIL_USER, to_address, text)
        server.quit()
        return "Email sent successfully."
    except Exception as e:
        return f"Error sending email: {e}"

if __name__ == '__main__':
    # Example usage (requires email environment variables to be set)
    if all([EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD]):
        send_email(
            to_address="recipient@example.com",
            subject="Test Email",
            body="This is a test email from the FinSight Agent."
        )
    else:
        print("Please set the email environment variables to send a test email.")
