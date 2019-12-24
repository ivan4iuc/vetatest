from config import app
from controller_functions import login, submitLogin, register, submitRegistration, home, addText, submitAddText, submitAddRecipient, confirmation, logout#, initDB 

app.add_url_rule("/login", view_func=login)
app.add_url_rule("/submitLogin", view_func=submitLogin, methods=["POST"])
app.add_url_rule("/register", view_func=register)
app.add_url_rule("/submitRegistration", view_func=submitRegistration, methods=["POST"])
app.add_url_rule("/home", view_func=home)
app.add_url_rule("/<card_id>/addText", view_func=addText)
app.add_url_rule("/<card_id>/submitAddText", view_func=submitAddText, methods=["POST"])
app.add_url_rule("/<card_id>/<history_id>/submitAddRecipient", view_func=submitAddRecipient, methods=["POST"])
app.add_url_rule("/<card_id>/<history_id>/confirmation", view_func=confirmation)

app.add_url_rule("/logout", view_func=logout)

# app.add_url_rule("/initDB", view_func=initDB)
