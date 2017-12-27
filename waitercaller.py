from flask import Flask, render_template
from flask import request, redirect, url_for

from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user
from flask_login import current_user

from mockdbhelper import MockDbHelper as DbHelper
from user import User
from passwordhelper import PasswordHelper
import config


app = Flask(__name__)
# secret key for signing cookies
app.secret_key = ("7MflXuEmpMAHI4IGtBFCpvddXmgkkhC7oXh5Hl12COQv1nrtoqimXx" +
                  "AbrjbzrNhq3N75D3VGFYxNv7iKSllLMBd/OORglMXJACn")

login_manager = LoginManager(app)

db_helper = DbHelper()

pw_helper = PasswordHelper()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/account")
@login_required
def account():
    tables = db_helper.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables)


@app.route("/account/createtable", methods=['POST'])
@login_required
def account_createtable():
    tablenumber = request.form.get('tablenumber')
    table_id = db_helper.add_table(tablenumber, current_user.get_id())
    new_url = config.base_url + 'newrequest/' + table_id
    db_helper.update_table(table_id, new_url)
    return redirect(url_for('account'))


@app.route("/account/deletetable")
@login_required
def account_deletetable():
    table_id = request.args.get('table_id')
    db_helper.delete_table(table_id)
    return redirect(url_for('account'))


# this route for handle user entering email and password
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    # check with email and password in database
    user_in_db = db_helper.get_user(email)
    if user_in_db and pw_helper.validate_password(password,
                                                  user_in_db['salt'],
                                                  user_in_db['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    
    return home()   # login failed


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    

@app.route("/register", methods=["POST"])
def register():
    # get the values from form-post
    email = request.form.get('email')
    password1 = request.form.get('password')
    password2 = request.form.get('password2')

    # if 2 passwords not identical
    if password1 != password2:
        return redirect(url_for('home'))

    # if email is duplicate
    if db_helper.get_user(email):
        return redirect(url_for('home'))

    salt = pw_helper.get_random_salt()
    hashed = pw_helper.get_hash(password1+salt)
    db_helper.add_user(email, salt, hashed)
    return redirect(url_for('home'))


# We need to create this method for flask_login, or we will get error
# Exception: No user_loader has been installed
@login_manager.user_loader
def load_user(user_email):
    user_in_db = db_helper.get_user(user_email)
    if user_in_db:
        return User(user_email)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
