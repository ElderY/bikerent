from __future__ import annotations
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, func, DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from typing import List
import random


# from app import app,db, Post, Inventory, Rentals
# app.app_context().push()
# db.create_all()
# import random
# i = 0
# while i < 25:
#     bike = Inventory(model_name='CityClassic', frame_number=random.randint(1000, 5000), status = 'available', condition='new')
#     db.session.add(bike)
#     i += 1
# db.session.commit()





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bikerent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


class Rentals(db.Model):
    __tablename__ = 'rentals'
    rental_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    bike_id: Mapped[int] = mapped_column(ForeignKey('inventory.id'), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey('requests.id'), nullable=False, unique=True)

    start_date: Mapped[int] = mapped_column(default=func.now())
    end_date: Mapped[int] = mapped_column(nullable=True)

    bike: Mapped["Inventory"] = relationship(back_populates="rentals")
    student_request: Mapped["Post"] = relationship(back_populates="rentals")


class Inventory(db.Model):
    __tablename__ = 'inventory'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    model_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    frame_number: Mapped[int] = mapped_column(db.String(100), nullable=False)
    status: Mapped[str] = mapped_column(db.String(100), nullable=False, default='available')
    condition: Mapped[str] = mapped_column(db.String(100), nullable=False)

    rentals: Mapped[list["Rentals"]] = relationship(back_populates="bike")


class Post(db.Model):
    __tablename__ = 'requests'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(nullable=False, default='PENDING')
    first_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    phone_number: Mapped[int] = mapped_column(nullable=False)
    street_address: Mapped[str] = mapped_column(db.String(100), nullable=False)
    postal_code: Mapped[int] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(db.String(100), nullable=False)
    state: Mapped[str] = mapped_column(db.String(100), nullable=False)
    country: Mapped[str] = mapped_column(db.String(100), nullable=False)
    matrikel: Mapped[int] = mapped_column(nullable=False, unique=True)
    bike_model: Mapped[str] = mapped_column(db.String(100), nullable=False)

    rentals: Mapped[list["Rentals"]] = relationship(back_populates="student_request")


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

@app.route('/dashboard')
def dashboard():
    all_requests = Post.query.all()
    pending_requests = Post.query.filter(Post.status == 'PENDING').count()
    active_rentals = Rentals.query.filter_by(end_date=None).all()
    total = Inventory.query.count()
    free = Inventory.query.filter_by(status='available').count()
    return render_template('dashboard.html',
                           requests=all_requests,
                           pending=pending_requests,
                           rentals=active_rentals,
                           total=total,
                           free=free
                           )

@app.route('/approve_request/<int:req_id>')
def approve_request(req_id):
    request_to_approve = Post.query.get_or_404(req_id)
    bike = Inventory.query.filter_by(model_name=request_to_approve.bike_model, status='available').first()

    if not bike:
        return "Error: Keine verfügbaren Fahrräder dieses Modells!", 400

    try:
        new_rental = Rentals(bike=bike, student_request=request_to_approve)
        bike.status = 'BUSY'
        request_to_approve.status = 'APPROVED'
        db.session.add(new_rental)
        db.session.commit()
        db.session.close()
        return redirect('/dashboard')

    except Exception as e:
        db.session.rollback()
        return f"Datenbankfehler: {str(e)}", 500

    else:
        return render_template('dashboard.html')


if __name__ == '__main__':

    app.run(debug=True)

