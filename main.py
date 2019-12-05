from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:gato@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    blog_id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(30))
    body = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

    def __init__(self, blog_title, body, user):
        self.blog_title = blog_title
        self.body = body
        self.user = user

class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blog = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

signedin = False
#username = None

@app.route('/', methods=['POST', 'GET'])
def index():
    #global username
    #username = request.args.get('username')

    global signedin
    users = Users.query.all()

    return render_template('index.html', signedin=signedin, users=users)

@app.route("/sign-in", methods=['POST', 'GET'])
def check_signin_form():
    if request.method == 'POST':
        username = request.form['user-id']
        password = request.form["password"]
        pass_check = request.form["pass-check"]
        errors = 0

        error1 = ""
        error2 = ""
        error3 = ""
        error4 = ""
        error5 = ""
        error6 = ""
        error7 = ""

        if (username.strip() == ""):
            error1 = "Please enter your name."
            errors += 1

        if (password.strip() == ""):
            error2 = "Please enter your password."
            errors += 1

        if (pass_check.strip() == ""):
            error3 = "Please enter your password verification."
            errors += 1
        
        if (len(username) < 3) or (len(username) > 20) or (" " in username):
            error4 = "Please enter a valid username. Within the range of 3 to 20 characters and contains no spaces"
            errors += 1

        if (len(password) < 3) or (len(password) > 20) or (" " in password):
            error5 = "Please enter a valid password Within the range of 3 to 20 characters and contains no spaces"
            errors += 1

        if (password != pass_check):
            error6 = "Make sure your password and password verification are the same."
            errors += 1

        if (errors > 0):
            return render_template('form.html', name_mem=username, error1=error1, error2=error2, error3=error3, error4=error4, error5=error5, error6=error6, error7=error7)

        db_check = db.session.query(Users).filter_by(username=username).first()

        global signedin
        signedin = False

        if db_check == None or db_check.username == None or db_check.password == None:
            missing_account = "There is no account with this username or password."
            return render_template('form.html', error_account=missing_account, signedin=signedin)

        
        signedin = True
        completed_blogs = Blog.query.all()
        session['username'] = username
        users = Users.query.all()

        return render_template('index.html', users=users, username=session['username'], signedin=signedin, completed_blogs=completed_blogs)
    return render_template('form.html',title="Sign In!", signedin=signedin)

@app.route("/sign-up", methods=['POST', 'GET'])
def check_signup_form():

    if request.method == 'POST':
        username = request.form['user-id']
        password = request.form["password"]
        pass_check = request.form["pass-check"]
        errors = 0

        error1 = ""
        error2 = ""
        error3 = ""
        error4 = ""
        error5 = ""
        error6 = ""
        error7 = ""

        if (username.strip() == ""):
            error1 = "Please enter your name."
            errors += 1

        if (password.strip() == ""):
            error2 = "Please enter your password."
            errors += 1

        if (pass_check.strip() == ""):
            error3 = "Please enter your password verification."
            errors += 1
        
        if (len(username) < 3) or (len(username) > 20) or (" " in username):
            error4 = "Please enter a valid username. Within the range of 3 to 20 characters and contains no spaces"
            errors += 1

        if (len(password) < 3) or (len(password) > 20) or (" " in password):
            error5 = "Please enter a valid password Within the range of 3 to 20 characters and contains no spaces"
            errors += 1

        if (password != pass_check):
            error6 = "Make sure your password and password verification are the same."
            errors += 1

        if (errors > 0):
            return render_template('form.html', name_mem=username, error1=error1, error2=error2, error3=error3, error4=error4, error5=error5, error6=error6, error7=error7)

        db_check = db.session.query(Users).filter_by(username=username).first()

        global signedin
        signedin = False

        if db_check != None:
            missing_account = "There is already an account with this username. Please choose another."
            return render_template('form.html', error_account=missing_account, signedin=signedin)

        
        signedin = True
        completed_blogs = Blog.query.all()

        

        new_account = Users(username, password)
        db.session.add(new_account)
        db.session.commit()

        session['username'] = username
        users = Users.query.all()

        return render_template('index.html', users=users, username=session['username'], signedin=signedin, completed_blogs=completed_blogs)
    return render_template('signup.html',title="Sign Up Here!", signedin=signedin)

@app.route('/new-blog', methods=['POST', 'GET'])
def new_post():
    global signedin
    #global username

    if request.method == 'POST':
        #global username
        blog_title = request.form['blog-title']
        body = request.form['blog']
        if blog_title == "":
            error1 = "Please enter something in the blog title."
            return render_template('newpost.html',title="New Post!", 
            error1=error1, titlearea=blog_title, textarea=body, username=session['username'])
        if body == "":
            error2 = "Please enter something in the blog body."
            return render_template('newpost.html',title="New Post!",
            error2=error2, titlearea=blog_title, textarea=body, username=session['username'])
        user = Users.query.filter_by(username=session['username']).first()
        new_blog = Blog(blog_title, body, user)
        db.session.add(new_blog)
        db.session.commit()
        return render_template('blogpost.html',title=blog_title, body=body, user=session['username'], username=session['username'], signedin=signedin)

    return render_template('newpost.html',title="New Post!", username=session['username'], signedin=signedin)

@app.route('/blogs', methods=['POST', 'GET'])
def blogs():
    global signedin
    username = request.args.get('username')
    completed_blogs = Blog.query.all()
    return render_template('blogs.html', username=session['username'], completed_blogs=completed_blogs, signedin=signedin)

@app.route('/blogpost', methods=['POST', 'GET'])
def post_list():
    global signedin
    username = request.args.get('username')
    user = request.args.get('user')
    blog_id = request.args.get('id')
    blog_record = db.session.query(Blog).filter_by(blog_id=blog_id).one()

    return render_template('blogpost.html', title=blog_record.blog_title,
    body=blog_record.body, user=user, username=session['username'], signedin=signedin)

@app.route('/singleUser', methods=['POST', 'GET'])
def user_list():
    global signedin
    user = request.args.get('username')
    blogs = Users.query.filter_by(username=user).first().blog

    return render_template('singleUser.html', user=user, username=session['username'], blog_list=blogs, signedin=signedin)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    global signedin
    signedin = False
    session['username'] = None

    completed_blogs = Blog.query.all()
    users = Users.query.all()

    return render_template('index.html', users=users, signedin=signedin, completed_blogs=completed_blogs)


if __name__ == '__main__':
    app.run()