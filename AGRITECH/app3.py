from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime
from flask_mail import Mail, Message   
from functools import wraps

from utils.history_data import log_user_activity, get_user_history
import requests
from utils.crop_data import crop_data
from utils.data_tree import get_states_by_region, get_crop_types_by_state, get_crops_by_type
#from utils.user_data import users


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # MySQL username
app.config['MYSQL_PASSWORD'] = '#####'  # MySQL password
app.config['MYSQL_DB'] = 'Agrotech'  # MySQL database name
mysql = MySQL(app)

# Flask-Mail configuration for Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # Use 587 for TLS
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False  # Set to True if using port 587
app.config['MAIL_USERNAME'] = 'abc@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = '######'  # Or App Pass
app.config['MAIL_DEFAULT_SENDER'] = 'abcd@gmail.com'

mail = Mail(app)

# Create tables if they don't exist
def create_tables():
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone_no VARCHAR(15),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            location VARCHAR(255),
            registration_datetime DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS maids (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone_no VARCHAR(15),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            aadhar VARCHAR(20),
            address TEXT,
            food_preference ENUM('veg', 'nonveg', 'both'),
            skills TEXT,
            gender ENUM('male', 'female', 'other'),
            location VARCHAR(255),
            profile_pic VARCHAR(255),
            registration_datetime DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,  
            rating INT NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        cursor.execute(''' 
        CREATE TABLE if not exists bookings (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            address TEXT NOT NULL,
            phone VARCHAR(15) NOT NULL,
            maid_id INT NOT NULL,
            maid_name VARCHAR(255) NOT NULL,
            otp VARCHAR(4) NOT NULL,
            booking_status ENUM('pending', 'confirmed', 'canceled') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (maid_id) REFERENCES maids(maid_id)
        ); 
        ''')
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS contact_form (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,  
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(15) NOT NULL,
            message TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        mysql.connection.commit()
        cursor.close()

# Create the tables at startup
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/index.html', methods=['GET', 'POST'])
def home1():
    return render_template('index.html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        name = request.form['name']
        phone_no = request.form['phone_no']
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashpw(password.encode('utf-8'), gensalt())  # Hash the password
        location = request.form['location']
        
        registration_datetime = datetime.now()
        
        cur = mysql.connection.cursor()
        cur.execute(""" 
        INSERT INTO customers (name, phone_no, email, password, location, registration_datetime)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, phone_no, email, hashed_password, location, registration_datetime))  
        mysql.connection.commit()
        cur.close()
        flash('Thank you for registering! Your account has been created.', 'success')
        return redirect(url_for('register_customer'))
    
    return render_template('customer.html')

@app.route('/maid.html', methods=['GET', 'POST'])
def register_maid():
    if request.method == 'POST':
        name = request.form['name']
        phone_no = request.form['phone_no']
        email = request.form['email']
        password = request.form['password']
        aadhar = request.form['aadhar']
        address = request.form['address']
        food_preference = request.form['food_preference']
        skills = request.form['skills']
        gender = request.form['gender']
        location = request.form['location']
        profile_pic = request.form['profile_pic']

        hashed_password = hashpw(password.encode('utf-8'), gensalt())

        cur = mysql.connection.cursor()

        cur.execute(''' 
            INSERT INTO maids (name, phone_no, email, password, aadhar, address, food_preference, 
                               skills, gender, location, profile_pic, registration_datetime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (name, phone_no, email, hashed_password, aadhar, address, food_preference, 
              skills, gender, location, profile_pic, datetime.now()))

        mysql.connection.commit()
        cur.close()
        flash('Thank you for registering! Your profile has been created.', 'success')
        return redirect(url_for('register_maid'))

    return render_template('maid.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mysql.connection.cursor()

        if user_type == 'customer':
            cur.execute('SELECT * FROM customers WHERE email = %s', (email,))
            customer = cur.fetchone()
            if customer and checkpw(password.encode('utf-8'), customer[4].encode('utf-8')):
                session['user_id'] = customer[0]
                session['user_name'] = customer[1]
                session['phone_no'] = customer[2]
                session['email'] = customer[3]
                session['location'] = customer[5]
                session['user_role'] = 'Customer'
                flash(f'Login successful as {session["user_role"]}!', 'success')
                return redirect(url_for('customer_dashboard'))
            else:
                flash('Wrong password entered for Customer.', 'danger')
                return redirect(url_for('login'))

        elif user_type == 'maid':
            cur.execute('SELECT * FROM maids WHERE email = %s', (email,))
            maid = cur.fetchone()
            if maid and checkpw(password.encode('utf-8'), maid[4].encode('utf-8')):
                session['user_id'] = maid[0]
                session['user_name'] = maid[1]
                session['phone_no'] = maid[2]
                session['email'] = maid[3]
                session['aadhar'] = maid[5]
                session['address'] = maid[6]
                session['food_preference'] = maid[7]
                session['skills'] = maid[8]  
                session['gender'] = maid[9]  
                session['location'] = maid[10] 
                session['registration_datetime'] = maid[12] 
                session['user_role'] = 'Maid'
                flash(f'Login successful as {session["user_role"]}!', 'success')
                return redirect(url_for('maid_dashboard'))
            else:
                flash('Wrong password entered for Maid.', 'danger')
                return redirect(url_for('login'))

        cur.close()

    return render_template('login.html')

@app.route('/customers_dashboard')
def customer_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Debugging: Print session data
    print("Session Data:", session)

    user_name = session.get('user_name')
    phone_no = session.get('phone_no')
    email = session.get('email')
    location = session.get('location')
    
    return render_template('after_login_dashboard.html', user_name=user_name, phone_no=phone_no, email=email, location=location)
@app.route('/maid_dashboard')
def maid_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    phone_no = session.get('phone_no')
    email = session.get('email')
    aadhar = session.get('aadhar')
    address = session.get('address')
    food_preference = session.get('food_preference')
    skills = session.get('skills')
    gender = session.get('gender')
    location = session.get('location')
    registration_datetime = session.get('registration_datetime')

    return render_template('maids_dashboard.html', user_id=user_id, user_name=user_name, phone_no=phone_no, email=email, aadhar=aadhar, address=address,
food_preference=food_preference, skills=skills, gender=gender, location=location, registration_datetime=registration_datetime)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/about_us.html')
def about_us():
    return render_template('about_us.html')

@app.route('/reviews.html', methods=['GET', 'POST'])
def review():
    if 'user_id' not in session: 
        return redirect(url_for('register'))  # Redirect to registration if not logged in

    if request.method == 'POST':
        name = request.form['name']
        rating = request.form['rating']
        comment = request.form['comment']
        
        if not rating or not comment:
            flash('Please provide both a rating and a comment.', 'danger')
            return redirect(url_for('review'))
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                flash('Rating should be between 1 and 5.', 'danger')
                return redirect(url_for('review'))
        except ValueError:
            flash('Invalid rating. Please provide a valid number.', 'danger')
            return redirect(url_for('review'))

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO reviews (name, rating, comment) VALUES (%s, %s, %s)", (name, rating, comment))
        mysql.connection.commit()
        cursor.close()
        
        flash('Review Submitted. Thank you for your feedback!', 'success')
        return redirect(url_for('review'))

    return render_template('reviews.html')

@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        if not name or not email or not phone or not message:
            flash("Please fill in all fields.", 'danger')
            return redirect(url_for('contact'))

        cursor = mysql.connection.cursor()
        cursor.execute(''' 
        INSERT INTO contact_form (name, email, phone, message)
        VALUES (%s, %s, %s, %s)
        ''', (name, email, phone, message))

        mysql.connection.commit()

        try:
            msg = Message(
                'New Contact Form Submission',
                sender=email,
                recipients=['rajkumar777788889999000@gmail.com']
            )
            msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
            mail.send(msg)

            flash("Your message has been received. We will get back to you as soon as possible.", 'success')
        except Exception as e:
            flash(f"An error occurred while sending your message. Please try again later. Error: {str(e)}", 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html')

maids = [
    {'maid_id': 1, 'maid_name': 'Priyanka Sharma', 'maid_skills': 'Cleaning, Cooking, Child Care'},
    {'maid_id': 2, 'maid_name': 'Anita Desai', 'maid_skills': 'Cleaning, Elder Care'},
]

@app.route('/book_maid/<int:maid_id>', methods=['GET'])
def book_maid(maid_id):
    maid = next((maid for maid in maids if maid['maid_id'] == maid_id), None)
    if maid:
        return render_template('booking_form.html', maid_id=maid['maid_id'], maid_name=maid['maid_name'])
    return "Maid not found", 404

@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    if 'user_id' not in session:
        return redirect(url_for('register'))  # Redirect to registration if not logged in

    customer_name = request.form['customer_name']
    address = request.form['address']
    phone = request.form['phone']
    maid_id = request.form['maid_id']
    maid_name = request.form['maid_name']
    user_name = session.get('user_name')

    cursor = mysql.connection.cursor()
    cursor.execute( 
             """
    INSERT INTO bookings (customer_name, address, phone, maid_id, maid_name, user_name)
    VALUES (%s, %s, %s, %s, %s, %s)
    """,(customer_name, address, phone, maid_id, maid_name, user_name))
   
    mysql.connection.commit()

    flash(f"{user_name} Booking confirmed for {customer_name}. Maid {maid_name} will assist you soon!")
    return redirect(url_for('confirm_booking', user_name=user_name, customer_name=customer_name, maid_name=maid_name))

@app.route('/confirm_booking.html')
def confirm_booking():
    user_name = session.get('user_name')
    customer_name = request.args.get('customer_name')
    maid_name = request.args.get('maid_name')
    return render_template('confirm_booking.html', user_name=user_name, customer_name=customer_name, maid_name=maid_name)

@app.route('/privacyPolicy.html')
def privacyPolicy():
    return render_template('privacyPolicy.html')

@app.route('/TermsOfServices.html')
def TermsOfServices():
    return render_template('TermsOfServices.html')

@app.route('/tearmsAndConditionCustomer.html')
def tearmsAndConditionCustomer():
    return render_template('tearmsAndConditionCustomer.html')

@app.route('/tearmsAndConditionMaid.html')
def tearmsAndConditionMaid():
    return render_template('tearmsAndConditionMaid.html')

@app.route('/services.html')
def Services():
    return render_template('services.html')

@app.route('/read-more')
def read_more():
    return render_template('read_more.html')




@app.route('/book_rent_tools', methods=['GET'])
def book_rent_tools():
    user_name = request.args.get('user_name')
    location = request.args.get('location')
    return render_template('book_tools.html', user_name=user_name, location=location)

@app.route('/buy_sell_products', methods=['GET', 'POST'])  # Routing for buying and selling products
def buy_sell_products():
    user_name = session.get('user_name')
    location = session.get('location')

    if request.method == 'POST':
        # Add logic for handling buy and sell transactions
        product_action = request.form.get('action')  # Assuming there's a form field named 'action'
        product_details = request.form.get('product_details')  # Assuming there's a field for product details
        
        if not product_action or not product_details:
            flash("Please provide both product action and product details.", 'danger')
            return redirect(url_for('buy_sell_products'))

        # Insert the product action into the buy_sell_products table
        cursor = mysql.connection.cursor()
        cursor.execute(''' 
            INSERT INTO buy_sell_products (user_name, location, product_action, product_details)
            VALUES (%s, %s, %s, %s)
        ''', (user_name, location, product_action, product_details))

        # Commit the transaction
        mysql.connection.commit()

        # Flash a success message with dynamic action (buy or sell)
        flash(f"{user_name} has successfully {product_action}ed the product: {product_details}", 'success')

        return redirect(url_for('buy_sell_products'))  # Redirect to the same page after processing

    return render_template('buy_products.html', user_name=user_name, location=location)

@app.route('/cart', methods=['GET'])
def cart():
    user_name = session.get('user_name')

    # Fetch products available for buying
    cursor = mysql.connection.cursor()
    cursor.execute(''' 
        SELECT * FROM buy_sell_products
        WHERE product_action = 'buy' AND user_name != %s
    ''', (user_name,))
    products_to_buy = cursor.fetchall()

    # Fetch products that the user has listed for sale
    cursor.execute(''' 
        SELECT * FROM buy_sell_products
        WHERE product_action = 'sell' AND user_name = %s
    ''', (user_name,))
    products_for_sale = cursor.fetchall()

    # Render the cart page with the data
    return render_template('cart.html', 
                           products_to_buy=products_to_buy, 
                           products_for_sale=products_for_sale)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    action = request.form.get('action')  # Could be "buy"
    user_name = session.get('user_name')

    if action == "buy":
        cursor = mysql.connection.cursor()
        cursor.execute(''' 
            INSERT INTO cart (user_name, product_id, action)
            VALUES (%s, %s, %s)
        ''', (user_name, product_id, action))
        mysql.connection.commit()
        flash("Product added to your cart for buying!", 'success')

    return redirect(url_for('cart'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    user_name = session.get('user_name')

    cursor = mysql.connection.cursor()
    cursor.execute(''' 
        DELETE FROM cart
        WHERE user_name = %s AND product_id = %s
    ''', (user_name, product_id))
    mysql.connection.commit()

    flash("Product removed from your cart.", 'success')
    return redirect(url_for('cart'))


@app.route('/book-now', methods=['GET', 'POST']) #routing for labours
def book_now():
    user_name = session.get('user_name')
    location = session.get('location')

    if request.method == 'POST':
        pass

    return render_template('customers_dashboard.html', user_name=user_name, location=location)


#crop recommendations all routing here:->>
@app.route('/dashboard', methods=['GET', 'POST']) 
def dashboard():
    user_name = session.get('user_name')
    location = session.get('location')

    if request.method == 'POST':
        pass
    
    current_user = {
       "user_name": session['user_name'],
        "history": ["Crop Recommendation: Rice", "Market Price Check: Wheat"]  # Example history
     }
    
    
    return render_template('recommendation_dashboard.html', user_name=user_name, location=location)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    return render_template('input.html')

@app.route('/region_selection')
def region_selection():
    return render_template('region_selection.html')

@app.route('/state_selection/<region>')
def state_selection(region):
    states = get_states_by_region(region)
    return render_template('state_selection.html', region=region, states=states)

@app.route('/crop_type_selection/<state>')
def crop_type_selection(state):
    crop_types = get_crop_types_by_state(state)
    return render_template('crop_type_selection.html', state=state, crop_types=crop_types)

@app.route('/recommendations_r/<state>/<crop_type>')
def recommendations_r(state, crop_type):
    crops = get_crops_by_type(state, crop_type)
    return render_template('recommendations.html', state=state, crop_type=crop_type, crops=crops)

@app.route('/profile', methods=['GET', 'POST'])
def profile_crop_recommendation():
    return render_template('profile_crop_recommendation.html')


@app.route('/history')
def history():
    user_name = session['user_name']
    history = get_user_history(user_name)
    return render_template('history.html', history=history)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    # Extract input from the form
    soil_type = request.form.get('soil_type')
    temperature = request.form.get('temperature')
    rainfall = request.form.get('rainfall')
    pH = request.form.get('pH')
    if not (soil_type and temperature and rainfall and pH):
        flash('Please provide all inputs for recommendations.', 'error')
        return redirect(url_for('dashboard'))

    # Simulate crop recommendations ( can replace with our ML logic or algorithm)
    recommended_crops = crop_recommendation(soil_type, float(temperature), float(rainfall), float(pH))
    
    return render_template('recommendations.html', crops=recommended_crops)

def crop_recommendation(soil_type, temperature, rainfall, pH):
    crops_data = {
        "Rice": {"soil_type": "Loamy", "temperature": (20, 30), "rainfall": (1000, 1500), "pH": (6, 7.5)},"Wheat": {"soil_type": "Clayey", "temperature": (10, 25), "rainfall": (450, 650), "pH": (6, 7)},"Corn": {"soil_type": "Sandy", "temperature": (18, 27), "rainfall": (500, 750), "pH": (5.5, 7)},
        "Sugarcane": {"soil_type": "Clayey", "temperature": (20, 35), "rainfall": (1500, 2500), "pH": (6.5, 7.5)},"Cotton": {"soil_type": "Loamy", "temperature": (25, 35), "rainfall": (700, 1200), "pH": (5.8, 7)},"Soybean": {"soil_type": "Clayey", "temperature": (20, 30), "rainfall": (600, 1000), "pH": (6, 7)},
        "Potato": {"soil_type": "Sandy", "temperature": (15, 20), "rainfall": (500, 800), "pH": (5.5, 6.5)},"Tomato": {"soil_type": "Loamy", "temperature": (20, 27), "rainfall": (600, 1200), "pH": (6, 6.8)},"Onion": {"soil_type": "Sandy", "temperature": (12, 25), "rainfall": (500, 750), "pH": (6, 7)},
        "Carrot": {"soil_type": "Sandy", "temperature": (15, 20), "rainfall": (700, 900), "pH": (6, 6.8)},"Barley": {"soil_type": "Loamy", "temperature": (12, 22), "rainfall": (400, 600), "pH": (6, 7)},"Peas": {"soil_type": "Clayey", "temperature": (13, 18), "rainfall": (600, 1000), "pH": (6, 7.5)},
        "Lentil": {"soil_type": "Sandy", "temperature": (18, 30), "rainfall": (300, 600), "pH": (6, 7)},"Chickpea": {"soil_type": "Clayey", "temperature": (20, 25), "rainfall": (400, 600), "pH": (6, 7)},"Banana": {"soil_type": "Loamy", "temperature": (25, 35), "rainfall": (1500, 2500), "pH": (6, 7)},
        "Pineapple": {"soil_type": "Sandy", "temperature": (20, 30), "rainfall": (1200, 1500), "pH": (5, 6)},"Coffee": {"soil_type": "Loamy", "temperature": (20, 30), "rainfall": (1000, 2000), "pH": (6, 6.5)}, "Tea": {"soil_type": "Clayey", "temperature": (18, 30), "rainfall": (1500, 3000), "pH": (4.5, 5.5)},
        "Mustard": {"soil_type": "Sandy", "temperature": (10, 25), "rainfall": (400, 500), "pH": (5.5, 7)},"Groundnut": {"soil_type": "Sandy", "temperature": (25, 30), "rainfall": (500, 1000), "pH": (6, 7)},"Coconut": {"soil_type": "Sandy", "temperature": (27, 35), "rainfall": (1500, 2500), "pH": (5.2, 8)},
        "Sunflower": {"soil_type": "Loamy", "temperature": (20, 25), "rainfall": (600, 1000), "pH": (6, 7.5)},"Sorghum": {"soil_type": "Loamy", "temperature": (25, 30), "rainfall": (400, 800), "pH": (5.8, 7)},"Millet": {"soil_type": "Sandy", "temperature": (20, 30), "rainfall": (300, 600), "pH": (5.5, 6.5)},
        "Cabbage": {"soil_type": "Loamy", "temperature": (15, 20), "rainfall": (600, 1000), "pH": (6.5, 7)},"Cauliflower": {"soil_type": "Loamy", "temperature": (15, 20), "rainfall": (500, 800), "pH": (6, 7)},"Pepper": {"soil_type": "Loamy", "temperature": (20, 30), "rainfall": (600, 1000), "pH": (6, 6.8)},
        "Okra": {"soil_type": "Sandy", "temperature": (25, 30), "rainfall": (600, 800), "pH": (6, 6.8)},"Spinach": {"soil_type": "Loamy", "temperature": (15, 20), "rainfall": (400, 600), "pH": (6, 7.5)},"Strawberry": {"soil_type": "Loamy", "temperature": (10, 20), "rainfall": (600, 800), "pH": (5.5, 6.5)},
    }
    suitable_crops = []
    for crop, conditions in crops_data.items():
        if (
            soil_type == conditions["soil_type"]
            and conditions["temperature"][0] <= temperature <= conditions["temperature"][1]
            and conditions["rainfall"][0] <= rainfall <= conditions["rainfall"][1]
            and conditions["pH"][0] <= pH <= conditions["pH"][1]
        ):
            suitable_crops.append(crop)  
        activity = {
        "soil_type": soil_type,
        "temperature": temperature,
        "rainfall": rainfall,
        "pH": pH,
        "recommendations":suitable_crops
    }
    user_name = session['user_name']
    log_user_activity(user_name, activity)
    # Return the suitable crops or a message if none are found
    return suitable_crops if suitable_crops else ["No suitable crops found. Please adjust the parameters."]

@app.route('/crop/<crop_name>')
def crop_details(crop_name):
    if crop_name in crop_data:
        crop_info = crop_data[crop_name]
        return render_template('crop_details.html', crop_name=crop_name, crop_data=crop_info)
    else:
        return "Crop details not available, We will update shortly", 404
    
    
    #routing for  suggetion service
@app.route('/suggestion_dashboard', methods=['GET', 'POST'])
def suggestion_dashboard():
    user_name = session.get('user_name')

    # Fetch farming types from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, farming_name FROM farming_data")
    farming_list = cur.fetchall()
    cur.close()

    return render_template('suggestion_dashboard.html', user_name=user_name, farming_list=farming_list)



@app.route('/farming_details/<int:farming_id>')
def farming_details(farming_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM farming_data WHERE id = %s", (farming_id,))
    farming = cur.fetchone()
    cur.close()
    
    farm_name = farming[1]
    image_path = url_for('static', filename='images/farm_images/{farm_name}.jpg')
    
    if not farming:
        flash("Farming details not found!", "danger")
        return redirect(url_for('suggestion_dashboard'))
    
    return render_template('farming_details.html', image_path=image_path,farming=farming)

  ###have to change (AI/ML)
@app.route('/search_farming', methods=['GET', 'POST'])
def search_farming():
    query = request.form.get('search_query')
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT * FROM farming_data WHERE farming_name LIKE %s OR labor_needs LIKE %s
    ''', (f'%{query}%', f'%{query}%'))
    search_results = cur.fetchall()
    cur.close()

    return render_template('search_results_page.html', search_results=search_results)
    
    

if __name__ == '__main__':
    app.run(debug=True)
