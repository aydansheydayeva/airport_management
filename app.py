from flask import Flask, render_template, make_response, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
import json, os, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local_db.db'
db = SQLAlchemy(app)
api = Api(app)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), nullable = False)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    city_from = db.Column(db.String(64), nullable = False)
    city_to = db.Column(db.String(64), nullable=False)
    departure_time = db.Column(db.String(64), nullable=False)
    arrival_time = db.Column(db.String(64), nullable=False)
    airplane = db.Column(db.String(64), nullable=False)
    passenger_number = db.Column(db.String(64), nullable=False)

    def __init__(self, city_from, city_to, departure_time, arrival_time, airplane, passenger_number):
        self.city_from = city_from
        self.city_to = city_to
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.airplane = airplane
        self.passenger_number = passenger_number


class User(Resource):
    def get(self, from_city, to_city):
        data_from_db = []
        flights = Flight.query.all()
        for flight in flights:
            if flight.city_from == from_city and flight.city_to == to_city:
                flightDict = {"city_from": flight.city_from, "city_to": flight.city_to, "departure": flight.departure_time, "arrival": flight.arrival_time, "airplane": flight.airplane, "passenger_number": flight.passenger_number}
                data_from_db.append(flightDict)
    
        return data_from_db

class DBINFO(Resource):
    def get(self):
        data_from_db = []
        flights = Flight.query.all()
        for flight in flights:
            flightDict = {"id": flight.id, "city_from": flight.city_from, "city_to": flight.city_to, "departure": flight.departure_time, "arrival": flight.arrival_time, "airplane": flight.airplane, "passenger_number": flight.passenger_number}
            data_from_db.append(flightDict)

        return data_from_db

##########
tokens = []
##########

class Login(Resource):
    def post(self):
        admin_args = reqparse.RequestParser()
        admin_args.add_argument("email", type = str, help = "admin email")
        admin_args.add_argument("password", type = str, help = "admin password")
        args = admin_args.parse_args()
        admins = Admin.query.all()
        token = '' 
        for admin in admins:
            if admin.email == args.email and admin.password == args.password:
                tokenn = random.randint(0, 9999999999999)
                token = str(tokenn)

        tokens.append(token)
        return [{"token": token}]

class Options(Resource):
    def post(self):
        admin_args = reqparse.RequestParser()
        admin_args.add_argument("fromm", type = str, help = "from")
        admin_args.add_argument("to", type = str, help = "to")
        admin_args.add_argument("t1", type = str, help = "time1")
        admin_args.add_argument("t2", type = str, help = "time2")
        admin_args.add_argument("a_info", type = str, help = "airplane info")
        admin_args.add_argument("p_num", type = str, help = "passenger number")
        admin_args.add_argument("token", type = str, help = "token")
        args = admin_args.parse_args()
        if (args.token in tokens):
            obj = Flight(city_from=args.fromm, city_to=args.to, departure_time=args.t1, arrival_time=args.t2, airplane=args.a_info, passenger_number=args.p_num)
            db.session.add(obj)
            db.session.commit()
        else:
            print("Not authorized!!!")

    def delete(self):
        admin_args = reqparse.RequestParser()
        admin_args.add_argument("id", type = str, help = "id")
        admin_args.add_argument("token", type = str, help = "token")
        args = admin_args.parse_args()
        if(args.token in tokens):
            flightt = Flight.query.filter_by(id=args.id).first()
            db.session.delete(flightt)
            db.session.commit()
        else:
            print('Not authorized!!!')

    def put(self):
        admin_args = reqparse.RequestParser()
        admin_args.add_argument("id", type = str, help = "id")
        admin_args.add_argument("fromC", type = str, help = "from")
        admin_args.add_argument("toC", type = str, help = "to")
        admin_args.add_argument("time1", type = str, help = "time1")
        admin_args.add_argument("time2", type = str, help = "time2")
        admin_args.add_argument("aInfo", type = str, help = "airplane info")
        admin_args.add_argument("psngrNum", type = str, help = "passenger number")
        admin_args.add_argument("token", type = str, help = "token")
        args = admin_args.parse_args()
        if (args.token in tokens):
            print(args)
            flightt = Flight.query.filter_by(id=args.id).first()
            flightt.city_from = args.fromC
            flightt.city_to=args.toC
            flightt.departure_time=args.time1
            flightt.arrival_time=args.time2
            flightt.airplane=args.aInfo
            flightt.passenger_number=args.psngrNum
            db.session.commit()
        else:
            print("Not authorized!!!")


class Termination(Resource):
    def delete(self):
        admin_args = reqparse.RequestParser()
        admin_args.add_argument("token", type = str, help = "token")
        args = admin_args.parse_args()
        if(args.token in tokens):
            tokens.remove(args.token)
            if(args.token not in tokens):
                print('session teminated')

def main():

    db.create_all()

    api.add_resource(User, "/flights/<from_city>/<to_city>")    #get
    api.add_resource(Login, "/authentication_authorization")  #post
    api.add_resource(Options, "/flights")   #post, delete, put
    api.add_resource(Termination, "/end_session")  #delete

    api.add_resource(DBINFO, "/dbInfo")   #all db info

    # CREATE admins_table
    fa = open('./json_files/admins.json')
    admins = json.load(fa)

    db.create_all()
    for admin in admins:
        adminObj = Admin(email=admin['email'], password=admin['password'])
        db.session.add(adminObj)

    # CREATE flights_table
    ff = open('./json_files/flights.json')
    flights = json.load(ff)

    for flight in flights:
        flightObj = Flight(city_from=flight['city_from'], city_to=flight['city_to'], departure_time=flight['departure_time'], arrival_time=flight['arrival_time'], airplane=flight['airplane'], passenger_number=flight['passenger_number'])
        db.session.add(flightObj)

    db.session.commit()
    app.run()

if __name__ == "__main__":
    main()