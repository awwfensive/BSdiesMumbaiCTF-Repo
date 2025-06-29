from flask import Flask, request, render_template_string, session
import time
import random
import string

app = Flask(__name__)
app.secret_key = "authourlikecat69"  # Change this to a secure key in production

FLAG = "BMCTF{thankyou-thats-your-time_yay!}"

def generate_secret(length=6):
    """Generate a random secret of specified length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

@app.before_request
def set_session_secret():
    """Set a session secret if it doesn't already exist."""
    if 'secret' not in session:
        session['secret'] = generate_secret()  # Generate a secret for the session
        print(f"[SESSION STARTED] Secret for session: {session['secret']}")  # Logs to console

@app.route('/')
def index():
    """Main page to submit a query."""
    debug = request.args.get("debug") == "true"
    secret_display = f"<p><b>[DEBUG] Your session's secret: {session['secret']}</b></p>" if debug else ""
    return render_template_string(f"""
    <h1>XS-Search</h1>
    <p>Try to discover the secret using timing!</p>
    <form method="get" action="/search">
        <input name="q" placeholder="Enter query">
        <input type="submit" value="Search">
    </form>
    {secret_display}
    """)

@app.route('/search')
def search():
    """Handle the search query."""
    q = request.args.get("q", "")
    secret = session.get("secret")

    if not secret:
        return "Session error: No secret assigned."

    if q == "":
        return render_template_string("<p>No query given</p>")

    if q == secret:
        return f"Flag is: {FLAG}"

    # Timing attack logic: delay per correct char
    for i in range(min(len(q), len(secret))):
        if q[i] == secret[i]:
            time.sleep(0.05)  # Slight delay for each correct character
        else:
            break  # Stop checking as soon as a mismatch is found

    return f"No result for query: {q}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Set debug to False in production
