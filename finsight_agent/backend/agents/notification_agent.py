class NotificationAgent:
    def __init__(self):
        pass

    def run(self, report: str):
        print("--- Sending Notification ---")
        print(report)
        print("--- Notification Sent ---")
        return "Notification sent successfully."
