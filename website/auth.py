import random
from flask_mail import Mail, Message
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '2019csb1065@iitrpr.ac.in'  # Replace with your email address
app.config['MAIL_PASSWORD'] = 'Ad9124*['  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = '2019csb1065@iitrpr.ac.in'  # Replace with your email address
mail = Mail(app)

@app.route('/register', methods=['POST'])
def register():

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    #insert password hash and columns for all user info


    pet_name = request.form['pet_name']
    species = request.form['species']
    breed = request.form['breed']
    age = int(request.form['age'])
    gender = request.form['gender']
    description = request.form['description']
    photo = request.files['photo']

    # save photo to disk and get the file path
    photo_path = save_photo(photo)

    # Generate random OTP
    otp = str(random.randint(100000, 999999))

    user = User(name=name, email=email, phone=phone)

    # create a new pet object with the form data
    pet = Pet(name=name, species=species, breed=breed, age=age, gender=gender, description=description, photo=photo_path)

    # add the pet to the database
    db.session.add(user)
    db.session.add(pet)
    db.session.commit()

     # Send OTP to user's email
    msg = Message('OTP Verification', recipients=[email])
    msg.body = f'Your OTP is: {otp}'
    mail.send(msg)

    # Store the OTP in the session
    session['otp'] = otp
    session['email'] = email

    # Redirect the user to the OTP verification page
    return redirect(url_for('verify_otp'))


@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    # Get the stored OTP and email from the session
    otp = session.get('otp')
    email = session.get('email')

    if not otp or not email:
        # If OTP or email is not present in the session, redirect to the home page
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Get the entered OTP from the form
        entered_otp = request.form['otp']

        if entered_otp == otp:
            # If OTP is correct, remove the OTP and email from the session
            session.pop('otp')
            session.pop('email')

            # Redirect the user to the home page
            flash('Thank you for registering your pet!', 'success')
            return redirect(url_for('index'))
        else:
            # If OTP is incorrect, display an error message
            flash('Incorrect OTP. Please try again.', 'danger')
            return redirect(url_for('verify_otp'))

    # Render the OTP verification page
    return render_template('verify_otp.html')
