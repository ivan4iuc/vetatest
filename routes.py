from config import app
from controller_functions import login, submitLogin, register, submitRegistration, home, resetHome, holidayFilter, addText, submitAddText, editText, confirmation, logout#, initDB 

app.add_url_rule("/login", view_func=login)
app.add_url_rule("/submitLogin", view_func=submitLogin, methods=["POST"])
app.add_url_rule("/register", view_func=register)
app.add_url_rule("/submitRegistration", view_func=submitRegistration, methods=["POST"])
app.add_url_rule("/home", view_func=home)
app.add_url_rule("/resetHome", view_func=resetHome)
app.add_url_rule("/<card_holiday_id>/filter", view_func=holidayFilter)
app.add_url_rule("/<card_id>/addText", view_func=addText)
app.add_url_rule("/<card_id>/submitAddText", view_func=submitAddText, methods=["POST"])
app.add_url_rule("/<card_id>/<history_id>/editText", view_func=editText)
app.add_url_rule("/<card_id>/<history_id>/confirmation", view_func=confirmation, methods=["POST"])

app.add_url_rule("/logout", view_func=logout)

# app.add_url_rule("/initDB", view_func=initDB)
