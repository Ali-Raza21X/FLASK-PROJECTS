from flask import Flask, redirect, render_template, request, url_for, flash, abort, session
from forms import RegistrationForm, LoginForm, PostForm
from flask_bcrypt import Bcrypt
from extensions import db
from models import User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)





#default

# home route
@app.route('/')
@app.route('/home')
def home():
    tposts=Post.query.all()
    return render_template('home.html',tposts=tposts,title='Home')


# about route
@app.route('/about')
def main():
    return render_template('about.html',title='About')


# register route

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("Email already registered. Please use another email.", "danger")
            return redirect(url_for('register'))
        hashedpass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashedpass
        )

        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to login", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# login route

@app.route('/login', methods=['GET', 'POST'])
def login():


    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and Bcrypt().check_password_hash(user.password, form.password.data):
             
               session['user_id'] = user.id
               session['username'] = user.username
        flash('Logged in successfully', 'success')
        
        # gpt
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
            flash('Login unsuccessful! Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


# post route



@app.route('/post', methods=['GET', 'POST'])
def new():

     
    if 'user_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('login'))
    
    
    form = PostForm()
    
    if form.validate_on_submit():
        post=Post(title=form.title.data,
                  content=form.content.data,
                   user_id=session['user_id'] )
        db.session.add(post)
        db.session.commit()
        flash('posted successfully','success')
        return redirect(url_for('home'))

    return render_template('create_post.html',title='New Post',form=form)
    
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)




@app.route("/post/<int:post_id>/delete",methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if 'user_id' not in session or post.user_id != session['user_id']:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    flash('Post deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)

    
    