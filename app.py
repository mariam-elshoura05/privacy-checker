from flask import Flask, render_template, request
from privacycheck import get_page, check_trackers, check_headers, check_fingerprinting, check_cookies, calculate_risk
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    error = None
    url = None
    
    if request.method == "POST":
        url = request.form.get("url")
        try:
            response = get_page(url)
            soup = BeautifulSoup(response.text, "html.parser")
            
            trackers = check_trackers(soup, response.text)
            headers_results = check_headers(response)
            fingerprints = check_fingerprinting(response.text)
            cookie_results = check_cookies(response)
            risk = calculate_risk(trackers, headers_results, fingerprints, cookie_results)
            
            results = {
                "trackers": trackers,
                "headers": headers_results,
                "fingerprints": fingerprints,
                "cookies": cookie_results,
                "risk": risk,
                "url": url
            }
        except Exception as e:
            error = str(e)
    
    return render_template("index.html", results=results, error=error)

if __name__ == "__main__":
    app.runapp.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
