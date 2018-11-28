from flask import Flask, render_template, flash, request, redirect, session
from mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


app=Flask(__name__)
app.secret_key = "wielfjoijwefoemwf"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email', methods=['POST'])
def email():
    print(request.form)
    errors=False

    if len(request.form['email']) < 1:
        flash('Email can not be empty. Try again.')
        errors=True

    if not EMAIL_REGEX.match(request.form['email']):
        flash('email must be valid. try again')
        errors=True

    else:
        mysql = connectToMySQL('emaildb')
        query = 'SELECT email FROM emails WHERE email = %(contact)s;'
        data = {
                'contact': request.form['email']
                }
        matching_email = mysql.query_db(query, data)
    if len(matching_email) > 0:
        flash('Email already in use')
        errors = True

        if errors==True:
            return redirect('/')

    else:
        mysql = connectToMySQL('emaildb')
        query = "INSERT INTO emails(email, created_at, updated_at) VALUES(%(email)s, NOW(), NOW());"
        data = {
            'email': request.form['email']
        }
        user_id = mysql.query_db(query, data)
        session['user_id'] = user_id

        return redirect('/success')


# @app.route('/delete')
# def delete():



@app.route('/success')
def success():
    mysql = connectToMySQL('emaildb')
    query = "SELECT * FROM emails;"
    new_email_id = mysql.query_db(query)
    return render_template('success.html', emails=new_email_id)


if __name__=="__main__":
    app.run(debug=True)
