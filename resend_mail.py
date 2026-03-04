import os
import resend
from supabase_client import supabase
from threading import Thread
from dotenv import load_dotenv
import time

load_dotenv()

class ResendMail:
    def __init__(self):
        resend.api_key = os.getenv("RESEND_API_KEY")
        self.sender = os.getenv("RESEND_SENDER")

    # send function
    def _send(self, subject, recipients, content, content_type='text'):
        try:
            for recipient in recipients:
                email_data = {
                    "from": self.sender,
                    "to": [recipient],
                    "subject": subject
                }
                if content_type=='html':
                    email_data['html'] = content
                else:
                    email_data['text'] = content
                    
                response = resend.Emails.send(email_data)
                time.sleep(5) # 5 seconds delay
        except Exception as e:
            return f"Email Error: {str(e)}"

    # Background wrapper function
    def send_email_background(self, subject, recipients, content, content_type='text'):
        thread = Thread(
            target=self._send,
            args=(subject, recipients, content, content_type)
        )
        thread.start()

class LoadEmailIds:
  def __init__(self):
    response = supabase.table('users').select('*').execute()
    if response.data:
      self.recipients = [user['email'] for user in response.data]

  def get_all_recipients(self):
    return self.recipients
