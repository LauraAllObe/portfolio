from flask import Flask, render_template, session
import os

app = Flask(__name__)
app.secret_key = '5305c0328237c354c422e0bae6da2b1b'  # Set a secret key for security purposes
#app.secret_key = os.environ.get('FLASK_SECRET_KEY')

@app.route('/')
def hello_world():
    # Initialize session data for slide indexes if it doesn't exist
    if 'slideIndexes' not in session:
        session['slideIndexes'] = [1, 1]  # Example for two slideshows
    return render_template('portfolio.html', slideIndexes=session['slideIndexes'])

if __name__ == '__main__':
    app.run(debug=True)
