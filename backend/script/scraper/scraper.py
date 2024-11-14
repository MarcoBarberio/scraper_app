from .scraper_interface import Scraper_interface
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
#data una pagina web restituisce il contenuto della pagina
class Scraper(Scraper_interface):
    
    def __init__(self):
        pass
    
    # funzione che restituisce il plain text di una pagina
    def get_data(self, url):
        page_data={
            "plain_text":"",
            "response_code":0
        }

        self._search(url,page_data)
        return page_data

    #funzione che effettua lo scraping per la pagina
    def _search(self, url, data_dict):
        # si usa requests per ottenere il response code di http per la pagina
        response=requests.get(url)
        data_dict["response_code"]=response.status_code
        # se il response code è diverso da 200 il caricamento della pagina non è andato a buon fine
        if response.status_code!=200:
            return
        driver=self._get_driver()     
        driver.get(url)   
        page_data=""
        # ricerca nei paragrafi
        paragraphs=driver.find_elements(By.TAG_NAME,"p")
        for paragraph in paragraphs:
            page_data+=paragraph.text+" "
        data_dict["plain_text"]=page_data
        driver.quit()
        
    
    #funzione che restituisce il driver di selenium
    def _get_driver(self):
        options = Options()
        # la modalità headless permette di un aprire una pagina di chrome
        options.add_argument("--headless")
        driver = Chrome( options=options)   
        return driver
