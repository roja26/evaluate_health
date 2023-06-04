""" TO DO -:
1. Make README.md
"""

"""
NOTE -:
1. ID is the primary key and is unique for each user, accounts for duplicate user
2. Can only enter valid integer for age
3. To portray the use of JWT, I have used it in POST method of users route
   when a user is added, a token is generated and returned to the user
   which can be used to access,update or delete a user's data in users/id route
"""

from flask import Flask, request, jsonify
import mysql.connector
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecretkey'

mydb = mysql.connector.connect(
        host="localhost",
        user = "root",
        password = "",
        database = "eval_health"
    )
mycursor = mydb.cursor()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        print(token)
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods = ['GET'])
def home():
    if request.method == 'GET':
        return 'Welcome to CRUD tasks in Flask and MySQL!'

@app.route('/users', methods = ['POST', 'GET'])
def users():
    if request.method == 'GET': # done
        try:
            mycursor.execute('''SELECT * FROM users''')
            users = mycursor.fetchall()
            resp = jsonify(users)
            resp.status_code = 200
            return resp
        except Exception as e:
            print(e)
            resp = jsonify('Error fetching users!')
            resp.status_code = 404
            return resp
   
    if request.method == 'POST': # done
        try:
            id = request.json['id']
            firstname = request.json['firstname']
            lastname = request.json['lastname']
            age = request.json['age']
            try:
                age = int(age)
                if age < 0:
                    resp = jsonify('Please enter valid age')
                    resp._status_code = 404
                    return resp
            except:
                resp = jsonify('Please enter valid age')
                resp._status_code = 404
                return resp
            if id == '' or firstname == '' or lastname == '' or age == '':
                resp = jsonify('Please fill all the fields!')
                resp.status_code = 404
                return resp
            else:
                mycursor.execute('''INSERT into users VALUES(%s, %s, %s, %s)''', (id, firstname,lastname, age))
                mydb.commit()
                resp = jsonify('User added successfully!')
                resp.status_code = 200

                token = jwt.encode({'user': request.json['id'], 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
                return jsonify({'token': token.decode('UTF-8')})
                # return resp
        
        except Exception as e:
            print(e)
            resp = jsonify('Error adding user!')
            resp.status_code = 404
            return resp
    
@app.route('/users/<id>', methods = ['GET', 'PUT', 'DELETE'])
@token_required
def user(id):
    if request.method == 'GET': # done
        try:
            mycursor.execute('''SELECT * FROM users WHERE id = %s''', (id,))
            users = mycursor.fetchall()
            if len(users) == 0:
                resp = jsonify('User with id: {} not found'.format(id))
                resp.status_code = 404
                return resp
            else:
                resp = jsonify(users)
                resp.status_code = 200
                return resp
        except Exception as e:
            print(e)
            resp = jsonify('Error fetching user!')
            resp.status_code = 404
            return resp

    if request.method == 'PUT': # done
        try:
            firstname = request.json['firstname']
            lastname = request.json['lastname']
            age = request.json['age']
            if id == '' or firstname == '' or lastname == '' or age == '':
                resp = jsonify('Please fill all the fields!')
                resp.status_code = 404
                return resp
            else:
                mycursor.execute('''UPDATE users SET firstname = %s, lastname = %s, age = %s WHERE id = %s''', (firstname,lastname, age, id))
                mydb.commit()
                resp = jsonify('User updated successfully!')
                resp.status_code = 200
                return resp
        
        except Exception as e:
            print(e)
            resp = jsonify('Error updating user!')
            resp.status_code = 404
            return resp

    if request.method == 'DELETE': #done
        try:
            mycursor.execute('''DELETE FROM users WHERE id = %s''', (id,))
            mydb.commit()
            resp = jsonify('User deleted successfully!')
            resp.status_code = 200
            return resp
        except Exception as e:
            print(e)
            resp = jsonify('Error deleting user!')
            resp.status_code = 404
            return resp
    
if __name__ == "__main__":
    app.run(debug=True)
