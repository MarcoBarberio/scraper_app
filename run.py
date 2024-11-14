from flask import Flask, request, jsonify, render_template
from script.scraper.scraper import Scraper
from script.text_generator.text_generation import Text_generator
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search', methods=['POST', 'GET'])
def search():
    data=request.get_json()
    url=data["url"]
    query=data["query"]
    scraper=Scraper()
    page_data=scraper.get_data(url)
    if page_data["response_code"]!=200:
        return jsonify({"result":"Error during the search execution"})
    return jsonify({"result":page_data["plain_text"]})
if __name__ == '__main__':
    app.run(debug=True)
