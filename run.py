from flask import Flask, request, jsonify, render_template
from script.scraper.scraper import Scraper
from script.text_generator.text_generation import Text_generator
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search', methods=['POST'])
def search():
    data=request.get_json()
    url=data["url"]
    query=data["query"]
    scraper=Scraper()
    page_data=scraper.get_data(url)
    if page_data["response_code"]!=200:
        return jsonify({"result":"Error during the search execution"})
    text = page_data.get("plain_text", "")

    if not text:
        return jsonify({"result": "No text found on the page."})
    generator=Text_generator()
    result=generator.query("I will give you a text followed by a query.\n"+
                           "you have to respond to the query using only informations that you can find on the text\n"+
                           "the text begins and finishes with [TXT] placeholder\n"+
                           "the query begins and finishes with [QUERY] placeholder\n"+
                           "give me a response without placeholders\n"+
                           "[TXT]"+text+"[TXT]\n"+
                           "[QUERY]"+query+"[QUERY]")
    return jsonify({"result":result.text})
if __name__ == '__main__':
    app.run(debug=True)
