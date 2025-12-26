from flask import Flask, send_from_directory, render_template, session
from werkzeug.routing import BaseConverter
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Custom URL converter - automatically converts all incoming URLs to lowercase
class LowercaseConverter(BaseConverter):
    def to_python(self, value):
        return value.lower()
    
    def to_url(self, value):
        return value.lower()

app.url_map.converters['lowercase'] = LowercaseConverter

# Valid company keys (all lowercase) - includes all previously defined companies
VALID_COMPANIES = {
    'affirm', 'akamai', 'amazon', 'bae_systems', 'beaconfire', 'celoxica',
    'chalk', 'citadelsecurities', 'flex', 'gevernova', 'goldmansachs',
    'google', 'gp', 'greenway', 'heron', 'ibm', 'icahn', 'intuit', 'jerry',
    'kkr', 'mercor', 'microsoft', 'nyoag', 'nytimes', 'optimum', 'precisely',
    'ramp', 'revature', 'rokt', 'runpod', 'stayd', 'thatch', 'valon',
    'wanderlog', 'zoetis',
}

# Mapping of company keys to display names with proper spacing and capitalization
COMPANY_DISPLAY_NAMES = {
    'affirm': 'Affirm',
    'akamai': 'Akamai',
    'amazon': 'Amazon',
    'bae_systems': 'BAE Systems',
    'beaconfire': 'Beaconfire',
    'celoxica': 'Celoxica',
    'chalk': 'Chalk',
    'citadelsecurities': 'Citadel Securities',
    'flex': 'Flex',
    'gevernova': 'Gevernova',
    'goldmansachs': 'Goldman Sachs',
    'google': 'Google',
    'gp': 'GP',
    'greenway': 'Greenway',
    'heron': 'Heron',
    'ibm': 'IBM',
    'icahn': 'Icahn',
    'intuit': 'Intuit',
    'jerry': 'Jerry',
    'kkr': 'KKR',
    'mercor': 'Mercor',
    'microsoft': 'Microsoft',
    'nyoag': 'NY OAG',
    'nytimes': 'NY Times',
    'optimum': 'Optimum',
    'precisely': 'Precisely',
    'ramp': 'Ramp',
    'revature': 'Revature',
    'rokt': 'ROKT',
    'runpod': 'RunPod',
    'stayd': 'StayD',
    'thatch': 'Thatch',
    'valon': 'Valon',
    'wanderlog': 'Wanderlog',
    'zoetis': 'Zoetis',
}

def find_company(input_key):
    """
    Find a valid company by normalizing various formatting variations.
    Handles hyphens, underscores, and mixed formatting.
    """
    # First try direct match (already lowercase from converter)
    if input_key in VALID_COMPANIES:
        return input_key
    
    # Try with hyphen to underscore conversion
    normalized = input_key.replace('-', '_')
    if normalized in VALID_COMPANIES:
        return normalized
    
    # Try removing all special chars/underscores and match alphanumeric
    input_no_special = ''.join(c for c in input_key if c.isalnum())
    for company in VALID_COMPANIES:
        company_no_special = ''.join(c for c in company if c.isalnum())
        if input_no_special == company_no_special:
            return company
    
    return None

@app.route('/')
def hello_world():
    # Initialize session data for slide indexes if it doesn't exist
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]  # Example for two slideshows
    return render_template('portfolio.html', slideIndexes=session['slideIndexes'], company_display='')

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

# Unified company route - accepts any case and converts to lowercase
@app.get("/<lowercase:company_key>")
def company_page(company_key):
    # Try to find the company with various formatting normalizations
    valid_company = find_company(company_key)
    
    if not valid_company:
        return "Company not found", 404
    
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]
    
    company_display = COMPANY_DISPLAY_NAMES.get(valid_company, valid_company)
    
    return render_template("portfolio.html", 
                          slideIndexes=session['slideIndexes'], 
                          company=valid_company,
                          company_display=company_display)

if __name__ == '__main__':
    app.run(debug=True)
# activate venv first ".\.venv\Scripts\Activate.ps1"

#run locally using "python -m flask run"

#"python -m flask run --host=0.0.0.0"
