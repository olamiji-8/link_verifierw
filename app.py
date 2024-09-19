from flask import Flask, request, render_template
import validators
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        is_valid, message = verify_url(url)
        return render_template('index.html', is_valid=is_valid, message=message, url=url)
    return render_template('index.html')

def verify_url(url):
    try:
        response = requests.get(url, timeout=5)  # Timeout for quick response
        if response.status_code == 200:
            return True, "The link is valid!"
        else:
            return False, f"The link returned a status code {response.status_code}."
    except requests.exceptions.RequestException as e:
        return False, f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)


# A simple heuristic phishing detection function
def is_phishing(url):
    if not validators.url(url):
        return False, "Invalid URL format."
    
    # Check for common phishing traits (you can expand this)
    phishing_keywords = ['login', 'verify', 'secure', 'bank', 'account', 'password', 'paypal']
    if any(keyword in url.lower() for keyword in phishing_keywords):
        return True, "Suspicious keywords found."

    # Example of using a public API to detect phishing (you can replace this with a more sophisticated solution)
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return True, "Website returned an unusual status."
    except:
        return True, "Unable to reach the website."

    return False, "URL seems fine."

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/check', methods=['POST'])
def check_url():
    url = request.form['url']
    phishing, message = is_phishing(url)
    return render_template('result.html', url=url, phishing=phishing, message=message)

if  __name__ == '__main__':
    app.run(debug=True)
