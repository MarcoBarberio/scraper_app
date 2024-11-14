from flask import Blueprint, render_template, request, jsonify
from backend.script.text_generator.text_generation import Text_generator
from backend.script.scraper.scraper import Scraper
blueprint=Blueprint("main",__name__)

@blueprint.route("/")
#pagina iniziale con il form
def index():
    return render_template("index.html")

#post per fare lo scraping e la query
@blueprint.route("/scrape",methods=["POST"])
def scrape():
    #si prendono i dati dalla pagina html
    data=request.json
    url=data.get("url")
    query=data.get("query")
    
    scraper=Scraper()
    text_generator=Text_generator()
    #scraping della pagina
    result_scraping=scraper.get_data(url)
    
    # controllo se la pagina restituisce un codice di errore 
    if result_scraping["response_code"]!=200:
        return jsonify({"result":"error"})
    
    return jsonify({"result":result_scraping["plain_text"]})
    result_query=text_generator.query("""Ti sarà dato un testo che inizia e finisce dalla key word [TXT]\n
                poi ti sarà dato un argomento che inizia e finisce dalla key word [ARG]\n
                mi devi restituire le informazioni ricavate dal testo relative all'argomento passato\n\n
                [TXT]"""+result_scraping["plain_text"]+"[TXT]\n[ARG]"+query+"[ARG]")
    
    return jsonify({"result":result_query})
    

    