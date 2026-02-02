from flask import Flask, send_from_directory, render_template, session
from werkzeug.routing import BaseConverter
from dotenv import load_dotenv
import os
from pathlib import Path

# Detect Vercel environment
IS_VERCEL = os.getenv("VERCEL") == "1"
VERCEL_ENV = os.getenv("VERCEL_ENV")  # "production" | "preview" | "development"
IS_PROD = (VERCEL_ENV == "production") or (os.getenv("FLASK_ENV") == "production")

# Only load .env locally (or vercel dev)
if not IS_VERCEL:
    load_dotenv()

# Repo root is one level above /api
REPO_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = REPO_ROOT / "static"
TEMPLATES_DIR = STATIC_DIR / "templates"

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path="/static",  # ensures /static/... URLs work
)

secret = os.getenv("SECRET_KEY")
if not secret:
    raise RuntimeError("SECRET_KEY is required")
app.config["SECRET_KEY"] = secret


# Custom URL converter - automatically converts all incoming URLs to lowercase
class LowercaseConverter(BaseConverter):
    def to_python(self, value):
        return value.lower()

    def to_url(self, value):
        return value.lower()

app.url_map.converters["lowercase"] = LowercaseConverter

# Valid company keys (all lowercase) - includes all previously defined companies
VALID_COMPANIES = {
    'affirm', 'akamai', 'amazon', 'bae_systems', 'beaconfire', 'brex', 'celoxica',
    'chalk', 'citadelsecurities', 'flex', 'gevernova', 'github', 'goldmansachs',
    'google', 'gp', 'greenway', 'heron', 'ibm', 'icahn', 'intuit', 'jerry',
    'kkr', 'mercor', 'microsoft', 'nyoag', 'nytimes', 'optimum', 'precisely',
    'ramp', 'revature', 'rokt', 'runpod', 'squarespace', 'stayd', 'thatch', 'valon',
    'wanderlog', 'zoetis',
}

# Mapping of company keys to display names with proper spacing and capitalization
COMPANY_DISPLAY_NAMES = {
    'testcompany': 'Test Company',
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

@app.route("/")
def hello_world():
    if "slideIndexes" not in session:
        session["slideIndexes"] = [1, 1]
    return render_template("portfolio.html", slideIndexes=session["slideIndexes"], company_display="")

@app.get("/portfolio.md")
def portfolio_md():
    return send_from_directory(str(STATIC_DIR), "portfolio.md", mimetype="text/markdown")

@app.get("/sitemap.xml")
def sitemap_xml():
    return send_from_directory(str(STATIC_DIR), "sitemap.xml", mimetype="application/xml")

@app.get("/portfolio.txt")
def portfolio_txt():
    return send_from_directory(str(STATIC_DIR), "portfolio.txt", mimetype="text/plain")

@app.get("/<lowercase:company_key>")
def company_page(company_key):
    valid_company = find_company(company_key)
    if not valid_company:
        return "Company not found", 404

    if "slideIndexes" not in session:
        session["slideIndexes"] = [1, 1]

    company_display = COMPANY_DISPLAY_NAMES.get(valid_company, valid_company)

    return render_template(
        "portfolio.html",
        slideIndexes=session["slideIndexes"],
        company=valid_company,
        company_display=company_display,
    )

# Optional: only for running locally via `python api/index.py`
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=True)
