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

# Company specific routes (custom project lists and headings)
@app.get("/Affirm")
def affirm_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Affirm")

@app.get("/Akamai")
def akamai_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Akamai")

@app.get("/Amazon")
def amazon_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Amazon")

@app.get("/BAE_Systems")
def bae_systems_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="BAE Systems")
    
@app.get("/BeaconFire")
def beacon_fire_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="BeaconFire")

@app.get("/Celoxica")
def celoxica_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Celoxica")

@app.get("/Chalk")
def chalk_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Chalk")

@app.get("/GEVernova")
def ge_vernova_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="GE Vernova")

@app.get("/GoldmanSachs")
def goldman_sachs_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Goldman Sachs")

@app.get("/Google")
def google_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Google")

@app.get("/gp")
def gp_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="gp")

@app.get("/Heron")
def heron_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Heron")

@app.get("/IBM")
def ibm_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="IBM")

@app.get("/Icahn")
def icahn_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Icahn")

@app.get("/Intuit")
def intuit_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Intuit")

@app.get("/Jerry")
def jerry_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Jerry")

@app.get("/KKR")
def kkr_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="KKR")

@app.get("/Mercor")
def mercor_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Mercor")

@app.get("/Microsoft")
def microsoft_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Microsoft")

@app.get("/NYOAG")
def ny_oag_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="NY OAG")

@app.get("/NYTimes")
def ny_times_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="NY Times")

@app.get("/Optimum")
def optimum_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Optimum")

@app.get("/Ramp")
def ramp_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Ramp")

@app.get("/Thatch")
def thatch_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Thatch")

@app.get("/Zoetis")
def zoetis_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Zoetis")

@app.get("/Valon")
def valon_page():
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session['slideIndexes'], company="Valon")

if __name__ == '__main__':
    app.run(debug=True)
# activate venv first ".\.venv\Scripts\Activate.ps1"

#run locally using "python -m flask run"

#"python -m flask run --host=0.0.0.0"
