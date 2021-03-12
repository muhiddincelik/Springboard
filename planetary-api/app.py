from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
import os


# App configuration
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_PORT'] = 2525

# Initiate required services
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


# Function to create database
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created.')


# Function to create database
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped.')


# Insert sample record into the database
@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='mercury',
                     planet_type='Class D',
                     home_star='Sol',
                     mass=3.258e23,
                     radius=1516,
                     distance=35.98e6)

    venus = Planet(planet_name='venus',
                   planet_type='Class K',
                   home_star='Sol',
                   mass=4.867e24,
                   radius=3760,
                   distance=67.24e6)

    earth = Planet(planet_name='earth',
                   planet_type='Class M',
                   home_star='Sol',
                   mass=5.972e24,
                   radius=3959,
                   distance=92.96e6)

    # Add sample planets to db
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    # Create a User instance
    test_user = User(first_name='William',
                     last_name='Herschel',
                     email_name='wh@test.com',
                     password='wh@test.com')

    # Add sample user to db
    db.session.add(test_user)
    db.session.commit()  # To execute
    print('Database seeded.')


# User parameters in form
@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message='Sorry ' + name + ' you are not old enough.'), 401
    else:
        return jsonify(message='Welcome ' + name + ' you are old enough.')


# User parameters in url
@app.route('/url_variables/<name>/<age>')
def url_variables(name, age):
    if int(age) < 18:
        return jsonify(message='Sorry ' + name + ' you are not old enough.'), 401
    else:
        return jsonify(message='Welcome ' + name + ' you are old enough.')


# Get all planets
@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)


# Register a user
@app.route('/register', methods=['POST'])
def register():
    email = request.form['email_name']
    test = User.query.filter_by(email_name=email).first()
    if test:
        return jsonify(message='This email already registered!'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email_name=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User registered carefully!'), 201


# User login
@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email_name']
        password = request.json['password']
    else:
        email = request.form['email_name']
        password = request.form['password']

    test = User.query.filter_by(email_name=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login is successful!', access_token=access_token)
    else:
        return jsonify(message='Bad email or password!'), 401


# Retrieve password for a user
@app.route('/retrieve_password/<email_name>', methods=['GET'])
def retrieve_password(email_name):
    user = User.query.filter_by(email_name=email_name).first()
    if user:
        msg = Message("Your planetary API password is " + user.password,
                      sender="admin@planetary-api.com",
                      recipients=[email_name])
        mail.send(msg)
        return jsonify(message='Password sent to ' + email_name)
    else:
        return jsonify(message='Invalid email!'), 401


# Get the details of a specific planet
@app.route('/planet_details/<planet_id>', methods=["GET"])
def planet_details(planet_id):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    else:
        return jsonify(message='This planet does not exist!'), 404


# Adding a planet
@app.route('/add_planet', methods=['POST'])
@jwt_required()
def add_planet():
    planet_name = request.form['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify(message='There is already a planet with this name!'), 409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = float(request.form['mass'])
        radius = float(request.form['radius'])
        distance = float(request.form['distance'])

        new_planet = Planet(planet_name=planet_name,
                            planet_type=planet_type,
                            home_star=home_star,
                            mass=mass,
                            radius=radius,
                            distance=distance)

        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message='You added a planet!'), 201


# Updating a planet record
@app.route('/update_planet', methods=['PUT'])
@jwt_required()
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:  # If an existing planet
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = float(request.form['mass'])
        planet.radius = float(request.form['radius'])
        planet.distance = float(request.form['distance'])

        db.session.commit()
        return jsonify(message='You updated a planet!'), 202
    else:
        return jsonify(message='That planet does not exist!'), 404


# Removing a planet
@app.route('/remove_planet/<planet_id>', methods=['DELETE'])
@jwt_required()
def remove_planet(planet_id):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message="You deleted a planet!"), 202
    else:
        return jsonify(message="That planet does not exist!"), 404


# User class
class User(db.Model):
    __table_name__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email_name = Column(String, unique=True)
    password = Column(String)


# Planet class
class Planet(db.Model):
    __table_name__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


# User schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email_name', 'password')


# User schema
class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')


# Instantiate user and planet schema classes for single and many use cases
user_schema = UserSchema()
users_schema = UserSchema(many=True)
planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)


# Driver code
if __name__ == '__main__':
    app.run()
