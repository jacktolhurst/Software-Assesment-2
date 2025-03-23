from flask import Flask
from flask import render_template,url_for, jsonify
from flask import request
from flask import redirect
from flask_wtf.csrf import CSRFProtect
import user_management as dbHandler
import re
import html

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)
app.config["SECRET_KEY"] = 'fansonly122'
csrf = CSRFProtect(app)

@app.after_request
def addCSPHeader(response):
    csp_policy = (
        "default-src 'self'; "
        "script-src 'self' http://192.168.1.37:3000 https://getfreebootstrap.ru; "
        "style-src 'self' https://fonts.googleapis.com https://getfreebootstrap.ru; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self'; "
        "connect-src 'self';"
    )
    response.headers['Content-Security-Policy'] = csp_policy
    return response

@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@csrf.exempt
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = santiseHTML(request.form["feedback"])
        dbHandler.insertFeedback(feedback)
    
    feedback_data = dbHandler.listFeedback() 
    return render_template("/success.html", state=True, value="Back", feedback_data=feedback_data)



@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            feedback_data = dbHandler.listFeedback() 
            return render_template("/success.html", value=username, state=isLoggedIn, feedback_data=feedback_data)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")


@app.route('/checkDB', methods=['GET'])
def checkDatabase():
    search_string = request.args.get("username", "")

    if search_string:
        user_exists = dbHandler.checkUserExists(search_string)
        
        if user_exists:
            result = True
        else:
            result = False
    else:
        result = False

    return jsonify({'result': result})

def santiseHTML(text):
    return html.escape(text)

@app.template_filter('unsantiseHTML')
def unsantiseHTML(text):
    return html.unescape(text)

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=3000)