# Evaluate_Health Task
- To Do - Create a simple API using Flask and interact with a MySQL database. The API should allow users to perform basic CRUD operations (Create, Read, Update, Delete) on a "users" table in the database.

## Pre-requisiste softwares
- Flask
- MySQL - mysql.connector, xampp
- Postman

## How to run the project ?
### For MySQL setup
- 1. Setup XAMPP in your system to run the mysql server
- 2. Get the MySQL Database and Apache Web Server Running
- 3. Visit `http://localhost/phpmyadmin/` in your browser and create a database = eval_health and table = users
### For Flask setup
- 1. Download <app.py> to your system
- 2. Run command `python3 -m flask run`
- 3. Website is locally hosted on `http://127.0.0.1:5000`
- 4. Enter the above URL in postman to test the API endpoints -> /user and /user/id

## Information
- in /user route
    - **GET** method displays all users details in the table users
    - **POST** method adds new user to table users
- in /user/id route
    - **GET** method displays details of user with id = id
    - **PUT** method updates details of user with id = id
    - **DELETE** method deleted user with id = id
- database name = eval_health, table name = users


