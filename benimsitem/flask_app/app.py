from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Kullanıcı modeli
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Home Route
@app.route("/")
def home():
    return render_template("home.html")

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Kullanıcı adı zaten mevcut!"

        with app.app_context():
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect('/dashboard')  # Doğrudan URL yönlendirmesi
        else:
            return "Geçersiz kullanıcı adı veya şifre!"
    return render_template("login.html")

# Dashboard Route
@app.route("/dashboard")
def dashboard():
    return "Dashboard Görüntüleme"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Veritabanı oluşturma
    app.run(debug=True)
