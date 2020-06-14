#author: pranitha
from datetime import datetime
from flask import Flask,render_template,url_for,flash,redirect
from forms import RegistrationForm,LoginForm
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SECRET_KEY']='28f0bce5c25ac75811e434a0e5a9c4df'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=False,default="default.jpg")
    posts=db.relationship('Post',backref='author',lazy=True)
    password=db.Column(db.String(60),nullable=False)
    def __repr__(self):
        return "User('{}','{}','{}')".format(self.username,self.email,self.password)
    
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column=(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self):
        return "Post('{}','{}')".format(self.title,self.date_posted,nullable=False)


posts=[
    {
       'author':'pranitha peddi',
        'title':'blog post 1',
        'content':'first post',
        'date_posted':'June 13, 2020'
    },
    {
       'author':'hello kitty',
        'title':'blog post 2',
        'content':'second post',
        'date_posted':'June 14, 2020'
    }
    
]
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",posts=posts)
@app.route("/about")
def about():
    return render_template("about.html",title="ABOUT")
@app.route("/register",methods=['GET','POST'])
def register():
    form= RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {} !'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template("register.html",title="Register",form=form)
@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if(form.email.data=="admin@blog.com" and form.password.data=="password"):
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsucessful! Please check username and password.', 'danger')
    return render_template("login.html",title="Login",form=form)

if __name__=='__main__':
    app.run(debug=True)

