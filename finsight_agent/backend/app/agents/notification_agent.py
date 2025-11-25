from ..tools import email_service

def get_notification_agent(to_address: str, subject: str, body: str):
    """
    Agent responsible for sending notifications.
    This agent directly calls the email_service tool.
    """
    print(f"Sending report to {to_address}...")
    result = email_service.send_email(to_address, subject, body)
    return result

if __name__ == '__main__':
    # Example usage (requires email environment variables to be set)
    # Make sure to set the email environment variables
    import os
    if os.getenv("EMAIL_HOST"):
        report_content = "This is a sample financial report."
        result = get_notification_agent(
            to_address="user@example.com",
            subject="Your FinSight Financial Report",
            body=report_content
        )
        print(result)
    else:
        print("Please set the email environment variables to test the notification agent.")
