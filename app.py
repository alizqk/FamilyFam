from flask import Flask, render_template, redirect, request, session
import sqlite3


app = Flask(__name__)
app.secret_key = "Super Secret"

db = sqlite3.connect("FriendlyFamDB.db")

cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, username VARCHAR(52), password VARCHAR(128))")
cursor.execute("CREATE TABLE IF NOT EXISTS events (id INT PRIMARY KEY, host VARCHAR(52), description VARCHAR(128), day VARCHAR(53), time VARCHAR(53), status VARCHAR(53))")
db.commit()
db.close()
@app.route('/')
def index():
    if "username" in session:
        return redirect("/home")
    return render_template("index.HTML")

@app.route('/signup',  methods=["post", "get"])
def signup():
    message = ''
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        connection = sqlite3.connect("FriendlyFamDB.db")
        cursor = connection.cursor()
        if len(username) <= 5:
            message = "username is too short"
            return render_template("signup.html", message=message) 
        temp = cursor.execute(f'''SELECT username from users where username = "{username}"''').fetchall()
        if len(temp) == 0:
            cursor.execute(f'''INSERT into users (username, password) values("{username}", "{password}")''')  
            connection.commit()
            connection.close()
            return redirect('/login') 
        connection.close()
        return render_template("signup.html", message="user already exists")
    return render_template("signup.html")
 
@app.route('/login',  methods=["post", "get"])
def login():    
    username = request.form.get("username")
    connection = sqlite3.connect("FriendlyFamDB.db")
    cursor = connection.cursor()
    password = request.form.get("password")
    temp = cursor.execute(f'''SELECT username from users where username = "{username}" and password = "{password}" ''').fetchone()
    connection.close()
    if temp == None:
            message = "incorrect username or password"
            return render_template("index.HTML", message=message)

    else: 
            message = "incorrect username or password"
    if request.method == "GET":
        return render_template("index.html", message=message)
    return render_template("index.HTML")     


#this is a modification

if __name__ == "__main__":
    import os
    HOST = os.environ.get('SERVER_HOST','localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555   
    app.run(HOST, PORT, debug=True)