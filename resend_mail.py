import os
import resend

class ResendMail:
    def __init__(self):
        resend.api_key = os.getenv("RESEND_API_KEY")
        self.sender = os.getenv("RESEND_SENDER")

    def send_text_email(self, subject, recipients, body):
        try:
            response = resend.Emails.send({
                "from": self.sender,
                "to": recipients,
                "subject": subject,
                "text": body
            })
            return response
        except Exception as e:
            return str(e)

    def send_html_email(self, subject, recipients, html_content):
        try:
            response = resend.Emails.send({
                "from": self.sender,
                "to": recipients,
                "subject": subject,
                "html": html_content
            })
            return response
        except Exception as e:
            return str(e)
