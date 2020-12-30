# Airport Management - Flask Restful API

This is a CLI based server-client application that accepts two roles from client side: user and admin. 

If role is user, then there is only an option of viewing all flights by making a request to http://127.0.0.1:5000/flights/<city_from>/<city_to>.

In order to have admin privileges, user should login with email and password (this data is generated from .json file automatically as soon as program starts). When the role is admin, the there are 4 options:
1. Adding data to database

(POST request to http://127.0.0.1:5000/flights/)

2. Updating data in database.

(PUT request to http://127.0.0.1:5000/flights)

3. Deleting data from database.

(DELETE request to http://127.0.0.1:5000/flights)

4. Terminating current admin session.
(DELETE request to http://127.0.0.1:5000/end_session)

In login, client makes POST request to http://127.0.0.1:5000/authentication_authorization

## Installation

To download app, you need to type following command:

```bash
git clone https://github.com/aydansheydayeva/airport_management
```
 Then install requirements to have all packets needed for this project:

```bash
pip install requirements.txt
```

## Usage

To use this app, 2 terminals should be opened. Next 2 commands should be run in terminals:

**Server terminal:**
```
python3 app.py
```


**Client terminal:**
```
python3 client.py
```

Service is running on port 5000 at 127.0.0.1.

- OOP approach is used in implementation.

- Flask SQLAlchemy is used for database management.

## Example of client-side commands
- to POST data into db

Type command: POST Mexico Baku may_15,09:00am may_15,23:59pm airplane_5 566

- to DELETE record by ID

Type command: DELETE 6

- to UPDATE database info

Type command: PUT 9

new city_from: city1

new city_to: city2

new departure_time: august_31,09:00am

new arrival_time: august_31,15:10pm

new airplane_info: airplane_5

new passengerNumber: 350

- to end SESSION

Type command: END_SESSION

- using app as simple user

Role (user or admin): user

city_from: Baku

city_to: Ganja


Terminate both terminals with Ctrl+C
