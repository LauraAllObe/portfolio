from flask import Flask, send_from_directory, render_template, session
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def hello_world():
    # Initialize session data for slide indexes if it doesn't exist
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]  # Example for two slideshows
    return render_template('portfolio.html', slideIndexes=session['slideIndexes'])

@app.get("/portfolio.md")
def portfolio_md():
    # Serve a static markdown file with correct content type
    return send_from_directory("static", "portfolio.md", mimetype="text/markdown")

@app.get("/sitemap.xml")
def sitemap_xml():
    return send_from_directory("static", "sitemap.xml", mimetype="application/xml")

@app.get("/portfolio.txt")
def portfolio_txt():
    return send_from_directory("static", "portfolio.txt", mimetype="text/plain")

# --- add below your existing @app.route('/') view ---
@app.get("/Google")
def google_page():
    # keep slide indexes behavior the same
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Google")

@app.get("/Amazon")
def amazon_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Amazon")

@app.get("/GEVernova")
def ge_vernova_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="GE Vernova")

if __name__ == '__main__':
    app.run(debug=True)
# activate venv first ".\.venv\Scripts\Activate.ps1"

#run locally using "python -m flask run"

#"python -m flask run --host=0.0.0.0"
