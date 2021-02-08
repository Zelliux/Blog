from flask import Flask, render_template, redirect, request, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
from util.utility import prettify_date

"""
INSTANCES
"""
# app
app = Flask(__name__, static_url_path='')
# login
login_manager = LoginManager()
login_manager.init_app(app)
# sql
db = SQLAlchemy(app)

"""
CONFIG
"""
# Secret Key config
app.secret_key = 'hViyPctqQbOcqfQ/zKUcMrXkOokUTpuYim#QYvLD'

# set session time limit to 2 years
app.permanent_session_lifetime = timedelta(days=365*2)

app.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    SECURITY_PASSWORD_SALT='ZelliusPasswordHash',
    SQLALCHEMY_DATABASE_URI='sqlite:///database/user.db',
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024 # In bytes
)


"""
CODE
"""

class User(UserMixin, db.Model):
    """
    Database data.
    Database class of user    
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    google_account = db.Column(db.Boolean, nullable=False)
    google_id = db.Column(db.Text)
    account_creation_date = db.Column(db.Date, nullable=False)

class Post(UserMixin, db.Model):
    """
    Database data.
    Database class of user    
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    post_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)



# Return user function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Handle login error (401)
@app.errorhandler(401)
def custom_401(error):
    return render_template('index.html', error='sign-in', error_message='You need to sign in to create a post.', modal='sign-in')

# Handle not found error (404)
@app.errorhandler(404)
def custom_404(error):
    return render_template('index.html', error='not-found', error_message='Page not found.')

# Home
@app.route('/')
def index():
    """
    Main page
    """
    is_logged = current_user.is_authenticated


    if is_logged:
        # Get session account values
        user = User.query.filter_by(id=current_user.id).first()
        
        # shorten name in case it's too large
        user.name = user.name if len(user.name) < 25 else user.name[:25]+'...'

        return render_template('index.html', is_logged=is_logged, user=user)
    else:
        return render_template('index.html')



@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():

    is_logged = current_user.is_authenticated

    if not is_logged and request.method == 'POST':
        # Get form values
        email = request.form['sign-in-email']
        password = request.form['sign-in-password']

        if email and password:
            try:
                user = User.query.filter_by(email=email).first()

                if user.email == email and user.password == password:
                    login_user(user, remember=True)
                    
                    return redirect('/')

                else:
                    return render_template('index.html', error='sign-in', error_message='Email does not match the password, please try again.', modal='sign-in')

            except:
                return render_template('index.html', error='sign-in', error_message='The account does not exist.', modal='sign-in') 
        else:
            return render_template('index.html', error='sign-in', error_message='Please fill the form.', modal='sign-in') 



    # Handle: already logged
    else:
        print(request.method)
        return redirect('/')  



@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    """
    Create an account
    """

    is_logged = current_user.is_authenticated

    if not is_logged and request.method == 'POST':
        # Get form values
        name = request.form['sign-up-name']
        email = request.form['sign-up-email']
        password = request.form['sign-up-password']

        if len(password) >= 6:
            if len(email) < 500 or len(name) < 500:

                try:
                    # Check if account already exists
                    user = User.query.filter_by(email=email).first()

                    if user.email:
                        return render_template('index.html', error='sign-in', error_message='Account already exists.', modal='sign-up')
                
                except:
                    # Create new user
                    user = User(name=name, email=email, password=password, account_creation_date=datetime.now())

                    try:
                        # Add user data to database
                        db.session.add(user)
                        db.session.commit()

                        # Login user
                        status = login_user(user)

                        return redirect('/')

                    except Exception as E:
                        return str(E)

            # Handle: too large name / email
            else:
                return render_template('index.html', error='sign-in', error_message='Too large name or email.', modal='sign-up')

        # Handle: too large password
        else:
            # return redirect(url_for('.index', error='sign-up', error_message='The password must be 6 chars in length'))
            return render_template('index.html', error='sign-up', error_message='The password must be 6 chars in length', modal=True)
    
    # Handle: already logged
    else:
        return render_template('index.html', error='sign-up', error_message='You are already signed in.', modal=True)
    
    
@app.route('/log-out')
@login_required
def logout():
    logout_user()
    return redirect('/')


"""
POSTS 
"""

@app.route('/create')
@login_required
def create_post():

    # Get session account values
    user = User.query.filter_by(id=current_user.id).first()
    
    # shorten name in case it's too large
    user.name = user.name if len(user.name) < 25 else user.name[:25]+'...'

    return render_template('create_post.html', is_logged=True, user=user)


@app.route('/submit-post', methods=['POST', 'GET'])
@login_required
def submit_post():
    if request.method == 'POST':
        title = request.form['post-title']
        content = request.form['post-content']

        post = Post(name=current_user.name, post_date=datetime.now(), title=title, content=content)

        try:
            # Add user data to database
            db.session.add(post)
            db.session.commit()

            # Login user

            return redirect(f'/post/{post.id}')

        except Exception as E:
            return str(E)
            

@app.route('/post/<id>')
def post(id):


    # check if user is logged
    is_logged = current_user.is_authenticated

    if is_logged:

        # Get session account values
        user = User.query.filter_by(id=current_user.id).first()

        # shorten name in case it's too large
        user.name = user.name if len(user.name) < 25 else user.name[:25]+'...'


    try:
        # Get post values
        post = Post.query.filter_by(id=id).first()

        # Prettify date
        post_date = prettify_date(post.post_date)

        # Return post page with the variables
        return render_template('post.html', 
        name=post.name, 
        post_date=post_date, 
        title=post.title, 
        content=post.content,
        is_logged=is_logged, 
        user=user)
    
    except AttributeError:
        return redirect('/not-found') 

@app.route('/recent')
def recent_posts():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")