#references:
#basic login/register page
#https://www.youtube.com/watch?v=fOj16SIa02U&list=LL&index=3
#https://www.youtube.com/watch?v=zjvfeho2890&list=LL&index=4
#https://www.youtube.com/watch?v=bxyaJ8w_wak&t=213s
#https://www.youtube.com/watch?v=aV8YSefG1fw

#validation
#https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
#https://stackoverflow.com/questions/65915695/how-do-i-make-sql-python-find-if-a-full_name-is-already-in-the-database
#https://python-forum.io/thread-7016.html

#connecting database
#https://www.youtube.com/watch?v=WeslBREciKY&t=153s
#https://www.youtube.com/watch?v=nrG0tKSYMHc&t=295s

#login issues
#https://tedboy.github.io/flask/generated/werkzeug.check_password_hash.html 
#https://stackoverflow.com/questions/46723767/how-to-get-current-user-when-implementing-python-flask-security - returning a full_name
#https://stackoverflow.com/questions/59380641/how-to-display-full_name-in-multiple-pages-using-flask

#Session permanence
#https://stackoverflow.com/questions/37227780/flask-session-persisting-after-close-browser

#insertion / updating text
#https://stackoverflow.com/questions/42554368/python-flask-inserting-data-from-form
#https://stackoverflow.com/questions/12277933/send-data-from-a-textbox-into-flask
#https://stackoverflow.com/questions/61625715/how-to-write-input-from-input-box-from-a-flask-website-into-a-csv-or-txt-file

#Updating profile
#https://www.youtube.com/watch?v=1G2Uk_RAZqE
#https://www.youtube.com/watch?v=o6YjyOt2Zhc&t=135s


#connecting Stripe to web app
#https://www.youtube.com/watch?v=jMX74n-TwF4
#https://www.youtube.com/watch?v=6plVs_ytIH8
#https://stripe.com/
#https://www.youtube.com/watch?v=6O8LTwVfTVs
#https://www.youtube.com/watch?v=uZgRbnIsgrA
#https://stripe.com/docs
#https://github.com/stripe/stripe-python

#Uploading / Deleting images
#https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
#https://www.youtube.com/watch?v=2De9Lu9tReg
#https://www.youtube.com/watch?v=YLptAhf3wwM&t=963s
#https://www.geeksforgeeks.org/python-os-remove-method/

#Imports for functionality of the server / backend
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, request, render_template
from flask import request, jsonify
from datetime import datetime
import re
import stripe
import os
import json
import logging

#Start -code by prakash

app = Flask(__name__, static_url_path="", static_folder="public")

# Stripe API Keys 
stripe.api_key = "sk_test_51QtHxkE9I53MxGEG7q4d6GghW7i88Wdb1ddzxsahEuswMEzNK1qW2EO3RWguhlwcEWOzZAyXl8SwsKSnwzP0Gln700uKNfydfi"

# Your website domain
YOUR_DOMAIN = "http://localhost:5000"
app.config['STRIPE_PUBLIC_KEY'] = "pk_test_51QtHxkE9I53MxGEGGlW18Yii7C5kQ70WVsj8fZCkHqk5U8MPND3NhLMp1ETOvIDYXeOdpkxbbTB91HiP51RH9dPv00C71btimR"

#Start -code by prakash






#START: CODE COMPLETED BY CHRISTIAN
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

logging.basicConfig(level=logging.INFO)

#Uploading files

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg,'}
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')





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


def phoneNumRange(phone_number):
    return re.match(r"^\d{10}$",phone_number)


    


#If the user is logged in, it will send them to their designated dashboard, otherwise the homepage
@app.route("/")
def home():
    if "user_id" in session:
        if(session["role"] == "customer"):
            return redirect(url_for("customer"))
        elif(session["role"] == "driver"):
            return redirect(url_for("driver"))
        elif(session["role"] == "food_owner"):
            return redirect(url_for("foodOwner"))
        
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
            return redirect(url_for("foodOwner"))
        
    if request.method == "GET":
        return render_template("register.html")
    
    else:
        #grabs the information from the form textfield and makes it into variables
        full_name = request.form["full_name"]
        password = request.form["password"]
        email = request.form["email"]
        role = request.form["role"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]

        #used to encrypt password for security
        hashPass = generate_password_hash(password)

        #validation for inputs
        
        if not emailValidation(email):
            flash("Email is in an invalid format")
            return redirect(url_for("register"))
        
        elif email_exists(email):
            flash("Email is already registered")
            return redirect(url_for("register"))
        
        elif not phoneNumRange(phone_number):
            flash("Phone number out of range")
            return redirect(url_for("register"))
        

        
 #code started by prakash#

 # If the user is a driver, create a Stripe Checkout Session
        if role == "driver":
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                            "price_data": {
                                "currency": "usd",
                                "product_data": {
                                    "name": "Driver Joining Fee",
                                },
                                "unit_amount": 1000,  # Joining fee in cents (e.g., $10.00)
                            },
                            "quantity": 1,
                        }
                    ],
                    mode="payment",
                    success_url=url_for("success", _external=True),
                    cancel_url=url_for("register", _external=True),
                   metadata={
                        "full_name": full_name,
                        "email": email,
                        "password": hashPass,  # Store the hashed password in metadata
                        "role": role,
                        "phone_number": phone_number,
                        "address": address,
                    },
                )
                return redirect(checkout_session.url, code=303)
            except stripe.error.StripeError as e:
                flash(f"Payment failed: {str(e)}")
                return redirect(url_for("register"))

        #code end by prakash#





        #inserts the data into the database
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Users (full_name, email, password, role, phone_number, address) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (full_name, email, hashPass, role, phone_number, address))
        mysql.connection.commit()
      
        
        #Depending on the role, specific data will be placed into that role
        if(role == "customer"):
            cursor.execute("INSERT INTO Customers (full_name, phone_number,address) VALUES (%s, %s, %s)", 
                       (full_name, phone_number, address))
            mysql.connection.commit()

        elif(role == "driver"):
            cursor.execute("INSERT INTO Drivers (full_name, phone_number) VALUES (%s, %s)", 
                       (full_name, phone_number))
            mysql.connection.commit()

        elif(role == "food_owner"):
            cursor.execute("INSERT INTO FoodOwners (full_name, phone_number) VALUES (%s, %s)", 
                       (full_name, phone_number))
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
            return redirect(url_for("foodOwner"))
        
    
        
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
            session["full_name"] = user["full_name"]
            session["email"] = user["email"]
            session["role"] = user["role"]
            session["phone_number"] = user["phone_number"]
            session["address"] = user["address"]
            session.permanent = True
            if(session["role"] == "customer"):
                return redirect(url_for("customer"))
            elif(session["role"] == "driver"):
                return redirect(url_for("driver"))
            else:
                return redirect(url_for("foodOwner"))

        
        return render_template("login.html")
        




#pages / dashboards for each role
@app.route('/customer')
def customer():
    return render_template("customer.html")

@app.route('/driver')
def driver():
    return render_template("driver.html")

@app.route('/foodOwner')
def foodOwner():
    return render_template("foodOwner.html")

#END: CODE COMPLETED BY CHRISTIAN






#START: CODE COMPLETED BY PRAKASH


@app.route("/stripe_webhook", methods=["GET", "POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, "whsec_MyZAqVSQzHVCuEAYL3CaTyBwXJNgDddj"  # Replace with your webhook secret
        )
    except ValueError as e:
        logging.error(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        logging.error(f"SignatureVerificationError: {str(e)}")
        return jsonify({"error": str(e)}), 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})

        # Extract common details from metadata
        full_name = metadata.get("full_name")
        email = metadata.get("email")
        password = metadata.get("password")
        role = metadata.get("role")
        phone_number = metadata.get("phone_number")
        address = metadata.get("address")

        # Save user details to the database
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO Users (full_name, email, password, role, phone_number, address) VALUES (%s, %s, %s, %s, %s, %s)",
                           (full_name, email, password, role, phone_number, address))
            mysql.connection.commit()

            if role == "driver":
                # Save driver details
                cursor.execute("INSERT INTO Drivers (full_name, phone_number) VALUES (%s, %s)",
                               (full_name, phone_number))
                mysql.connection.commit()
                logging.info(f"Driver {full_name} ({email}) created successfully.")

            elif role == "foodOwner":
                # Save food owner details
                cursor.execute("INSERT INTO FoodOwners (full_name, phone_number) VALUES (%s, %s)",
                               (full_name, phone_number))
                mysql.connection.commit()
                logging.info(f"Food Owner {full_name} ({email}) created successfully.")

        except Exception as e:
            logging.error(f"Error saving user data: {str(e)}")
            mysql.connection.rollback()
        finally:
            cursor.close()

    # Handle subscription events
    elif event["type"] == "invoice.payment_succeeded":
        # Handle subscription renewal for food owners
        invoice = event["data"]["object"]
        stripe_subscription_id = invoice["subscription"]
        subscription = stripe.Subscription.retrieve(stripe_subscription_id)

        # Extract subscription details
        plan_name = subscription["plan"]["nickname"]
        amount = subscription["plan"]["amount"]
        start_date = datetime.fromtimestamp(subscription["current_period_start"])
        end_date = datetime.fromtimestamp(subscription["current_period_end"])
        next_payment_date = datetime.fromtimestamp(subscription["current_period_end"])

        # Save subscription details to the database
        cursor = mysql.connection.cursor()

        try:
            cursor.execute("INSERT INTO Subscriptions (food_owner_id, stripe_subscription_id, plan_name, amount,payment_status, start_date, end_date, next_payment_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (session["food_owner_id"], stripe_subscription_id, plan_name, amount, "active", start_date, end_date, next_payment_date))
            mysql.connection.commit()
            logging.info(f"Subscription {stripe_subscription_id} updated successfully.")
        except Exception as e:
            logging.error(f"Error saving subscription data: {str(e)}")
            mysql.connection.rollback()
        finally:
            cursor.close()

    return jsonify({"success": True}), 200





@app.route('/Cprofile', methods=["GET", "POST"])
def Cprofile():
    return render_template("Cprofile.html", full_name=session["full_name"], email=session["email"], phone_number=session["phone_number"], address=session["address"])

@app.route('/schedulePickup')
def schedulePickup():
    return render_template("schedulePickup.html")

@app.route('/foodMarketplace')
def foodMarketplace():
    return render_template("foodMarketplace.html")

# Customer payment Page - One-Time Payment
@app.route('/Cpayment')
def Cpayment():
    return render_template("Cpayment.html")  # One-time payment page


# Create Checkout Session for One-Time Payment
@app.route("/create-checkout-session-one-time", methods=["GET", "POST"])
def create_checkout_session_one_time():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "One-Time Purchase",
                        },
                        "unit_amount": 500,  # $5.00
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{YOUR_DOMAIN}/success",
            cancel_url=f"{YOUR_DOMAIN}/cancel"
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e), 400



@app.route('/Dprofile', methods=["GET", "POST"])
def Dprofile():
    return render_template("Dprofile.html", full_name=session["full_name"], email=session["email"], phone_number=session["phone_number"], address=session["address"])

@app.route('/pickupRequest')
def pickupRequest():
    return render_template("pickupRequest.html")

@app.route('/earningReport')
def earningReport():
    return render_template("earningReport.html")

@app.route('/Fprofile', methods=["GET", "POST"])
def Fprofile():
    return render_template("Fprofile.html", full_name=session["full_name"], email=session["email"], phone_number=session["phone_number"], address=session["address"])


# Subscription Page
@app.route('/Subscribe')
def subscription():
    return render_template("subscription.html") # Subscription payment page


# Create Checkout Session for Subscription
@app.route("/create-checkout-session-subscription", methods=["GET", "POST"])
def create_checkout_session_subscription():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": "price_1QtIH1E9I53MxGEGrg7Sfvx8",  # recurring price ID from Stripe
                    "quantity": 1
                }
            ],
            mode="subscription",
            success_url=f"{YOUR_DOMAIN}/success",
            cancel_url=f"{YOUR_DOMAIN}/cancel"
        
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e), 400


# Success Page
@app.route("/success")
def success():
    return render_template("success.html")

# Cancel Page
@app.route("/cancel")
def cancel():
    return render_template("cancel.html", message="Your payment was unsuccessful. Please try again.")



#END: CODE COMPLETED BY PRAKASH

#START: CODE COMPLETED BY CHRISTIAN
@app.route("/updateCProfile", methods=["GET", "POST"])
def updateCProfile():
    if request.method == "GET":
        return render_template("updateCProfile.html")
    else:
        email = request.form["email"]
        full_name = request.form["full_name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]

        if email_exists(email):
            flash("Email is already registered, please try again")
            return redirect(url_for("updateCProfile"))
        
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Users SET email = %s, full_name = %s, phone_number = %s, address = %s WHERE user_id = %s",
                       (email, full_name, phone_number, address, session["user_id"]))
        mysql.connection.commit()
        cursor.close()

        #logs the user out
        session.clear()
        flash("Profile Updated! Log back in to see updates")
        return redirect(url_for("login"))

@app.route("/updateDProfile", methods=["GET", "POST"])
def updateDProfile():
    if request.method == "GET":
        return render_template("updateDProfile.html")
    else:
        email = request.form["email"]
        full_name = request.form["full_name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]

        if email_exists(email):
            flash("Email is already registered")
            return redirect(url_for("updateDProfile"))

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Users SET email = %s, full_name = %s, phone_number = %s, address = %s WHERE user_id = %s",
                       (email, full_name, phone_number, address, session["user_id"]))
        mysql.connection.commit()
        cursor.close()

        #logs the user out
        session.clear()
        flash("Profile Updated! Log back in to see updates")
        return redirect(url_for("login"))

@app.route("/updateFProfile", methods=["GET", "POST"])
def updateFProfile():
    if request.method == "GET":
        return render_template("updateFProfile.html")
    else:
        email = request.form["email"]
        full_name = request.form["full_name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]

        if email_exists(email):
            flash("Email is already registered")
            return redirect(url_for("updateFProfile"))
        
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Users SET email = %s, full_name = %s, phone_number = %s, address = %s WHERE user_id = %s",
                       (email, full_name, phone_number, address, session["user_id"]))
        mysql.connection.commit()
        cursor.close()

        #logs the user out
        session.clear()
        flash("Profile Updated! Log back in to see updates")
        return redirect(url_for("login"))
    

@app.route('/postPromotion', methods =["GET", "POST"])
def postPromotion():

    #Used to create the Jinja template / display each image in promotion page
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, image, caption FROM Promotions")
        promotions = cursor.fetchall()
        return render_template("postPromotion.html", promotions=promotions)
    
    else:
        #Validation 
        if request.method == 'POST':
            image = request.files['image']
            if image.filename == '':
                flash('No selected file')
                return redirect(url_for('postPromotion')) 
            
            if image:
                #Creates a filepath of uploads\x.jpg 
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(filepath)
                uploadFilePath= os.path.join('uploads', image.filename)

                # Insert image into database with a caption
                cursor = mysql.connection.cursor()
                caption = request.form.get('caption')
                cursor.execute("INSERT INTO Promotions (image, caption) VALUES (%s, %s)", (uploadFilePath, caption))
                mysql.connection.commit()
                cursor.close()
                
                flash('Image uploaded successfully')
                return redirect(url_for('postPromotion'))



#Used to remove a specific image from the Uploads folder, from the website and from the database
@app.route('/deleteImage/<int:id>')
def deleteImage(id):
    #Used to get root directory of every computer, so it can access the TeamProject folder
    root = os.path.dirname(os.path.abspath(__file__))
        
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT image FROM Promotions WHERE id = %s", (id,))
    imageFile = cursor.fetchone()
    imageFileName = imageFile['image'] #Grabs the image column from Promotions table
    

    imagePath = os.path.join(root,'static', imageFileName)
    os.remove(imagePath)

    cursor.execute("DELETE FROM Promotions WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for("postPromotion"))

        
        
         
        

    


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))
  
#makes it so that it only runs the app when executed
if __name__ == "__main__":
    app.run(debug=True) #updates in real-time + shows bugs / errors on CMD

#END: CODE COMPLETED BY CHRISTIAN
