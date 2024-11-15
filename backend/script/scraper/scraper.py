from .scraper_interface import Scraper_interface
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from ..utilities import get_domain
from urllib.parse import urljoin
#data una pagina web restituisce il contenuto della pagina
class Scraper(Scraper_interface):
    
    def __init__(self):
        pass
    
    # funzione che restituisce il plain text di una pagina
    def get_data(self, url):
        page_data={
            "plain_text":"",
            "redirect_links":[],
            "response_code":0
        }
        # si usa requests per ottenere il response code di http per la pagina
        try:
            response=requests.get(url)
            page_data["response_code"]=response.status_code
        except requests.exceptions.MissingSchema:
            return page_data
        # se il response code è diverso da 200 il caricamento della pagina non è andato a buon fine
        if response.status_code!=200:
            # nel caso lo status code fosse 403 si prova con una ricerca con selenium
            if response.status_code==403:
                self._dynamic_search(url,page_data)            
            return page_data
        # inizializzazione dell'oggetto beautiful soap che fa parsing statico
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ricerca statica con beautiful soap
        self._static_search(url,page_data,soup)
        return page_data

    # funzione che effettua lo scraping statico per la pagina
    def _static_search(self,url,page_data,soup):
        domain=get_domain(url)
        links=soup.find_all("a",href=True) #trova tutti gli anchor
        for link in links:
            href = link.get("href") #prende tutti gli href degli anchor trovati
                
            #href contiene solo link relativi. Si ricostruisce il link assoluto
            full_url = urljoin(url, href)
            #si controlla se il link effettua un redirect verso la stessa pagina. Nel caso viene scartato
            if full_url == url:
                continue      
            #si controlla se il link appartiene allo stesso dominio del padre
            full_url_domain = get_domain(full_url)
            if full_url_domain != domain:
                continue
            page_data["redirect_links"].append(full_url)
        # ricerca nei paragrafi
        paragraphs=soup.find_all("p")
        data = "\n".join(paragraph.text.strip() for paragraph in paragraphs)
        page_data["plain_text"]=data


    #funzione che effettua lo scraping dinamico per la pagina
    def _dynamic_search(self, url, page_data):
        domain=get_domain(url)
        
        driver=self._get_driver()     
        driver.get(url)   
        #ricerca dei link nella pagina
        redirect_links=driver.find_elements(By.TAG_NAME,"a")
        for link in redirect_links:
            href=link.get_attribute("href")
            #href contiene solo link relativi. Si ricostruisce il link assoluto
            full_url = urljoin(url, href)
            #si controlla se il link effettua un redirect verso la stessa pagina. Nel caso viene scartato
            if full_url == url:
                continue      
            #si controlla se il link appartiene allo stesso dominio del padre, altrimenti si scarta
            full_url_domain = get_domain(full_url)
            if full_url_domain != domain:
                continue
            page_data["redirect_links"].append(full_url)
        # ricerca nei paragrafi
        paragraphs=driver.find_elements(By.TAG_NAME,"p")
        data = "\n".join(paragraph.text.strip() for paragraph in paragraphs)
        page_data["plain_text"]=data
        driver.quit()
        
    
    #funzione che restituisce il driver di selenium
    def _get_driver(self):
        options = Options()
        # la modalità headless permette di un aprire una pagina di chrome
        options.add_argument("--headless")
        driver = Chrome( options=options)   
        return driver
