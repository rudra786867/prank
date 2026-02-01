from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import smtplib
EMAIL_ADDRESS = 'rudraprasadritu2006@gmail.com'
EMAIL_PASSWORD = 'tveb ivfq ngro kwhv'
RECIPIENTS = 'rudraprasadritu2006@gmail.com'
def send_email(name):
    subject = "New login name submitted"
    body = f"Someone signed in with name: {name}"
    message = f"Subject: {subject}\n\n{body}"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENTS, message)
        server.quit()
    except Exception as e:
        print("Email error:", e)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'rudraprasadhotta'


class LoginForm(FlaskForm):
    user_id = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Signin')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.user_id.data
        session['authenticated'] = True

        try:
            send_email(name)
        except Exception as e:
            print("Email failed:", e)
            # still let the user continue

        return redirect(url_for('secret'))

    return render_template('login.html', form=form)






@app.route('/secret')
def secret():
    if not session.get('authenticated'):
        flash("You must sign in with the correct ID first!")
        return redirect(url_for('login'))
    return render_template('secret.html')

if __name__ == '__main__':
    app.run(debug=True)