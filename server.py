#references:
#basic login/register page
#https://www.youtube.com/watch?v=fOj16SIa02U&list=LL&index=3
#https://www.youtube.com/watch?v=zjvfeho2890&list=LL&index=4
#https://www.youtube.com/watch?v=bxyaJ8w_wak&t=213s
#https://www.youtube.com/watch?v=aV8YSefG1fw

#validation
#https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
#https://stackoverflow.com/questions/65915695/how-do-i-make-sql-python-find-if-a-username-is-already-in-the-database
#https://python-forum.io/thread-7016.html

#connecting database
#https://www.youtube.com/watch?v=WeslBREciKY&t=153s
#https://www.youtube.com/watch?v=nrG0tKSYMHc&t=295s

#login issues
#https://tedboy.github.io/flask/generated/werkzeug.check_password_hash.html 
#https://stackoverflow.com/questions/46723767/how-to-get-current-user-when-implementing-python-flask-security - returning a username
#https://stackoverflow.com/questions/59380641/how-to-display-username-in-multiple-pages-using-flask

#Session permanence
#https://stackoverflow.com/questions/37227780/flask-session-persisting-after-close-browser

#insertion / updating text
#https://stackoverflow.com/questions/42554368/python-flask-inserting-data-from-form
#https://stackoverflow.com/questions/12277933/send-data-from-a-textbox-into-flask
#https://stackoverflow.com/questions/61625715/how-to-write-input-from-input-box-from-a-flask-website-into-a-csv-or-txt-file

#Imports for functionality of the server / backend
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re











#Used to access the Database / keep users logged in 
app = Flask(__name__, template_folder='templates')
app.config["SESSION_PERMANENT"] = True
app.config['MYSQL_HOST'] = 'viaduct.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'WrwOIlogTwAShYIOsHGKQveeLHfVNxwy'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 13847
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = "test"



mysql = MySQL(app)



#Validation definitions

#Email format: xxx@yyy.com or abc.def@123.co.uk
def emailValidation(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

def email_exists(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

def username_exists(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user
    


#If the user is logged in, it will send them to their designated dashboard, otherwise the homepage
@app.route("/")
def home():
    if "user_id" in session:
        if(session["role"] == "customer"):
            return redirect(url_for("customer"))
        elif(session["role"] == "driver"):
            return redirect(url_for("driver"))
        elif(session["role"] == "food_owner"):
            return redirect(url_for("promoter"))
        
    else:
        return render_template("home.html")


#Used to register users accounts (GET is used to display and POST is used to store data)
@app.route("/register", methods=["GET","POST"])
def register():

    #displays the register page 
    if "user_id" in session:
        if(session["role"] == "customer"):
            flash("You must log out to create another account")
            return redirect(url_for("customer"))
        
        elif(session["role"] == "driver"):
            flash("You must log out to create another account")
            return redirect(url_for("driver"))
        
        elif(session["role"] == "food_owner"):
            flash("You must log out to create another account")
            return redirect(url_for("promoter"))
        
    if request.method == "GET":
        return render_template("register.html")
    
    else:
        #grabs the information from the form textfield and makes it into variables
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        role = request.form["role"]

        #used to encrypt password for security
        hashPass = generate_password_hash(password)

        #validation for inputs
        
        if not emailValidation(email):
            flash("Email is in an invalid format")
            return redirect(url_for("register"))
        
        elif email_exists(email):
            flash("Email is already registered")
            return redirect(url_for("register"))
        
        elif username_exists(username):
            flash("Username already exists")
            return redirect(url_for("register"))
        
       


        
        
        
        #inserts the data into the database
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Users (username, email, password, role) VALUES (%s, %s, %s, %s)", 
                       (username, email, hashPass, role))
        mysql.connection.commit()
        cursor.close()
        flash("Account created successfully!")

        
        return render_template("register.html")
        

        
    
@app.route('/login', methods = ["GET", "POST"])
def login():
    #displays the login page 
    if "user_id" in session:
        if(session["role"] == "customer"):
            flash("You are already logged in")
            return redirect(url_for("customer"))
            
        elif(session["role"] == "driver"):
            flash("You are already logged in")
            return redirect(url_for("driver"))
        
        elif(session["role"] == "food_owner"):
            flash("You are already logged in")
            return redirect(url_for("promoter"))
        
    
        
    if request.method == "GET":
        return render_template("login.html")
    
    
    else:
        email = request.form["email"]
        password = request.form["password"]
        

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        #Validation for inputs
        if not email or not password:
            flash("You must type in an email AND a password")

        elif not user:
            flash("Invalid email address")
        
        #used if you forget the user password: elif password != user["password"]
        elif not check_password_hash(user["password"],password):
            flash("Invalid password")

        
            
        #depending on the type of role, it will send you to a certain dashboard
        else:
            #keeps the user logged in, even when browser is closed
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["email"] = user["email"]
            session["role"] = user["role"]
            session.permanent = True
            if(session["role"] == "customer"):
                return redirect(url_for("customer"))
            elif(session["role"] == "driver"):
                return redirect(url_for("driver"))
            else:
                return redirect(url_for("promoter"))

        
        return render_template("login.html")
        
    
@app.route('/basket')
def basket():
    return render_template("basket.html")

@app.route('/recycle')
def recycle():
     return render_template("recycle.html")



@app.route('/profile', methods=["GET", "POST"])
def profile():
    
    #If the user is not logged in, display this
    if "user_id" not in session:
        flash("You must have created an account to view the profile page")
        return render_template('home.html')

    

    #same method as register, used to grab the details from Database and insert them into the form textfields    
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"] 

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Users (username, email) VALUES (%s, %s,)", 
                            (username, email))
        mysql.connection.commit()
        cursor.close()

    return render_template("profile.html", username=session["username"], email=session["email"])

#pages / dashboards for each role
@app.route('/customer')
def customer():
    return render_template("customer.html")

@app.route('/driver')
def driver():
    return render_template("employee.html")

@app.route('/promoter')
def promoter():
    return render_template("promoter.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))
    
    
#makes it so that it only runs the app when executed
if __name__ == "__main__":
    app.run(debug=True) #updates in real-time + shows bugs / errors on CMD
