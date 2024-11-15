from flask import Flask, request, jsonify, render_template
from script.crawler.crawler import Crawler
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
    # profondità massima per prendere informazioni
    depth=data["depth"]
    #query da domandare all'ai
    query=data["query"]
    crawler=Crawler() 
    pages_data=crawler.crawl(url,depth)
    #pages_data è un array contenente i dati delle pagine trovate
    #in text vengono inserite tutte le informazioni delle pagine separate da \n
    text = "\n".join1(pages_data)

    if not text:
        return jsonify({"result": "No text found on the page."})
    
    return jsonify({"result":text})
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
