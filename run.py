from flask import Flask, request, jsonify, render_template
from script.scraper.scraper import Scraper
from script.text_generator.text_generation import Text_generator
app = Flask(__name__)

#quando si tira su il sito viene visualizzata questa pagina
@app.route('/')
def home():
    return render_template("index.html")

# funzione da avviare con una post
@app.route('/search', methods=['POST'])
def search():
    # la post invia url e query in un json chiamato request
    data=request.get_json()
    # url da cui prendere informazioni
    url=data["url"]
    #query da domandare all'ai
    query=data["query"]
    scraper=Scraper()
    page_data=scraper.get_data(url)
    #page_data è un dizionario contenente i dati della pagina e il codice di risposta della pagina
    # se il codice  di risposta è diverso da 200 c'è stato un qualche problema nello scraping
    if page_data["response_code"]!=200:
        return jsonify({"result":"Error during the search execution"})
    #in text vengono immagazinati i dati della pagina o niente di default (se c'è qualche problema) 
    text = page_data.get("plain_text", "")

    if not text:
        return jsonify({"result": "No text found on the page."})
    
    generator=Text_generator()
    #query da fare all'ai
    result=generator.query("I will give you a text followed by a query.\n"+
                           "you have to respond to the query using only informations that you can find on the text\n"+
                           "the text begins and finishes with [TXT] placeholder\n"+
                           "the query begins and finishes with [QUERY] placeholder\n"+
                           "give me a response without placeholders\n"+
                           "[TXT]"+text+"[TXT]\n"+
                           "[QUERY]"+query+"[QUERY]")
    
    #si restituisce un json con i risultati della query
    return jsonify({"result":result.text})
if __name__ == '__main__':
    #si avvia l'applicazione flask
    app.run(debug=True)
