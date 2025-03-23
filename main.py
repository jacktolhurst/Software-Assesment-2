from flask import Flask, render_template,url_for, jsonify, request, redirect
from flask_wtf.csrf import CSRFProtect
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
import user_management as dbHandler
import html
from urllib.parse import urlparse, urljoin



# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)
app.config["SECRET_KEY"] = 'fansonly122'
csrf = CSRFProtect(app)
# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["200 per day", "50 per hour"],
#     storage_uri="memory://",
# )
ALLOWED_DOMAINS = [
    "127.0.0.1:3000", 
    "172.20.10.4:3000" 
]

@app.after_request
def addCSPHeader(response):
    csp_policy = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self'; "
        "connect-src 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "report-to /csp-violation-report-endpoint;"
        "Content-Security-Policy: upgrade-insecure-requests;"
        "report-to csp-endpoint;"
    )
    response.headers['Content-Security-Policy'] = csp_policy
    response.headers["X-Frame-Options"] = "DENY"
    return response

@app.route("/success.html", methods=["POST", "GET"])
@csrf.exempt
# @limiter.limit("0.5/second", override_defaults=False)
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        if not isSafeURL(url):
            return "Forbidden redirect!", 403
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = santiseHTML(request.form["feedback"])
        dbHandler.insertFeedback(feedback)
    
    feedback_data = dbHandler.listFeedback() 
    return render_template("/success.html", state=True, value="Back", feedback_data=feedback_data)



@app.route("/signup.html", methods=["POST", "GET"])
# @limiter.limit("0.1/second", override_defaults=False)
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        if not isSafeURL(url):
            return "Forbidden redirect!", 403
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
# @limiter.limit("1/second", methods=["POST", "GET"], override_defaults=False)
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        if not isSafeURL(url):
            return "Forbidden redirect!", 403
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
# @limiter.limit("3/second", override_defaults=False)
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

def isSafeURL(url):
    print("URL passed:", url)
    base_url = "http://127.0.0.1:3000"  
    full_url = urljoin(base_url, url)

    parsed_url = urlparse(full_url)
    return parsed_url.netloc in ALLOWED_DOMAINS

def santiseHTML(text):
    return html.escape(text)

@app.template_filter('unsantiseHTML')
def unsantiseHTML(text):
    return html.unescape(text)

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=3000)