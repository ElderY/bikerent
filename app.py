from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from app import app,db
# app.app_context().push()
# db.create_all()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bikerent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    matrikel = db.Column(db.Integer, nullable=False)
    bike_model = db.Column(db.String, nullable=False)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['POST', 'GET'])
def apply():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        street_address = request.form['street_address']
        postal_code = request.form['postal_code']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        matrikel = request.form['matrikel']
        bike_model = request.form['bike_model']

        post = Post(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, street_address=street_address, postal_code=postal_code, city=city, state=state, country=country, matrikel=matrikel, bike_model=bike_model)

        try:
            db.session.add(post)
            db.session.commit()
            db.session.close()
            return redirect('/')
        except:
            return 'ERROR'
    else:
        return render_template('apply.html')



@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':

    app.run(debug=True)

