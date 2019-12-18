from config import app
from controller_functions import login, submitLogin, register, submitRegistration, home, addText, addRecipient, confirmation, submitCard, cardSent, logout

app.add_url_rule("/login", view_func=login)
app.add_url_rule("/submitLogin", view_func=submitLogin, methods=["POST"])
app.add_url_rule("/register", view_func=register)
app.add_url_rul("/submitRegistration", view_func=submitRegistration, methods=["POST"])
app.add_url_rule("/home", view_func=home)
app.add_url_rule("/<card_id>/addText", view_func=addText)
app.add_url_rule("/<card_id>/addRecipient", view_func=addRecipient)
app.add_url_rule("/<card_id>/confirmation", view_func=confirmation)
app.add_url_rule("/submitCard", view_func=submitCard, methods=["POST"])
app.add_url_rule("/cardSent", view_func=cardSent)

app.add_url_rule("/logout", view_func=logout)
