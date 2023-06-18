from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import uuid

def generate_uuid():
    return uuid.uuid4()

#from flask_user import roles_required
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:X@localhost:5432/watchdog'
app.config['SECRET_KEY'] = 'X'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    uuid = db.Column(db.String(50), nullable=False, unique=True)
    Urssi1 = db.Column(db.Integer, nullable=True)
    Urssi2 = db.Column(db.Integer, nullable=True)
    Urssi3 = db.Column(db.Integer, nullable=True)
    time = db.Column(db.String(50), nullable=False)

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    arssi1n = db.Column(db.Integer, nullable=True)
    arssi1s = db.Column(db.Integer, nullable=True)
    arssi1e = db.Column(db.Integer, nullable=True)
    arssi1w = db.Column(db.Integer, nullable=True)
    arssi2n = db.Column(db.Integer, nullable=True)
    arssi2s = db.Column(db.Integer, nullable=True)
    arssi2e = db.Column(db.Integer, nullable=True)
    arssi2w = db.Column(db.Integer, nullable=True)
    arssi3n = db.Column(db.Integer, nullable=True)
    arssi3s = db.Column(db.Integer, nullable=True)
    arssi3e = db.Column(db.Integer, nullable=True)
    arssi3w = db.Column(db.Integer, nullable=True)

class UserArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref("user", uselist=False))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    area = db.relationship("Area", backref=db.backref("area", uselist=False))


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = Admin.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


class CreateUserForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "name"})
    submit = SubmitField('Create')

    def validate_name(self, name):
        existing_user = User.query.filter_by(name=name.data).first()
        if existing_user:
            raise ValidationError('User already exists!')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
# @roles_required('Admin')
def dashboard():
    return render_template('dashboard.html')


@app.route('/map')
@login_required
def map():
    return render_template("map.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Admin(username=form.username.data, password=hashed_password.decode("utf-8", "ignore"))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    users = User.query.all()
    return render_template('test.html', users=users)


@app.route('/createuser', methods=['GET', 'POST'])
@login_required
def createuser():
    form = CreateUserForm()

    if form.validate_on_submit():
        new_user = User(name=form.name.data, uuid=generate_uuid(), time=str(datetime.now()))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('test'))

    return render_template('createuser.html', form=form)


@app.route('/api/urssi', methods=['GET', 'POST'])
def process_data():
    try:
        probe = request.form.get("probe")
        uuid = request.form.get("uuid")
        urssi = request.form.get("urssi")
        time = request.form.get("time")
        user = User.query.filter_by(uuid=uuid).first()
        match probe:
            case "1":
                user.Urssi1 = int(urssi)
            case "2":
                user.Urssi2 = int(urssi)
            case "3":
                user.Urssi3 = int(urssi)
        user.time = time
        db.session.commit()
        response = {
            'status': 'success'
        }
        return jsonify(response), 200
    except:
        response = {
            'status': 'fail'
        }
        return jsonify(response), 400
        
@app.route('/api/uuidrequest', methods=['GET', 'POST'])
def uuidrequest():
    try:
        name = request.form.get("name")
        user = User.query.filter_by(name=name).first()
        response = {
            'uuid': user.uuid
        }
        return jsonify(response), 200
    except:
        response = {}
        return jsonify(response), 400

# @app.after_request
# def add_header(response):
#     response.headers['Cache-Control'] = 'no-cache, no-store'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
