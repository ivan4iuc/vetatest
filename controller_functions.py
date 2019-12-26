from config import db, bcrypt
from models import users, cards, holidays, history, contacts 
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
            return redirect('/resetHome')
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
        return redirect('/resetHome')

    return redirect('/register')

# Rendering basic home page
def home():
    allCards = cards.query.all() 
    return render_template("main.html", user=users.query.get(int(session["loggedInUserID"])), cards=allCards)

def resetHome():
    for card in cards.query.all():
        card.include = "Y"
        db.session.commit()
    return redirect("/home")

# Filter card images according to selection in carousel
def holidayFilter(card_holiday_id):
    for card in cards.query.all():
        if card.holiday_id != int(card_holiday_id):
            card.include = "N"
        else:
            card.include = "Y"
            
        db.session.commit()
    return redirect('/home')

# Return templates for adding text and recipients once card is selected from home page
def addText(card_id):
    card = cards.query.get(int(card_id))
    return render_template("info.html", card=card, history=[], phmessage="Type something...", phname="David Smith", 
                            phaddress="500 Race Street", phcity="San Diego", phzip="95126")

# After submitting the text field
def submitAddText(card_id):
    newHistory = history(user_id=int(session["loggedInUserID"]), card_id=int(card_id), message=request.form["message"])
    db.session.add(newHistory)
    db.session.commit()
    card = cards.query.get(int(card_id))
    return render_template("info.html", card=card, history=newHistory, phmessage=newHistory.message, phname="David Smith", 
                            phaddress="500 Race Street", phcity="San Diego", phzip="95126")   

# If you return to edit at confirmation
def editText(card_id, history_id):
    queryHistory = history.query.get(int(history_id))
    card = cards.query.get(int(card_id))
    return render_template("info.html", card=card, history=queryHistory, phmessage=queryHistory.message, 
                            phname=queryHistory.assoc_contacts.full_name, phaddress=queryHistory.assoc_contacts.address, 
                            phcity=queryHistory.assoc_contacts.city, phzip=queryHistory.assoc_contacts.zip_code)

# Send to confirmation page although info has already been added to db
def confirmation(card_id, history_id):
    newContact = contacts(full_name=request.form["full_name"], address=request.form["address"], city=request.form["city"], zip_code=request.form["zip_code"], country=request.form["country"])
    db.session.add(newContact)
    db.session.commit()
    queryHistory = history.query.get(int(history_id)) 
    queryHistory.contact_id=newContact.id
    db.session.commit()
    card = cards.query.get(int(card_id))
    return render_template("confirmation.html", card=card, history=queryHistory)

# log out, return to login page
def logout():           
    session.clear()
    return redirect('/login')

# code used to initialize the cards database
# def initDB():
#     newHoliday = holidays(holiday="Thanksgiving Day", day="November 26")
#     db.session.add(newHoliday)
#     newHoliday = holidays(holiday="Christmas Day", day="December 25")
#     db.session.add(newHoliday)
#     newHoliday = holidays(holiday="New Year's Day", day="January 1")
#     db.session.add(newHoliday)
#     newHoliday = holidays(holiday="Memorial Day", day="May 25")
#     db.session.add(newHoliday)
#     newHoliday = holidays(holiday="Independence Day", day="July 3*")
#     db.session.add(newHoliday)
#     newHoliday = holidays(holiday="Labor Day", day="September 7")
#     db.session.add(newHoliday)
#     newHoliday = holidays(holiday="Columbus Day", day="October 12")
#     db.session.add(newHoliday)
#     newHoliday = holidays(holiday="Veterans Day", day="November 11")
#     db.session.add(newHoliday)


#     newCard = cards(holiday_id=1, image="thanks.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=2, image="christmas.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=3, image="new_year.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=4, image="memorial.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=5, image="independence.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=6, image="labor.png", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=7, image="columb.png", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=8, image="veteran.png", include="Y")
#     db.session.add(newCard)

#     newCard = cards(holiday_id=2, image="img-1.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=1, image="img-2.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=2, image="img-3.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=3, image="img-4.jpeg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=2, image="img-5.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=8, image="img-6.png", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=4, image="img-7.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=4, image="img-8.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=4, image="img-9.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=8, image="img-10.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=5, image="img-11.jpg", include="Y")
#     db.session.add(newCard)
#     newCard = cards(holiday_id=7, image="img-12.png", include="Y")
#     db.session.add(newCard)

#     db.session.commit()
#     print("all have been added!")
