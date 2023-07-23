from datetime import datetime
from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange
from flask_bcrypt import Bcrypt
import uuid
import requests
import time
import threading

def generate_uuid():
    return uuid.uuid4()

#from flask_user import roles_required
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:P0stgres@localhost:5432/watchdog'
app.config['SECRET_KEY'] = '422718fe17b063bc6f00f386a0befa4846a58092eb1fe94f81b212fc4b4f813e'


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
    camera = db.Column(db.Integer, nullable=True)
    capture = db.Column(db.String(50), nullable=False)
    userarea = db.relationship("UserArea", backref='user')

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
    userarea = db.relationship("UserArea", backref='area')
    door = db.relationship("Door", backref='area')
    

class UserArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))

class Door(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    drssi11 = db.Column(db.Integer, nullable=True)
    drssi12 = db.Column(db.Integer, nullable=True)
    drssi13 = db.Column(db.Integer, nullable=True)
    drssi21 = db.Column(db.Integer, nullable=True)
    drssi22 = db.Column(db.Integer, nullable=True)
    drssi23 = db.Column(db.Integer, nullable=True)
    


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = Admin.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


class CreateUserForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "name"})
    submit = SubmitField('Create')

    def validate_name(self, name):
        existing_user = User.query.filter_by(name=name.data).first()
        if existing_user:
            raise ValidationError('User already exists!')
        

class CreateAreaForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "area name"})
    arssi1n = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi1s = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi1e = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi1w = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi2n = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi2s = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi2e = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi2w = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi3n = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi3s = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi3e = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    arssi3w = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    submit = SubmitField('Create')

    def validate_name(self, name):
        existing_area = Area.query.filter_by(name=name.data).first()
        if existing_area:
            raise ValidationError('Area already exists!')


class CreateDoorForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "door name"})
    drssi11 = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    drssi12 = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    drssi13 = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    drssi21 = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    drssi22 = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])
    drssi23 = IntegerField(validators=[InputRequired(), NumberRange(min=-90, max=0)])    
    area = SelectField(validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super(CreateDoorForm, self).__init__(*args, **kwargs)
        self.area.choices = [value[0] for value in db.session.query(Area.name)]
    
    submit = SubmitField('Create')

    def validate_name(self, name):
        existing_door = Door.query.filter_by(name=name.data).first()
        if existing_door:
            raise ValidationError('Door already exists!')

    def validate_area(self, area):
        existing_area = Area.query.filter_by(name=area.data).first()
        if not existing_area:
            raise ValidationError('Area does not exists!')


class CreateUserAreaForm(FlaskForm):

    name = SelectField(validators=[InputRequired()])
    area = SelectField(validators=[InputRequired()])
    def __init__(self, *args, **kwargs):
        super(CreateUserAreaForm, self).__init__(*args, **kwargs)
        self.name.choices = [value[0] for value in User.query.with_entities(User.name)]
        self.area.choices = [value[0] for value in db.session.query(Area.name)]

    submit = SubmitField('Create')

    def validate_name(self, name):
        existing_user = User.query.filter_by(name=name.data).first()
        if not existing_user:
            raise ValidationError('User does not exists!')
    def validate_area(self, area):
        existing_area = Area.query.filter_by(name=area.data).first()
        if not existing_area:
            raise ValidationError('Area does not exists!')

"""
@app.route('/')
def home():
    return render_template('home.html')
"""


@app.route('/', methods=['GET', 'POST'])
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
    areas = Area.query.all()
    userareas = UserArea.query.all() 
    doors = Door.query.all()   
    return render_template('test.html', users=users, areas=areas, userareas = userareas, doors=doors)


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


@app.route('/createarea', methods=['GET', 'POST'])
@login_required
def createarea():
    form = CreateAreaForm()

    if form.validate_on_submit():
        new_area = Area(name=form.name.data,
                        arssi1n=form.arssi1n.data,
                        arssi1s=form.arssi1s.data,
                        arssi1e=form.arssi1e.data,
                        arssi1w=form.arssi1w.data,
                        arssi2n=form.arssi2n.data,
                        arssi2s=form.arssi2s.data,
                        arssi2e=form.arssi2e.data,
                        arssi2w=form.arssi2w.data,
                        arssi3n=form.arssi3n.data,
                        arssi3s=form.arssi3s.data,
                        arssi3e=form.arssi3e.data,
                        arssi3w=form.arssi3w.data)
        db.session.add(new_area)
        db.session.commit()
        return redirect(url_for('test'))

    return render_template('createarea.html', form=form)


@app.route('/createdoor', methods=['GET', 'POST'])
@login_required
def createdoor():
    form = CreateDoorForm()

    if form.validate_on_submit():
        area=Area.query.filter_by(name=form.area.data).first()
        new_door = Door(name=form.name.data,
                        drssi11=form.drssi11.data,
                        drssi12=form.drssi12.data,
                        drssi13=form.drssi13.data,
                        drssi21=form.drssi21.data,
                        drssi22=form.drssi22.data,
                        drssi23=form.drssi23.data,
                        area_id=area.id)
        db.session.add(new_door)
        db.session.commit()
        return redirect(url_for('test'))

    return render_template('createdoor.html', form=form)


@app.route('/createuserarea', methods=['GET', 'POST'])
@login_required
def createuserarea():
    form = CreateUserAreaForm()

    if form.validate_on_submit():
        
        user=User.query.filter_by(name=form.name.data).first()
        area=Area.query.filter_by(name=form.area.data).first()
        new_user_area = UserArea(user_id=user.id, area_id=area.id)
        db.session.add(new_user_area)
        db.session.commit()
        return redirect(url_for('test'))

    return render_template('createuserarea.html', form=form)


@app.route('/createdefaultadmin', methods=['GET', 'POST'])
@login_required
def createdefaultadmin():
    new_user = User(name="Admin", uuid="624fda32-5dd9-4600-bca2-9bd7cf1d6058", time=str(datetime.now()))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('test'))


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
        checklocation(uuid)
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
        response = user.uuid
        return jsonify(response), 200
    except:
        response = {}
        return jsonify(response), 400
    
def doorops(arg):
    match arg:
        case "open":
            print("open")
            # requests.get('http://127.0.0.1/api/open')
            time.sleep(5)
            doorops("close")
        case "close":
            print("close")
            # requests.get('http://127.0.0.1/api/close')


@app.route('/api/gettime', methods=['GET'])
def gettime():
    response = {
        'time': str(datetime.now())
    }
    return jsonify(response), 200

@app.route('/api/cameracapture', methods=['GET', 'POST'])
def cameracapture():
    user = User.query.filter_by(id=request.id.data()).first()
    user.camera = request.camera.data()
    user.capture = str(datetime.now())
    db.session.commit()
    response = {
        'status': 'success'
    }
    return jsonify(response), 200


def checklocation(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    user_id = user.id
    area_id = UserArea.query.filter_by(user_id=user_id).first().user_id
    door = Door.query.filter_by(area_id=area_id).first()
    if (door.drssi11 == user.Urssi1 and door.drssi12 == user.Urssi2 and door.drssi13 == user.Urssi3) or (door.drssi21 == user.Urssi1 and door.drssi22 == user.Urssi2 and door.drssi23 == user.Urssi3):
        thread = threading.Thread(target=doorops, args=("open",))
        thread.start()
    


# @app.after_request
# def add_header(response):
#     response.headers['Cache-Control'] = 'no-cache, no-store'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
