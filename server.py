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


#Flash
#https://flask.palletsprojects.com/en/stable/patterns/flashing/
#https://stackoverflow.com/questions/44569040/change-color-of-flask-flash-messages

#Imports for functionality of the server / backend
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, request, render_template
from flask import request, jsonify
from datetime import datetime, timedelta
from datetime import date
import re
import stripe
import os
import json
import logging
import random, string







#app = Flask(__name__, static_url_path="", static_folder="public")

# Stripe API Keys 
stripe.api_key = "sk_test_51QtHxkE9I53MxGEG7q4d6GghW7i88Wdb1ddzxsahEuswMEzNK1qW2EO3RWguhlwcEWOzZAyXl8SwsKSnwzP0Gln700uKNfydfi"









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

# Your website domain
YOUR_DOMAIN = "http://localhost:5000"
app.config['STRIPE_PUBLIC_KEY'] = "pk_test_51QtHxkE9I53MxGEGGlW18Yii7C5kQ70WVsj8fZCkHqk5U8MPND3NhLMp1ETOvIDYXeOdpkxbbTB91HiP51RH9dPv00C71btimR"

mysql = MySQL(app)

logging.basicConfig(level=logging.INFO)

#Uploading files

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value)
    except Exception as e:
        # Optionally log e for debugging
        return []  # Return an empty list if parsing fails


@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value)
    except Exception:
        return {}


# Inject datetime so we can use it for time conversion
@app.context_processor
def inject_datetime():
    return dict(datetime=datetime)

@app.template_filter('strftime')
def format_datetime(value, fmt="%H:%M"):
    return value.strftime(fmt)


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
            flash("You must log out to create another account", 'error')
            return redirect(url_for("customer"))
        
        elif(session["role"] == "driver"):
            flash("You must log out to create another account", 'error')
            return redirect(url_for("driver"))
        
        elif(session["role"] == "food_owner"):
            flash("You must log out to create another account", 'error')
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
            flash("Email is in an invalid format", 'error')
            return redirect(url_for("register"))
        
        elif email_exists(email):
            flash("Email is already registered", 'error')
            return redirect(url_for("register"))
        
        elif not phoneNumRange(phone_number):
            flash("Phone number out of range", 'error')
            return redirect(url_for("register"))
        

        
 
        
        cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO Users (full_name, email, password, role, phone_number, address) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (full_name, email, hashPass, role, phone_number, address))
        mysql.connection.commit()
      
        
        #Depending on the role, specific data will be placed into that role
        if(role == "customer"):
            cursor.execute("INSERT INTO Customers (full_name, phone_number,address) VALUES (%s, %s, %s)", 
                       (full_name, phone_number, address))
            mysql.connection.commit()

        elif role == "driver":
            cursor.execute("INSERT INTO Drivers (full_name, phone_number) VALUES (%s, %s)",
                       (full_name, phone_number))
            mysql.connection.commit()

        

        elif(role == "food_owner"):
            cursor.execute("INSERT INTO FoodOwners (full_name, phone_number) VALUES (%s, %s)", 
                       (full_name, phone_number))
            mysql.connection.commit()
        
        flash("Account created successfully!", 'success')
    except Exception as e:
      logging.error(f"Error saving user data: {str(e)}")
      mysql.connection.rollback()
      flash("An error occurred. Please try again.", 'error')
    finally:
              cursor.close()
        
    return render_template("register.html")
        

        


    
@app.route('/login', methods = ["GET", "POST"])
def login():
    #displays the login page 
    if "user_id" in session:
        if(session["role"] == "customer"):
            flash("You are already logged in", 'warning')
            return redirect(url_for("customer"))
            
        elif(session["role"] == "driver"):
            flash("You are already logged in", 'warning')
            return redirect(url_for("driver"))
        
        elif(session["role"] == "food_owner"):
            flash("You are already logged in", 'warning')
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
            flash("You must type in an email AND a password", 'error')

        elif not user:
            flash("Invalid email address", 'error')
        
        #used if you forget the user password: elif password != user["password"]
        elif not check_password_hash(user["password"],password):
            flash("Invalid password", 'error')

        
            
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

            #Used to grab the details from their respective tables and redirect them to their dashboard
            if(session["role"] == "customer"):
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM Customers WHERE phone_number= %s", (session["phone_number"],))
                customer = cursor.fetchone()
                cursor.close()

                #If the query is correct / phone number from Users equals the one in Customers
                if customer:
                    session["customer_id"] = customer["customer_id"]
                    session["credits"] = customer["credits"]
                    session["status"] = customer["status"]
                    session["pending_credits"] = customer["pending_credits"]

                
                return redirect(url_for("customer"))
            
            elif(session["role"] == "driver"):
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM Drivers WHERE phone_number= %s", (session["phone_number"],))
                driver = cursor.fetchone()
                cursor.close()

                if driver:
                    session["driver_id"] = driver["driver_id"]
                    session["is_available"] = driver["is_available"]
                    session["vehicle_type"] = driver["vehicle_type"]
                    session["history"] = driver.get("history",[])  #safely access history
                
                return redirect(url_for("driver"))

            else:
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT * FROM FoodOwners WHERE phone_number= %s", (session["phone_number"],))
                foodOwner = cursor.fetchone()
                cursor.close()

                if foodOwner:
                    session["food_owner_id"] = foodOwner["food_owner_id"]
                    session["business_name"] = foodOwner["business_name"]
                

                return redirect(url_for("foodOwner"))

        
        return render_template("login.html")
        




#pages / dashboards for each role
@app.route('/customer')
def customer():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, image, caption FROM Promotions")
    promotions = cursor.fetchall()
    return render_template("customer.html", promotions=promotions)

# CODE COMPLETED BY GLENN
@app.route('/driver')
def driver():
    driver_id = session.get("driver_id")
    current_delivery = None
    past_deliveries = []
    if driver_id:
        cursor = mysql.connection.cursor()
        # Query the active (accepted) pickup.
        cursor.execute(
            "SELECT * FROM Pickups WHERE driver_id = %s AND status = 'accepted' LIMIT 1",
            (driver_id,)
        )
        current_delivery = cursor.fetchone()
        
        # Query past (complete) deliveries.
        cursor.execute(
            "SELECT * FROM Pickups WHERE driver_id = %s AND status = 'completed' ORDER BY pickup_date DESC, pickup_time DESC",
            (driver_id,)
        )
        past_deliveries = cursor.fetchall()
        cursor.close()
    
    # Calculate earnings from past deliveries
    earnings_total = 0
    earnings_today = 0
    earnings_week = 0
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    
    for delivery in past_deliveries:
        # Ensure credits_earned is a float
        credits = float(delivery['credits_earned'])
        earnings_total += credits
        
        # Assume pickup_date is stored as a date object.
        # If it's a string, you might need to convert it using datetime.strptime.
        delivery_date = delivery['pickup_date']
        if isinstance(delivery_date, str):
            delivery_date = datetime.strptime(delivery_date, "%Y-%m-%d").date()
        
        if delivery_date == today:
            earnings_today += credits
        if delivery_date >= start_of_week:
            earnings_week += credits

    # Prepare display values.
    delivery_status = current_delivery["status"] if current_delivery else "Idle"
    delivery_destination = "N/A"  # Update if you have a destination field
    if current_delivery and current_delivery.get("pickup_time"):
        pickup_timedelta = current_delivery["pickup_time"]
        # Convert timedelta to a time object (assuming it represents time since midnight)
        pickup_time = (datetime.min + pickup_timedelta).time()
        delivery_eta = pickup_time.strftime("%H:%M")
    else:
        delivery_eta = "N/A"
    
    return render_template("driver.html",
                           driver_name=session.get("full_name", "Driver"),
                           driver_vehicle=session.get("vehicle_type", "N/A"),
                           delivery_status=delivery_status,
                           delivery_destination=delivery_destination,
                           delivery_eta=delivery_eta,
                           current_delivery=current_delivery,  # Pass active delivery details
                           upcoming_deliveries=[],  # If you add future deliveries, query here.
                           earnings_today=earnings_today,
                           earnings_week=earnings_week,
                           earnings_total=earnings_total,
                           past_deliveries=past_deliveries)

@app.route('/foodOwner')
def foodOwner():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, image, caption FROM Promotions")
    promotions = cursor.fetchall()
    return render_template("foodOwner.html", promotions=promotions)
    


#END: CODE COMPLETED BY CHRISTIAN






#START: CODE COMPLETED BY PRAKASH


@app.route("/stripe_webhook", methods=["POST"])
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
    

        # Log the event type
    logging.info(f"Received event: {event['type']}")

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})

         # Log the metadata
        logging.info(f"Session metadata: {metadata}")

# Extract driver details from metadata
        full_name = metadata.get("full_name")
        email = metadata.get("email")
        password = metadata.get("password")
        role = metadata.get("role")
        phone_number = metadata.get("phone_number")
        address = metadata.get("address")

        # Log the extracted data
        logging.info(f"Extracted data: full_name={full_name}, email={email}, role={role}")

        # Save driver details to the database
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO Users (full_name, email, password, role, phone_number, address) VALUES (%s, %s, %s, %s, %s, %s)",
                           (full_name, email, password, role, phone_number, address))
            mysql.connection.commit()

            if role == "driver":
                cursor.execute("INSERT INTO Drivers (full_name, phone_number) VALUES (%s, %s)",
                               (full_name, phone_number))
                mysql.connection.commit()
                logging.info(f"Driver {full_name} ({email}) created successfully.")
        except Exception as e:
            logging.error(f"Error saving driver data: {str(e)}")
            mysql.connection.rollback()
        finally:
            cursor.close()

    # Handle subscription events
    elif event["type"] == "invoice.payment_succeeded":
        # Handle subscription renewal for food owners
        invoice = event["data"]["object"]
        stripe_subscription_id = invoice["subscription"]

        #Retrive subscription detail from stripe
        subscription = stripe.Subscription.retrieve(stripe_subscription_id)

        # Extract subscription details
        
        start_date = datetime.fromtimestamp(subscription["current_period_start"])
        end_date = datetime.fromtimestamp(subscription["current_period_end"])
        next_due_date = datetime.fromtimestamp(subscription["current_period_end"])


       # Log the subscription details
        logging.info(f"Subscription details: start_date={start_date}, end_date={end_date}, next_due_date={next_due_date}")
        
        # update subscription details to the database
        cursor = mysql.connection.cursor()

        try:
            cursor.execute("""
                UPDATE Subscriptions
                SET subscription_start_date = %s,
                    subscription_end_date = %s,
                    next_due_date = %s,
                    status = 'active'
                WHERE stripe_subscription_id = %s
            """, (start_date, end_date, next_due_date, stripe_subscription_id))
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
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Orders WHERE customer_id = %s ORDER BY order_date DESC", (session["customer_id"],))
    orders = cursor.fetchall()
    cursor.close()

   
    for order in orders:
        try:
            order['items_parsed'] = json.loads(order['items'])
        except Exception as e:
            print("Error parsing order items:", e)
            order['items_parsed'] = []  

    return render_template("Cprofile.html",
                           full_name=session["full_name"],
                           email=session["email"],
                           phone_number=session["phone_number"],
                           address=session["address"],
                           orders=orders)

@app.route('/schedulePickup')
def schedulePickup():
    return render_template("schedulePickup.html")

@app.route('/foodMarketplace')
def foodMarketplace():
    cur = mysql.connection.cursor()

    # Fetch restaurants
    cur.execute("SELECT id, name, image, description FROM Restaurants")
    restaurants = cur.fetchall()

    # Fetch meals
    cur.execute("SELECT restaurant_id, meal_name, price FROM Meals")
    meals = cur.fetchall()

    cur.close()

    print("✅ RESTAURANTS:", restaurants)  # Debugging
    print("✅ MEALS:", meals)  # Debugging

    return render_template("foodMarketplace.html", restaurants=restaurants, meals=meals)

# Customer payment Page - One-Time Payment
@app.route('/Cpayment')
def Cpayment():
    return render_template("Cpayment.html")  # One-time payment page



@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.json

    if 'cart' not in session or not isinstance(session['cart'], list):
        session['cart'] = []  

    session['cart'].append(item)
    session.modified = True 

    print("🛒 Updated Cart:", session['cart'])  

    return jsonify({"message": f"{item['name']} added to cart!", "cart": session['cart']})



@app.route('/get_cart')
def get_cart():
    cart_data = session.get('cart', [])
    print(" Fetching Cart from Session:", cart_data)  #  Debugging
    return jsonify({"cart": cart_data})

# Remove item from cart
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_name = request.json.get("name")
    session['cart'] = [item for item in session.get('cart', []) if item['name'] != item_name]
    session.modified = True
    return jsonify({"message": f"{item_name} removed from cart!", "cart": session['cart']})


# Gets User Credits (from session,)
@app.route('/get_user_credit')
def get_user_credit():
    return jsonify({"credit": session.get("credits", 0)})


def save_order_to_db(cart, total_amount, customer_id, mysql):
    cursor = mysql.connection.cursor()
    items = json.dumps(cart)  
    cursor.execute("INSERT INTO Orders (customer_id, items, total_amount) VALUES (%s, %s, %s)",
                   (customer_id, items, total_amount))
    mysql.connection.commit()
    cursor.close()


@app.route('/create-checkout-session-one-time', methods=['POST'])
def create_checkout_session():
    
    #fetch user credit and verification status
    user_credit = float(session.get("credits", 0))
    #user_status = session.get("status", "")
    cart = session.get('cart', [])
    
  # Check if delivery fee checkbox is checked
    delivery_fee = 2 if request.form.get('delivery') == 'yes' else 0
    #use_credits = request.form.get('use_credits') == 'yes'
    if not delivery_fee:
        flash("You must agree to the delivery fee before proceeding.", "error")
        return redirect(url_for('Cpayment'))

    #delivery_fee = 2 if request.form.get('delivery') == 'yes' else 0
    use_credits = request.form.get('use_credits') == 'yes'


    if not cart:
        flash("Your cart is empty. Add items before checking out.", "warning")
        return redirect(url_for('Cpayment'))
    
   
    
    total_price = sum(float(item['price']) for item in cart)
    total_amount = total_price + delivery_fee

    if use_credits and user_credit > 0:
        if user_credit >= total_amount:
            # Payment fully by credits
            user_credit -= total_amount
            session["credits"] = user_credit
            # Save order before clearing the cart
            save_order_to_db(cart, total_amount, session["customer_id"], mysql)
            session.pop('cart', None)
            session.modified = True
            flash("Payment Successful! Paid using credits.", "success")
            return redirect(url_for('payment_success'))
        else:
            remaining_amount = total_amount - user_credit
            session["credits"] = 0  # Deduct all credits
    else:
        remaining_amount = total_amount

    # If remaining amount > 0, process with Stripe
    if remaining_amount > 0:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': 'Food Order'},
                    'unit_amount': int(remaining_amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('payment_success', _external=True),
            cancel_url=url_for('Cpayment', _external=True),
        )
        #  
        return redirect(checkout_session.url, code=303)

    
    save_order_to_db(cart, total_amount, session["customer_id"], mysql)
    session.pop('cart', None)
    session.modified = True
    flash("Payment Successful! No additional payment required.", "success")
    return redirect(url_for('payment_success'))

@app.route('/payment_success')
def payment_success():
    
    cart = session.get('cart')
    if cart:
        total_price = sum(float(item['price']) for item in cart)
      
        total_amount = total_price
        save_order_to_db(cart, total_amount, session["customer_id"], mysql)
        session.pop('cart', None)
        session.modified = True
    flash("Payment Successful!", "success")
    return redirect(url_for('customer'))


@app.route('/Dprofile', methods=["GET", "POST"])
def Dprofile():
    return render_template("Dprofile.html", full_name=session["full_name"], email=session["email"], phone_number=session["phone_number"], address=session["address"])

#END: CODE COMPLETED BY PRAKASH


# CODE COMPLETED BY GLENN
# Routes for Pickup Request Actions

@app.route('/pickupRequest')
def pickupRequest():
    cursor = mysql.connection.cursor()

    # Fetch pending pickup requests
    cursor.execute("SELECT * FROM Pickups WHERE status = 'pending'")
    pickups = cursor.fetchall()

    # Fetch pending deposit requests (not yet verified)
    cursor.execute("SELECT customer_id, pending_credits FROM Customers WHERE status = 'pending' AND pending_credits > 0")
    deposits = cursor.fetchall()

    # Fetch verified deposits
    cursor.execute("SELECT customer_id, pending_credits FROM Customers WHERE status = 'verified' AND pending_credits > 0")
    verified_deposits = cursor.fetchall()

    cursor.close()

 # Ensure verified_deposits is not empty before creating a dictionary
    if verified_deposits:
        session["credits"] = {customer_id: credits for customer_id, credits in verified_deposits}
        
        # Show a flash message for each verified deposit
        for customer_id, credits in verified_deposits:
                        session[f"verified_message_{customer_id}"] = f"Deposit Verified! {credits} EUR added."
    else:
        session["credits"] = {}  # Empty dictionary if no verified deposits exist

    return render_template("pickupRequest.html", pending_pickups=pickups, deposit_requests=deposits)

@app.route('/accept-pickup/<int:pickup_id>', methods=['POST'])
def accept_pickup(pickup_id):
    # Retrieve the phone number from the session instead of (or in addition to) driver_id.
    phone_number = session.get("phone_number")
    if not phone_number:
        flash("You must be logged in as a driver to accept pickups.", 'warning')
        return redirect(url_for("login"))
    
    # Query the Drivers table using the phone number to retrieve driver_id.
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT driver_id FROM Drivers WHERE phone_number = %s", (phone_number,))
    driver = cursor.fetchone()
    if not driver:
        flash("No driver record found for the logged in phone number.", 'error')
        return redirect(url_for("login"))
    
    driver_id = driver["driver_id"]
    # Update the session to store the driver_id so the dashboard can access it.
    session["driver_id"] = driver_id

    # Calculate pickup_time as 30 minutes after the current time
    pickup_time = (datetime.now() + timedelta(minutes=30)).strftime("%H:%M:%S")
    
    # Update the pickup request with the retrieved driver_id.
    cursor.execute(
        "UPDATE Pickups SET status = 'accepted', driver_id = %s WHERE pickup_id = %s",
        (driver_id, pickup_id)
    )
    mysql.connection.commit()
    cursor.close()
    
    flash(f"Pickup request {pickup_id} accepted!")
    return redirect(url_for('pickupRequest'))

@app.route('/decline-pickup/<int:pickup_id>', methods=['POST'])
def decline_pickup(pickup_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Pickups WHERE pickup_id = %s", (pickup_id,))
    mysql.connection.commit()
    cursor.close()
    flash(f"Pickup request {pickup_id} declined.", 'error')
    return redirect(url_for('pickupRequest'))

@app.route('/add-random-pickup', methods=['POST'])
def add_random_pickup():
    # For visual testing, we assume customer_id is 7.
    customer_id = 7
    pickup_date = date.today()
    # Generate a random time between 10:00 and 18:00
    hour = random.randint(10, 18)
    minute = random.randint(0, 59)
    # HH:MM:SS (MySQL TIME format)
    pickup_time = f"{hour:02d}:{minute:02d}:00"
    status = 'pending'
    credits_earned = 0.00

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO Pickups (customer_id, pickup_date, pickup_time, status, credits_earned) VALUES (%s, %s, %s, %s, %s)",
        (customer_id, pickup_date, pickup_time, status, credits_earned)
    )
    mysql.connection.commit()
    cursor.close()
    flash("Random pickup request added!", 'success')
    return redirect(url_for('pickupRequest'))

@app.route('/sync-pickups', methods=['POST'])
def sync_pickups():
    cursor = mysql.connection.cursor()
    today = date.today()
    
    # Query orders from today.
    # (Adjust this query as needed to match your criteria for "unsynced" orders.)
    cursor.execute("SELECT order_id, customer_id, order_date FROM Orders WHERE DATE(order_date) = %s", (today,))
    orders = cursor.fetchall()
    
    if not orders:
        flash("No orders found for today to sync.", "warning")
        return redirect(url_for('pickupRequest'))
    
    synced_count = 0
    for order in orders:
        # Check if a pickup already exists for this order based on customer_id and order_date.
        cursor.execute("SELECT * FROM Pickups WHERE customer_id = %s AND pickup_date = %s", 
                       (order['customer_id'], order['order_date']))
        existing = cursor.fetchone()
        if existing:
            continue  # Skip orders that already have a corresponding pickup
        
        # Insert a new pickup record.
        # Here, we set pickup_time to NULL (or you could use a default like "00:00:00"),
        # status as 'pending', and credits_earned as 0.00.
        cursor.execute("""
            INSERT INTO Pickups (customer_id, pickup_date, pickup_time, status, credits_earned)
            VALUES (%s, %s, %s, %s, %s)
        """, (order['customer_id'], order['order_date'], "00:00:00", 'pending', 5.00))
        synced_count += 1

    mysql.connection.commit()
    cursor.close()
    
    if synced_count > 0:
        flash(f"{synced_count} order(s) synced to pickups successfully.", "success")
    else:
        flash("No new orders to sync.", "warning")
    
    return redirect(url_for('pickupRequest'))

@app.route('/complete-delivery/<int:pickup_id>', methods=['POST'])
def complete_delivery(pickup_id):
    driver_id = session.get("driver_id")
    if not driver_id:
        flash("You must be logged in as a driver to complete deliveries.", 'warning')
        return redirect(url_for("login"))
    
    cursor = mysql.connection.cursor()
    # Verify that the pickup belongs to this driver and is still accepted.
    cursor.execute(
        "SELECT * FROM Pickups WHERE pickup_id = %s AND driver_id = %s AND status = 'accepted'",
        (pickup_id, driver_id)
    )
    pickup = cursor.fetchone()
    if not pickup:
        flash("Delivery not found or already completed.", 'error')
        cursor.close()
        return redirect(url_for("driver"))
    
    # Mark the delivery as complete and update earnings (set credits_earned to 5)
    cursor.execute(
        "UPDATE Pickups SET status = 'completed', credits_earned = %s WHERE pickup_id = %s",
        (5, pickup_id)
    )
    mysql.connection.commit()
    cursor.close()
    
    flash(f"Delivery {pickup_id} marked as complete!", 'success')
    return redirect(url_for("driver"))

@app.route('/earningReport')
def earningReport():
    return render_template("earningReport.html")

#CODE COMPLETED BY GLENN



#START: CODE COMPLETED BY PRAKASH

@app.route('/Fprofile', methods=["GET", "POST"])
def Fprofile():
    return render_template("Fprofile.html", full_name=session["full_name"], email=session["email"], phone_number=session["phone_number"], address=session["address"])


# Subscription Page
@app.route('/Subscribe')
def subscription():
        
        ##check if the user is logged in and has the correct role
        if "user_id" not in session or session["role"] != "food_owner":
           flash("You must be logged in as a food owner to view this page.", 'warning')
           return redirect(url_for("login"))


        #Fetch subscription data from the database
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("""
            SELECT subscription_id, stripe_subscription_id, subscription_start_date, subscription_end_date, next_due_date, status
            FROM Subscriptions
            WHERE promoter_id = %s
        """, (session["user_id"],)) #Fetch subscription for the logged-in user
            subscriptions = cursor.fetchall() # Get all rows as list of tuples
        except Exception as e:
             logging.error(f"Error fetching subscription data: {str(e)}")
             subscriptions = [] #If there's an error , return an empty list
        finally:
             cursor.close() #Close the database cursor

        return render_template("subscription.html", subscriptions=subscriptions)
  #  return render_template("subscription.html") # Subscription payment page


# Create Checkout Session for Subscription
@app.route("/create-checkout-session-subscription", methods=["GET", "POST"])
def create_checkout_session_subscription():

    if "user_id" not in session or session["role"] != "food_owner":
        flash("You must be logged in as a food owner to subscribe.", 'warning')
        return redirect(url_for("login"))

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
            cancel_url=f"{YOUR_DOMAIN}/cancel",
            metadata={
                "promoter_id": session["user_id"],  # Pass the logged-in user's ID
                "email": session["email"],      # Pass the logged-in user's email
                "role": session["role"],        # Pass the logged-in user's role
            },
        )

        # Store subscription details in the database
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO Subscriptions (promoter_id, stripe_subscription_id, subscription_start_date, subscription_end_date, next_due_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            session["user_id"],
            checkout_session.id,  # Stripe checkout session ID
            datetime.now(),  # Subscription start date
            datetime.now() + timedelta(days=30),  # Subscription end date (30 days from now)
            datetime.now() + timedelta(days=30),  # Next due date (30 days from now)
           
            "active"
        ))
        mysql.connection.commit()
        cursor.close()

        return redirect(checkout_session.url, code=303)
    except Exception as e:
        logging.error(f"Error creating Stripe Checkout Session: {str(e)}")
        flash("Payment failed. Please try again.", 'error')
        return redirect(url_for("subscription"))


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
@app.route("/deposit", methods = ["GET", "POST"])
def deposit():
    if request.method == "GET":
         # If the deposit was just verified, show a success message
        if session.get("status") == "verified":
            flash(f"Your deposit has been verified! You now have €{session['credits']} in credits.", "success")
        return render_template("deposit.html",  status=session["status"], credits=session["credits"], customer_id=session["customer_id"])
    
    else:
        #If the input field is empty
        if not request.form.get("bottles"):
            flash("Please enter a number of bottles before submitting", 'error')
            return redirect(url_for("deposit"))
        
        #For every bottle, you get 10 cent
        bottles = int(request.form["bottles"])
        credits = bottles / 10
        cursor = mysql.connection.cursor()
        
        if(bottles > 100):
            flash("Please deposit 100 bottles or less at a time", 'warning')
            return redirect(url_for("deposit"))
        
        elif(bottles <= 0):
            flash("You cannot enter less than 1 bottle", 'warning')
            return redirect(url_for("deposit"))
    
        
        else:
            cursor.execute("UPDATE Customers SET pending_credits = pending_credits + %s WHERE customer_id = %s", (credits, session["customer_id"]))
            mysql.connection.commit()
            cursor.close()
            
            #F-string used to display the variables alongside Flash
            flash(f"You have deposited {bottles} bottles, you will receive {credits} euro in your credits! They must be verified first in order to use them", 'success')

            session["pending_credits"] = float(session["pending_credits"]) + float(credits)
            session["status"] = "pending"

            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE Customers SET status = %s WHERE customer_id = %s", ("pending", session["customer_id"]))
            mysql.connection.commit()
            cursor.close()

           # session["status"] = "pending"

            return redirect(url_for("deposit"))
    

@app.route('/redeemCredits')
def redeemCredits():
    credits = float(session.get("credits"))  #used to prevent <= error
    pending_credits = float(session.get("pending_credits"))

    if session.get("status") == "pending":
        flash("You cannot use your credits until they are verified", 'error')
        return redirect(url_for("deposit"))

    if credits <= 0 or credits == 0 or credits == 0.00 or credits == None: 
        flash("You cannot redeem any credits since you do not have any", 'error')
        return redirect(url_for("deposit"))
    

    
    elif session.get("status") == "verified" or session.get("status") != "pending":
        flash(f"You have redeemed {session["credits"]} euro. You should receive your cash in 3-5 business days", 'success')
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Customers SET credits = 0 WHERE customer_id = %s", (session["customer_id"],))
        mysql.connection.commit()
        cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Customers SET status = '' WHERE customer_id = %s", (session["customer_id"],))
        mysql.connection.commit()
        cursor.close()

        
        session["credits"] = 0
        session["status"] = " "

        return redirect(url_for("deposit"))
    
@app.route('/verify-deposit/<int:customer_id>', methods=['POST'])
def verify_deposit(customer_id):
    cursor = mysql.connection.cursor()
    # Update the customer status to 'verified'
    cursor.execute("UPDATE Customers SET status = 'verified' WHERE customer_id = %s", (customer_id,))
    mysql.connection.commit()

    cursor.execute("UPDATE Customers SET credits = pending_credits + credits WHERE customer_id = %s", (customer_id,))
    mysql.connection.commit()

    
    cursor.execute("UPDATE Customers SET pending_credits = 0 WHERE customer_id = %s", (customer_id,))
    mysql.connection.commit()
    cursor.close()
    
     # Store the verified message in session (so it appears in /deposit)
    session[f"verified_message_{customer_id}"] = f"Deposit Verified! Your credits are now available."
    return redirect(url_for('pickupRequest'))

    


@app.route("/updateCProfile", methods=["GET", "POST"])
def updateCProfile():
    if request.method == "GET":
        return render_template("updateCProfile.html")
    else:
        email = request.form["email"]
        full_name = request.form["full_name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]

        if email_exists(email) and session["email"] != email:
            flash("Email is already registered, please try again", 'warning')
            return redirect(url_for("updateCProfile"))
        
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Users SET email = %s, full_name = %s, phone_number = %s, address = %s WHERE user_id = %s",
                       (email, full_name, phone_number, address, session["user_id"]))
        mysql.connection.commit()
        cursor.close()

        #logs the user out
        session.clear()
        flash("Profile Updated! Log back in to see updates", 'success')
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

        if email_exists(email) and session["email"] != email:
            flash("Email is already registered", 'warning')
            return redirect(url_for("updateDProfile"))

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Users SET email = %s, full_name = %s, phone_number = %s, address = %s WHERE user_id = %s",
                       (email, full_name, phone_number, address, session["user_id"]))
        mysql.connection.commit()
        cursor.close()

        #logs the user out
        session.clear()
        flash("Profile Updated! Log back in to see updates", 'success')
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

        if email_exists(email) and session["email"] != email:
            flash("Email is already registered", 'warning')
            return redirect(url_for("updateFProfile"))
        
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE Users SET email = %s, full_name = %s, phone_number = %s, address = %s WHERE user_id = %s",
                       (email, full_name, phone_number, address, session["user_id"]))
        mysql.connection.commit()
        cursor.close()

        #logs the user out
        session.clear()
        flash("Profile Updated! Log back in to see updates", 'success')
        return redirect(url_for("login"))
    

@app.route('/postPromotion', methods =["GET", "POST"])
def postPromotion():

    #Used to create the Jinja template / display each image in promotion page
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        user_id = session["user_id"]
        

        if user_id:
            cursor.execute("SELECT promoter_id FROM Subscriptions WHERE promoter_id = %s", (user_id,))
            validSub = cursor.fetchone()

            if validSub:
                cursor.execute("SELECT id, image, caption FROM Promotions")
                promotions = cursor.fetchall()
                return render_template("postPromotion.html", promotions=promotions)
        
            else:
                flash("You must subscribe to our plan to use the food promotion!", "error")
                return redirect(url_for('foodOwner'))

        
    
        
    
    else:
        #Validation 
        if request.method == 'POST':
            image = request.files['image']

            if not image or image.filename == '':
                flash('No selected file', 'error')
                return redirect(url_for('postPromotion')) 
            
            if not allowed_file(image.filename):
                flash('Invalid image type, use the following image extensions: .JPG, .PNG or .JPEG', 'error')
                return redirect(url_for('postPromotion'))
            
            
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
            
            flash('Image uploaded successfully', 'success')
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
    flash('Image successfully deleted!', 'success')

    return redirect(url_for("postPromotion"))

        
        
         
        

    


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))
  
#makes it so that it only runs the app when executed
if __name__ == "__main__":
    app.run(debug=True) #updates in real-time + shows bugs / errors on CMD

#END: CODE COMPLETED BY CHRISTIAN


@app.route('/foodMarketplace')
def foodMarketplace():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, image, description FROM Restaurants")
    rows = cur.fetchall()
    
    # Convert tuples to dictionaries for Jinja compatibility
    restaurants = [{"id": row[0], "name": row[1], "image": row[2], "description": row[3]} for row in rows]

    cur.close()
    
    print("✅ RESTAURANTS LOADED:", restaurants)  # Debugging

    return render_template("foodMarketplace.html", restaurants=restaurants)

if __name__ == "__main__":
    app.run(debug=True)  # ✅ Make sure this is at the bottom

      
