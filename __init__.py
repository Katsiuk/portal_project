from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://portal:W5edhu8Z6^@localhost/portal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "hello"
app.permanent_session_lifetime = datetime.timedelta(minutes=10)

db = SQLAlchemy(app)

class film(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    year = db.Column(db.DateTime, default=datetime.datetime.year)
    IMDB = db.Column(db.Float, nullable=False)

    def __init__(self, name, duration, rating, year, IMDB):
        self.name = name
        self.duration = duration
        self.rating = rating
        self.year = year
        self.IMDB = IMDB

    def __repr__(self):
        return f'<film {self._id}>'
    

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<users {self._id}>'


@app.route("/", methods=('GET', 'POST'))
@app.route("/home")
def home():
    films = film.query.order_by(film.year.desc()).all()
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            found_records = request.form.getlist('removing')
            for elem in found_records:
                db.session.delete(film.query.filter_by(_id=elem).first())
                db.session.commit()
            return redirect(url_for('home'))
    else:
        flash("Please login or sing up", category="error")
        return redirect(url_for("register"))
    return render_template("index.html", films=films)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            name = request.form['name']
            duration = request.form['duration']
            rating = request.form['rating']
            year = request.form['year']
            imdb = request.form['imdb']

            if not name:
                flash('Name is required!')
            elif not duration:
                flash('Duration is required!')
            elif not rating:
                flash('Rating is required!')
            elif not year:
                flash('Year is required!')
            elif not imdb:
                flash('IMDB is required!')
            else:
                info = film(name, duration, rating, year, imdb)
                db.session.add(info)
                db.session.commit()
                return redirect(url_for('home'))
    else:
        flash("Please login or sing up", category="error")
        return redirect(url_for("register"))
    

    return render_template('create.html')

@app.route("/update/<int:_id>", methods=['GET', 'POST'])
def update(_id):
    film_to_update = film.query.get_or_404(_id)
    films = film.query.all()
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            film_to_update.name = request.form['name']
            film_to_update.duration = request.form['duration']
            film_to_update.rating = request.form['rating']
            film_to_update.year = request.form['year']
            film_to_update.IMDB = request.form['imdb']
            try:
                db.session.commit()
                return redirect('/home')
            except:
                return "There was a problem updating that film..."
        else:
            return render_template("update.html", film_to_update=film_to_update)
    else:
        return redirect(url_for("register"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if request.form.get('match') == 'remember-me':
            session.permanent = True
        else:
            session.permanent = False
        user, passwd = request.form["nm"], request.form["psw"]

        found_user = users.query.filter_by(name=user).first()

        if found_user and md5(bytes(passwd.encode())).hexdigest() == found_user.password:    
            flash("Login successful", category="success")
            session["user"], session["passwd"] = user, passwd
            return redirect(url_for("user"))
        else:
            flash("Incorrect password or login. Try again or sign up, please!", category="error")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user", methods=['GET', 'POST'])
def user():
    if "user" in session:
        user = session["user"]
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))
    return render_template("user.html", user=user)

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form.get('match') == 'remember-me':
            session.permanent = True
        else:
            session.permanent = False
        user = request.form["lg"]
        email = request.form["em"]
        passwd, passwdc = request.form["psw"], request.form["pswc"]

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            flash(f"User {user} exists! Try to log in!")
            session.clear()
            return redirect(url_for("login"))
        else:
            if passwd == passwdc:
                print(f"Password: {type(passwd)}; Hash: {hash(passwd)}")
                usr = users(user, email, md5(bytes(passwd.encode())).hexdigest())
                try:
                    db.session.add(usr)
                    db.session.commit()
                    session.clear()
                except:
                    return "Registartion error!"
                flash("Registration successfull")
                return redirect(url_for("login"))
            else:
                return "Passwords are not similar!"
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("login"))

        return render_template("register.html")


if __name__ == '__main__':
    db.create_all()
    #app.run(debug=True)
    app.run(host='0.0.0.0')
