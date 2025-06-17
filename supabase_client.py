from supabase import create_client, Client
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANNON_KEY = os.getenv('SUPABASE_ANNON_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANNON_KEY)
admin = {
  'first_name':'Shailesh',
  'last_name':'Vishwakarma',
  'phone':9454147438,
  'email':'shailvestein.careers@gmail.com',
  'password':generate_password_hash('9454147438', method='scrypt'),
  'role':'admin'
  }
try:
  response = supabase.table('users').select('*').limit(1).execute()
  if len(response.data) == 0:
    response = supabase.table('users').insert(admin).execute()
    print(f"Admin added to database.")
  # response = supabase.table('users').select('*').limit(1).execute()
  # print(f"Connection successfull!\nResponse: {response}")
except Exception as e:
  print(f'Connection failed.\nerror {e} occurred!')
