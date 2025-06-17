from flask_mail import Mail, Message
from flask import render_template
from supabase_client import supabase
from dotenv import load_dotenv
import os

load_dotenv()

class SendMail:
  def __init__(self, app):
    # self.msg = Message()
    self.app = app
    
    # Configure mail settings
    self.app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')  # Or your provider's SMTP
    self.app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    self.app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    self.app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
    self.app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    self.app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') # NOT your Gmail password
    self.app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    self.mail = Mail(self.app)

  def send_customized_email(self, subject, recipients, body):
      try:
        msg = Message(
            subject=subject,
            recipients=recipients,  # List of recipients
            body=body
        )
        self.mail.send(msg)
        return "Email sent!"
      except Exception as e:
        return f"Error {e} occurred!"
  
  def send_email_with_rendered_html(self, subject, recipients, html_filepath, contents):
    try:
      msg = Message(subject,
                        recipients)
      msg.html = render_template(html_filepath, contents=contents)
      self.mail.send(msg)
      return f"Email sent!"
    except Exception as e:
      return f"Error {e} occurred!"
    
class LoadEmailIds:
  def __init__(self):
    response = supabase.table('users').select('*').execute()
    if response.data:
      self.recipients = [user['email'] for user in response.data]

  def get_all_recipients(self):
    return self.recipients
