from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blog:gato@localhost:3306/blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(30))
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, blog_title, name):
        self.blog_title = blog_title
        self.name = name
        self.completed = False



@app.route('/', methods=['POST', 'GET'])
def index():

    completed_blogs = Blog.query.all()
    return render_template('blogs.html',title="Blog Feed!", 
        completed_blogs=completed_blogs)


@app.route('/new-blog', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_doc = request.form['blog']
        if blog_title == "":
            error1 = "Please enter something in the blog title."
            return render_template('newpost.html',title="New Post!", 
            error1=error1, titlearea=blog_title, textarea=blog_doc)
        if blog_doc == "":
            error2 = "Please enter something in the blog body."
            return render_template('newpost.html',title="New Post!",
            error2=error2, titlearea=blog_title, textarea=blog_doc)
        new_blog = Blog(blog_title, blog_doc)
        db.session.add(new_blog)
        db.session.commit()

    return render_template('newpost.html',title="New Post!")

@app.route('/blogpost', methods=['POST', 'GET'])
def single_post():
    blog_id = request.args.get('id')
    blog_record = db.session.query(Blog).filter_by(id=blog_id).one()

    return render_template('blogpost.html', title=blog_record.blog_title,
    body=blog_record.name)


if __name__ == '__main__':
    app.run()