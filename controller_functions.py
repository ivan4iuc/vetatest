from config import db, bcrypt
from models import users, cards, history, contacts 
from flask import render_template, request, redirect, flash, session   
import re
from sqlalchemy.sql import func

# Initial login page
def login():
    return render_template('login.html')

# Initialized by clicking log in - only send to home page if email is registered and password is correct
def submitLogin():
    queryUser = users.query.filter_by(email=request.form["email"]).all()
    if queryUser:
        if bcrypt.check_password_hash(queryUser[0].password, request.form["password"]):
            session["loggedInUserID"] = queryUser[0].id  
            return redirect('/home')
        flash("Incorrect password")
        return redirect('/login')
    flash("Unrecognized email")
    return redirect('/login')

# Switch to registration page instead
def register():
    return render_template('register.html')

# Route to register a new user with form validations
def submitRegistration():
    special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    email_char = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    is_valid = True
    if len(request.form['first_name']) < 1:
        is_valid = False
        flash("Must enter first name")
    if len(request.form['last_name']) < 1:
        is_valid = False
        flash("Must enter last name")
    if len(request.form['pw']) < 5:
        is_valid = False
        flash("Password must be more than 5 characters")
    if special_char.search(request.form['pw']) == None:
        is_valid = False
        flash("Password must contain a special character")
    if any(char.isdigit() for char in request.form['pw']) == False:
        is_valid = False
        flash ("Password must contain a number")
    if request.form['pw'] != request.form['c_pw']:
        is_valid = False
        flash("Passwords must match") 
    if special_char.search(request.form['first_name']) != None:
        is_valid = False
        flash("First name cannot contain special characters")
    if special_char.search(request.form['last_name']) != None:
        is_valid = False
        flash("Last name cannot contain special characters")
    if any(char.isdigit() for char in request.form['first_name']) == True:
        is_valid = False
        flash ("First name cannot contain a number")
    if any(char.isdigit() for char in request.form['last_name']) == True:
        is_valid = False
        flash ("Last name cannot contain a number")
    if len(request.form['email']) < 1:
        is_valid = False
        flash("Must enter email")
    elif not email_char.match(request.form['email']):
        is_valid = False
        flash ("Incorrect format for email")
    for user in users.query.all(): 
        if request.form['email'] == user.email:
            is_valid = False
            flash("Email is already registered")

    if is_valid:
        pwd_hash = bcrypt.generate_password_hash(request.form["pw"])
        newUser = users(first_name=request.form["first_name"], last_name=request.form["last_name"], email=request.form["email"], password=pwd_hash)
        db.session.add(newUser)
        db.session.commit()

        session["loggedInUserID"] = newUser.id
        return redirect('/home')

    return redirect('/register')

# Rendering basic home page
def home():
    return render_template("home.html", user=users.query.get(int(session["loggedInUserID"])))

# Return templates for adding text and recipients once card is selected from home page
def addText(card_id):
    return render_template("addText.html", card_id = int(card_id))

def addRecipient(card_id):
    return render_template("addRecipient.html", card_id = int(card_id))


# Note to ES... need to test/play with how the confirmation and submit information is being sent back and forth between these requests
def confirmation(card_id):
    return render_template("confirmation.html", message = request.form["form-message"], card_id = int(card_id), full_name = request.form["form-full-name"], address = request.form["form-address"], city = request.form["form-city"], zip_code = request.form["form-zip-code"], country = request.form["form-country"])

def submitCard(card_id):
    newContact = contacts(full_name = request.form["form-full-name"], address = request.form["form-address"], city = request.form["form-city"], zip_code = request.form["form-zip-code"], country = request.form["form-country"])
    db.session.add(newContact)
    db.session.commit()
    newHistory = history(user_id = session['loggedInUserID'], card_id = int(card_id), contact_id = newContact.id, message = request.form["form-message"]) 
    db.session.add(newHistory)
    db.session.commit()

# Simple template confirmation of sent card
def cardSent():
    return render_template("cardSent.html")

# log out, return to login page
def logout():           
    session.clear()
    return redirect('/login')
