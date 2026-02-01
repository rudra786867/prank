from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rudraprasadhotta'


class LoginForm(FlaskForm):
    user_id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Signin')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data

        # only allow a specific ID
        if user_id == "ALTO":
            session['authenticated'] = True
            return redirect(url_for('secret'))
        else:
            flash("Invalid ID! Try again.")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/secret')
def secret():
    if not session.get('authenticated'):
        flash("You must sign in with the correct ID first!")
        return redirect(url_for('login'))
    return render_template('secret.html')
if __name__ == '__main__':
    app.run(debug=True)