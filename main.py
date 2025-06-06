# NOTE is the symbol for a significant finding, inspecific from new or old functionality
# ! is the symbol for new functionality
# * is for precreated things

from flask import Flask, render_template,url_for, jsonify, request, redirect, send_from_directory
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import user_management as dbHandler
from urllib.parse import urlparse, urljoin
import html
import re

app = Flask(__name__)

# ! session information
app.config["SECRET_KEY"] = 'fansonly122'
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax", 
    SESSION_COOKIE_SECURE=True  
)
csrf = CSRFProtect(app)

# ! flask limiter for limiting requests
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# ! a list of allowed domains for invalid forwarding and redirecting
ALLOWED_DOMAINS = [
    "127.0.0.1:3000", 
    "172.20.10.4:3000" 
]

# ! adds the CSP to every request
@app.after_request
def addCSPHeader(response):
    csp_policy = (
        "default-src 'self'; "
        "script-src 'self'  https://127.0.0.1:3000; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self'; "
        "connect-src 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
    )
    response.headers['Content-Security-Policy'] = csp_policy
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers.pop("Server", None)
    return response

# ! lets the browser know that all entered JS files are JS files
# NOTE does not work with app.js, don't know why
@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename, mimetype='application/javascript;charset=utf-8')

# * the route for the feedback page
# ! checks if the URL is safe
# ! santises any inputs from the user as to HTML friendly
# ! limits the amount of calls available
@app.route("/success.html", methods=["POST", "GET"])
@csrf.exempt
@limiter.limit("0.5/second", override_defaults=False)
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

# * the signup page bluh bluh bulj
# ! checks if the URL is safe
# ! goes to the success page when signup, instead of the home page
# ! limits the amount of calls available
@app.route("/signup.html", methods=["POST", "GET"])
@limiter.limit("0.1/second", override_defaults=False)
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
        if dbHandler.insertUser(username, password, DoB):
            return render_template("/success.html")
        else:
            return render_template("/signup.html")
    else:
        return render_template("/signup.html")

# * the home/login page
# ! checks if the URL is safe
# ! limits the amount of calls available
@app.route("/index.html", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
@limiter.limit("5/second", methods=["POST", "GET"], override_defaults=False)
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

# ! checks the database for a username string given
# ! returns true if the user exists, false if it doesn't
@app.route('/checkDB', methods=['GET'])
@limiter.limit("20/second", override_defaults=False)
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

# ! checks if a given url is safe
# ! returns true if it is safe, false if it isn't
def isSafeURL(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.netloc and parsed_url.netloc not in ALLOWED_DOMAINS:
            return False  
        if parsed_url.scheme and parsed_url.scheme not in ["http", "https"]:
            return False  
        if re.search(r"[^\w\-/.:]", url):  
            return False  
        
        return True 
    except Exception:
        return False

# ! uses the HTML import to return a HTML safe version of a string
def santiseHTML(text):
    return html.escape(text)

# ! uses the HTML import to return an unsecaped version of the given string
@app.template_filter('unsantiseHTML')
def unsantiseHTML(text):
    return html.unescape(text)

# * general app startup
# ! ssl_context gives the permission for HTTPS
if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=3000, ssl_context=("cert.pem", "key.pem"))