from flask import Flask, render_template, redirect, url_for, request, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import datetime as dt
from send_mail import SendMail, LoadEmailIds
from supabase_client import supabase
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


# # Initialize SendMail client
send_mail = SendMail(app=app)

@app.route('/')
@app.route('/home')
def home():
  return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    # login code here
    
    phone = request.form['phone']
    password = request.form['password']
    response = supabase.table('users').select('*').eq('phone', phone).execute()
    if not response.data:
      flash('User not found', 'danger')
      return redirect(url_for('login'))
    
    user = response.data[0]
    if user and len(user) and check_password_hash(user['password'], password):
      session['username'] = user['phone']
      session['role'] = user['role']
      if user['role'] == 'user':
        return redirect(url_for('user_dashboard'))
      else:
        return redirect(url_for('admin_dashboard'))
    else:
      flash('Invalid credentials', 'danger')
      return redirect(url_for('login'))
  return render_template('login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
  if 'username' in session and session['role'] == 'admin':
    response = supabase.table('users').select('*').eq('phone', session['username']).execute()
    if response.data:
      user = response.data[0]
      expenses_count = supabase.table('expenses').select('*', count='exact').eq('entry_added_by', user['first_name']).execute().count
      return render_template('admin_dashboard.html', 
                            user=user, expenses_count=expenses_count)
  if session['role'] == 'user':
    session.pop('username', None)
    flash('You are not authorized to access this admin dashboard.\nPlease login with admin credentials', 'danger')
  return redirect(url_for('login'))

@app.route('/user_dashboard')
def user_dashboard():
  if 'username' in session and session['role'] == 'user':
    response = supabase.table('users').select('*').eq('phone', session['username']).execute()
    if response.data:
      user = response.data[0]
      expenses_count = supabase.table('expenses').select('*', count='exact').eq('entry_added_by', user['first_name']).execute().count
      return render_template('user_dashboard.html', user=user, expense_count=expenses_count)
  return redirect(url_for('login'))

@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('login'))

@app.route('/generate_otp', methods=['GET', 'POST'])
def generate_otp():
    if request.method == 'POST':
      phone = request.form['registered_phone']
      phone = phone.strip()
      users = supabase.table('users').select('*').eq('phone', phone).execute()
      if not users.data:
        flash('User not found', 'danger')
        return redirect(url_for('generate_otp'))
      user = users.data[0]
      user_email = user['email']
      session['username'] = phone
      session.permanent = True
      app.permanent_session_lifetime = dt.timedelta(minutes=1)

      otp = ''
      for _ in range(6):
         otp += str(random.randint(0,9))
      session['otp'] = otp

      mail_body = f"""
      OTP for Password Reset
      Use the following OTP to reset your password: {otp}
      """
      send_mail.send_customized_email(
          subject='OTP for Password Reset',
          recipients=[user_email],
          body=mail_body
      )
      return redirect(url_for('verify_otp'))
    return render_template('generate_otp.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
  if request.method == 'POST':

    if 'otp' not in session:
      flash('OTP session expired. Please request again.', 'warning')
      return redirect(url_for('login'))

    entered_otp = request.form['requested_otp']
    if entered_otp == session['otp']:
        flash('OTP verified successfully! You can now reset your password.', 'success')
        return redirect(url_for('reset_password'))
    else:
        flash('Invalid OTP. Please try again.', 'danger')
        return redirect(url_for('verify_otp'))
  return render_template('verify_otp.html')
      
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
  if request.method == 'POST':
    if 'otp' not in session or 'username' not in session:
      flash('OTP session expired. Please request again.', 'warning')
      return redirect(url_for('login'))
    
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password != confirm_password:
      flash('Passwords do not match!', 'danger')
      return redirect(url_for('reset_password'))

    phone = session['username']
    response = supabase.table('users').select('*').eq('phone', phone).execute()
    user = response.data[0]
    hash_pwd = generate_password_hash(new_password)

    try:
      supabase.table('users').update({'password' : hash_pwd}).eq('phone', phone).execute()
      flash('Password reset successfully!', 'success')
      session.pop('otp', None)
      return redirect(url_for('login'))
    except Exception as e:
      flash(f'Error resetting password.\nPlease try again!', 'danger')
      return redirect(url_for('reset_password'))

  return render_template('reset_password.html')

@app.route('/register', methods=['GET', 'POST'])
def register():  
  if request.method == 'POST':
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone = request.form['phone']
    role = request.form['role']
    email=request.form['email']

    response = supabase.table('users').select('*').eq('phone', phone).execute()
    if response.data:
      existing_user = response.data[0]
      flash('User already exists!', 'danger')
      return redirect(url_for('register'))
    
    try:
      user = {'first_name':first_name.capitalize(),
                          'last_name':last_name.capitalize(),
                          'phone':phone,
                          'email':email.lower(),
                          'password':generate_password_hash(phone),
                          'role':role}
      response = supabase.table('users').insert(user).execute()
    except Exception as e:
      flash(f'Error registering user.\nPlease try again!', 'danger')
      return redirect(url_for('register'))
    
    flash('User registered successfully!', 'success')
    return redirect(url_for('register'))
  
  return render_template('register.html')


@app.route('/view_users')
def view_users():
  all_users = supabase.table('users').select('*').execute().data
  return render_template('view_users.html', users=all_users)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
  
  response = supabase.table('users').select('*').eq('id', user_id).execute()
  if response.data:
    user = response.data[0]
  
  if request.method == 'POST':
    user['first_name'] = request.form['first_name'].capitalize()
    user['last_name'] = request.form['last_name'].capitalize()
    user['phone'] = request.form['phone']
    user['email'] = request.form['email'].lower()
    
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password and confirm_password and password == confirm_password:
       user['password'] = generate_password_hash(password)
    else:
      flash('Passwords do not match!', 'danger')
      return redirect(url_for('edit_user', user_id=user_id))
    try:
      response = supabase.table('users').update(user).eq('id', user_id).execute()
      flash('user details updated successfully', 'success')
      return redirect(url_for('view_users'))
    except Exception as e:
      flash(f'Error updating user.\nPlease try again!', 'danger')
      return redirect(url_for('edit_user', user_id=user_id))
  return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
  
  response = supabase.table('users').select('*').eq('id', user_id).execute()
  if response.data:
    user = response.data[0]
  if user['phone'] == session['username']:
    flash('admin can not delete itself.', 'danger')
    return redirect(url_for('view_users'))
  try:
    response = supabase.table('users').delete().eq('id', user_id).execute()
    if response.data:
      flash('User deleted successfully', 'success')
      return redirect(url_for('view_users'))
    flash('Please try again!', 'danger')
  except Exception as e:
    flash('Error occurred', 'danger')
  return redirect(url_for('view_users'))

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
  response = supabase.table('users').select('*').eq('phone', session['username']).execute()
  if response.data:
    user = response.data[0] 
  if request.method == 'POST':
    print(f"Adding expense by {user['phone']} {datetime.now().time()}")
    item = request.form['item']
    price = request.form['price']
    purchasing_date = request.form['purchasing_date'] + " " + str(datetime.now().time())
    purchased_by = request.form['purchased_by']
    entry_date = datetime.now().isoformat()
    entry_added_by = user['first_name']
    purchasing_date = datetime.strptime(purchasing_date, '%Y-%m-%d %H:%M:%S.%f')
    try:
      if purchasing_date > datetime.now():
        flash('Purchase date cannot be in future', 'danger')
        return redirect(url_for('add_expense'))
      new_exp = {'item':item,
                  'price':price,
                  'purchasing_date':purchasing_date.isoformat(),
                  'purchased_by':purchased_by,
                  'entry_date':entry_date,
                  'entry_added_by':entry_added_by}
      response = supabase.table('expenses').insert(new_exp).execute()
      if response.data:
      
        # Sending   all   expenses  email 
        # once     a new    expense      added
        # Loading email ids from database #
        prev_hisab_date = supabase.table('calculations').select('*').order('id', desc=True).execute().data[0]['to_date'] 
        expenses = supabase.table('expenses').select('*').gt('entry_date', prev_hisab_date).execute().data
        records = []
        column_names = [column for column in expenses[0].keys()][1:]
        for e in expenses:
          row_record = []
          for column in column_names:
            col_val = e[column]
            row_record.append(col_val)
          records.append(row_record)
          
        recipients  = LoadEmailIds().get_all_recipients()
        subject = f"New expense record added successfully by {entry_added_by}"
        contents = dict()
        contents['table_title'] = 'All expenses after New added expense'
        contents['table_headings'] = column_names
        contents['table_contents'] = records
        send_mail.send_email_with_rendered_html(subject=subject,
                                                html_filepath = 'email_parser.html', 
                                                recipients= recipients,
                                                contents=contents)
        flash('Expense added successfully', 'success')
        return redirect(url_for('view_expense'))

    except Exception as e:
      flash(f"Error occurred in adding new expense {e}", 'danger')
    return redirect(url_for('add_expense'))
  return render_template('add_expense.html', user=user)


@app.route('/view_expense', methods=['GET', 'POST'])
def view_expense():
    # Recent calculation history
    recent_calculation_history = supabase.table('calculations').select('*').order('id', desc=True).limit(1).execute().data
    if not recent_calculation_history:
        expenses = supabase.table('expenses').select('*').execute().data
    else:
        previous_hisab_date = recent_calculation_history[0]['to_date']
        if isinstance(previous_hisab_date, datetime):
            previous_hisab_date = previous_hisab_date.isoformat()
        expenses = supabase.table('expenses').select('*').gt('purchasing_date', previous_hisab_date).order('entry_date', desc=True).execute().data

    # 🧾 Get all unique 'purchased_by' values
    all_names = sorted({'Brijesh', 'Santosh'})

    # 🎯 Filter logic (GET)
    selected_users = request.args.getlist('purchased_by')
    if selected_users:
        filtered_expenses = [exp for exp in expenses if exp['purchased_by'] in selected_users]
    else:
        filtered_expenses = expenses

    # 📤 Email send logic (POST)
    if request.method == 'POST':
        if len(filtered_expenses) == 0:
            flash("No new expenses found after hisab-done! Please add new ones.", 'danger')
            return redirect(url_for('view_expense'))
        try:
            column_names = [column for column in filtered_expenses[0].keys()][1:]
            records = []
            for e in filtered_expenses:
                row_data = []
                for column in column_names:
                    col_value = e[column]
                    row_data.append(col_value)
                records.append(row_data)
            column_names.insert(0, '#')  # Add index column
            for i, record in enumerate(records):
                record.insert(0, i + 1)


            # Emailing logic
            response = supabase.table('users').select('*').eq('phone', session['username']).execute()
            if response.data:
                recipients = [response.data[0]['email']]

            subject = f"All expenses record shared by {session['username']}"
            contents = {
                'table_title': 'सभी खर्चे',
                'table_headings': column_names,
                'table_contents': records
            }

            send_mail.send_email_with_rendered_html(subject=subject,
                                                    recipients=recipients,
                                                    contents=contents,
                                                    html_filepath='email_parser.html')
            
            flash(f"Expenses sent successfully on {recipients[0]}", 'success')

        except Exception as e:
            flash(f"Some error {e} occurred!", 'danger')

        return redirect(url_for('view_expense'))

    return render_template('view_expense.html',
                           expenses=filtered_expenses,
                           role=session['role'],
                           all_names=all_names,
                           selected_users=selected_users)


@app.route('/edit_expense/<int:expense_id>', methods=['GET','POST'])
def edit_expense(expense_id):
  users = supabase.table('users').select('*').eq('phone', session['username']).execute().data[0]
  expense = supabase.table('expenses').select('*').eq('id', expense_id).execute().data[0]
  if expense:
    previous_entry = [ 'Previous ->', 
                     expense['item'],
                     expense['price'],
                     expense['purchasing_date'],
                     expense['purchased_by'],
                     expense['entry_date'] ]
  if request.method == 'POST':
    new_item = request.form['item']
    new_price = request.form['price']
    new_purchased_by = request.form.get('purchased_by')
    new_purchasing_date = request.form['purchasing_date']

    if not new_purchased_by:
      new_purchased_by = expense['purchased_by']

    if not new_purchasing_date:
      new_purchasing_date= expense['purchasing_date']
      

    if new_item and new_price and new_purchased_by and new_purchasing_date:
      expense['item'] = new_item
      expense['price'] = new_price
      expense['purchased_by'] = new_purchased_by
      expense['purchasing_date'] = new_purchasing_date
      expense['entry_updated_by'] = users['first_name']

      # Sending email once a expense edited
      # Loading email ids from database #
      recipients  = LoadEmailIds().get_all_recipients()
      subject = f"Expense record edited successfully by {session['username']}"
      contents = dict()
      contents['table_title'] = 'New edited expense'
      contents['table_headings'] = ['#', 'item', 'price', 'purchased date', 'purchased by', 'entry recorded on']
      contents['table_contents'] = [previous_entry,
                                   ['Updated ->', new_item, new_price, new_purchasing_date, new_purchased_by, expense['entry_date']]]

    try:
      supabase.table('expenses').update(expense).eq('id', expense_id).execute()
      
      send_mail.send_email_with_rendered_html(subject=subject,
                                              html_filepath = 'email_parser.html', 
                                              recipients= recipients,
                                              contents=contents)
      
      flash('Expense updated successfully', 'success')
      return redirect(url_for('view_expense'))
    except Exception as e:
      flash('Error occurred in updating!', 'danger')
    return redirect(url_for('edit_expense', expense_id=expense.id))
  return render_template('edit_expense.html', expense=expense)

@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
  
  expense = supabase.table('expenses').select('*').eq('id', expense_id).execute().data[0]

  # Sending email once a expense deleted    #
  # Loading email ids from database #
  recipients  = LoadEmailIds().get_all_recipients()
  subject = f"Expense record Deleted successfully by {session['username']}"
  contents = dict()
  contents['table_title'] = 'Deleted expense'
  contents['table_headings'] = ['#', 'item', 'price', 'purchased date', 'purchased by', 'entry recorded on']
  contents['table_contents'] = [['Deleted ->', expense['item'], expense['price'], expense['purchasing_date'], expense['purchased_by'], expense['entry_date']]]
  
  try:
    supabase.table('expenses').delete().eq('id', expense_id).execute()
    send_mail.send_email_with_rendered_html(subject=subject,
                                              html_filepath = 'email_parser.html', 
                                              recipients= recipients,
                                              contents=contents)
    flash('Expenses deleted successfully', 'success')
  except Exception as e:
    flash("Error occurred while deleting!", 'danger')
  return redirect(url_for('view_expense'))

@app.route('/calculations', methods=['GET', 'POST'])
def calculations():
    def get_calculations_to_make_hisab(expense=[]):
        brijesh_spent=0
        santosh_spent=0
        for e in expense:
            if e['purchased_by'] == 'Brijesh':
                brijesh_spent += e['price']
            else:
                santosh_spent += e['price']
                
        total = brijesh_spent + santosh_spent
        share = int(total / 2)
        calculations = {
            'total': total,
            'brijesh_spent': brijesh_spent,
            'santosh_spent': santosh_spent,
            'share': share
        }
        extra = {}
        if brijesh_spent > share:
            extra['extra_expense'] = brijesh_spent - share
            extra['name'] = 'Brijesh Vishwakarma ने ज्यादा खर्च किए|'
        elif brijesh_spent < share:
            extra['extra_expense'] = santosh_spent - share
            extra['name'] = 'Santosh Vishwakarma ने ज्यादा खर्च किए|'
        else:
            extra['extra_expense'] = 0
            extra['name'] = 'दोनों ने बराबर खर्च किए हैं |'

        calculations['extra'] = extra
        return calculations

    # Get latest calculation history
    calculation_result = supabase.table('calculations').select('*').order('id', desc=True).limit(1).execute().data
    recent_calculation_history = calculation_result[0] if calculation_result else None

    if not recent_calculation_history:
        expense = supabase.table('expenses').select('*').execute().data
    else:
        till_prev_hisab_date = recent_calculation_history['to_date']
        expense = supabase.table('expenses').select('*').gt('purchasing_date', till_prev_hisab_date).execute().data



    calculations = get_calculations_to_make_hisab(expense)
    is_saved = False

    if request.method == 'POST':
      try:
        if calculations['total'] == 0:
            flash('No expenses found! Please add some.', 'warning')
            return redirect(url_for('calculations'))
        # Safely fetch from_date (oldest) and to_date (latest)
        # Reload latest calculation history for display
        calc_result = supabase.table('calculations').select('*').order('id', desc=True).limit(1).execute().data
        if not calc_result:
          # If no previous calculation, fetch from the expenses table
          from_date_result = supabase.table('expenses').select('purchasing_date').order('purchasing_date', desc=False).limit(1).execute().data
          from_date = from_date_result[0]['purchasing_date']
        else:
          from_date= calc_result[0]['to_date']
        
        to_date_result = supabase.table('expenses').select('purchasing_date').order('purchasing_date', desc=True).limit(1).execute().data
        to_date = to_date_result[0]['purchasing_date'] if to_date_result else None

        current_hisab_date = datetime.now().isoformat()

        save_history = {
            'made_by': session['username'],
            'total': calculations['total'],
            'brijesh_spent': calculations['brijesh_spent'],
            'santosh_spent': calculations['santosh_spent'],
            'share': calculations['share'],
            'final_payment': f"₹ {calculations['extra']['extra_expense']} {calculations['extra']['name']}",
            'final_payment_done': True if request.form['final_payment_done'] == 'True' else False,
            'from_date': from_date,
            'to_date': to_date,
            'hisab_date': current_hisab_date
        }

        response = supabase.table('calculations').insert(save_history).execute()
        if response.data:
          is_saved = True

          # Sending email once a expense deleted
          # Loading email ids from database #
          recipients  = LoadEmailIds().get_all_recipients()
          subject = f"Hisab record saved successfully by {session['username']}"
          contents = dict()
          contents['table_title'] = 'Hisab record history'
          contents['table_headings'] = ['#', 'total', 'share', 'brijesh_spent', 'santosh_spent', 'Who spent more?']
          contents['table_contents'] = [['Hisab ->', calculations['total'], calculations['share'], 
                                         calculations['brijesh_spent'], calculations['santosh_spent'], 
                                         f"₹ {calculations['extra']['extra_expense']} {calculations['extra']['name']}" ]]          
          send_mail.send_email_with_rendered_html(subject=subject,
                                                    html_filepath = 'email_parser.html', 
                                                    recipients= recipients,
                                                    contents=contents)
      
          flash('Saved hisab to history successfully', 'success')
      except Exception as e:
        flash(f"Error {e} occurred during saving hisab history", 'danger')

    # Reset if data was saved or nothing was spent
    if is_saved or calculations['total'] == 0:
        calculations = get_calculations_to_make_hisab()
        calculations['extra']['name'] = "कोई खर्च नहीं है |"

    # Reload latest calculation history for display
    calc_result = supabase.table('calculations').select('*').order('id', desc=True).limit(1).execute().data
    latest_history = calc_result[0] if calc_result else None

    return render_template('calculations.html', data=calculations, calculation_history=latest_history)


@app.route('/calculations_history')
def calculations_history():
  calculations_history = supabase.table('calculations').select('*').order('id', desc=True).execute().data
  return render_template('calculations_history.html', calculations_history=calculations_history)

@app.route('/final_payment_done/<int:history_id>', methods=['POST'])
def final_payment_done(history_id):
    try:
        response = supabase.table('calculations').select('*').eq('id', history_id).execute()

        if not response.data:
            flash("Record not found", 'danger')
            return redirect(url_for('calculations_history'))

        history = response.data[0]
        history['final_payment_done'] = True
        update_response = supabase.table('calculations').update(history).eq('id', history_id).execute()

        if update_response.data:
          # Sending email once a hisab record updated
          # Loading email ids from database #
          recipients  = LoadEmailIds().get_all_recipients()
          subject = f"Payment recieved, Hisab record updated successfully by {session['username']}"
          contents = dict()
          contents['table_title'] = 'Payment Recieving Confirmation'
          contents['table_headings'] = [col + ' (₹)' if col in ['total', 'brijesh_spent', 'santosh_spent', 'share'] else col  for col in response.data[0].keys()]
          contents['table_contents'] = [[value for value in response.data[0].values()]]

          send_mail.send_email_with_rendered_html(subject=subject,
                                                  html_filepath = 'email_parser.html', 
                                                  recipients= recipients,
                                                  contents=contents)
          flash('Updated successfully', 'success')
        else:
          flash('Update failed, please try again.', 'danger')

    except Exception as e:
        flash("Error occurred please try again later", 'danger')

    return redirect(url_for('calculations_history'))

@app.route('/send_report', methods=['GET'])
def send_report():
  try:
    response = supabase.table('calculations').select('*').execute()
    if not response.data:
      flash("No data found", 'danger')
      return redirect(url_for('admin_dashboard'))

    history = response.data
    column_names = [column for column in history[0].keys()]
    records = []
    for record in history:
      row_data = []
      for column in column_names:
        col_value = record[column]
        row_data.append(col_value)
      records.append(row_data)


    # Sending email report of hisab-kitab    #
    # Loading email ids from database #
    recipients  = LoadEmailIds().get_all_recipients()
    subject = f"हिसाब-किताब Report shared by {session['username']}"
    contents = dict()
    contents['table_title'] = 'हिसाब-किताब कब-कब हुआ|'
    contents['table_headings'] = column_names
    contents['table_contents'] = records
    send_mail.send_email_with_rendered_html(subject=subject,
                                            recipients=recipients,
                                            contents=contents,
                                            html_filepath='email_parser.html')

    flash("Report shared successfully with all users!", 'success')
  except Exception as e:
    flash(f"Some error {e} occurred!", 'danger')
  return redirect(url_for('admin_dashboard'))

@app.route('/view_expenses_history/<history_id>', methods=['GET', 'POST'])
def view_expenses_history(history_id):
    # Fetch the calculation range
    calculations_history_record = supabase.table('calculations') \
        .select('*') \
        .eq('id', history_id) \
        .execute().data[0]

    from_date = calculations_history_record['from_date']
    to_date = calculations_history_record['to_date']

    # Fetch all expenses within the date range
    all_expenses = supabase.table('expenses') \
        .select('*') \
        .gt('purchasing_date', from_date) \
        .lte('purchasing_date', to_date) \
        .execute().data

    # Collect all unique names from the expenses
    dynamic_names = set(e['purchased_by'] for e in all_expenses)

    # Ensure 'Brijesh' and 'Santosh' are always included
    required_names = {'Brijesh', 'Santosh'}
    all_names = sorted(dynamic_names.union(required_names))  # merged and sorted

    # Get checkbox values from URL query
    selected_users = request.args.getlist('purchased_by')

    # Apply filter if selected_users is non-empty
    if selected_users:
        filtered_expenses = [e for e in all_expenses if e['purchased_by'] in selected_users]
    else:
        filtered_expenses = all_expenses  # No filter, show all

    return render_template('view_expenses_history.html',
                           expenses=filtered_expenses,
                           all_names=all_names,
                           selected_users=selected_users)


if __name__ == '__main__':
  app.run(debug=True)