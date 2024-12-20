import random
from urllib.parse import urlparse
import re
from dotenv import load_dotenv
import os
load_dotenv()
#si accede ad ogni pagina con un user agent diverso per evitare problemi di ban
def get_random_user_agent(): 
    user_agents = os.getenv("USER_AGENTS").split("-")
    return random.choice(user_agents)

def get_domain(url):
    #restituisce il dominio di una pagina
    return urlparse(url).netloc 

def get_resource_name(url):
    #restituisce il nome della risorsa (il nome della pagina o il nome del file senza estensione)
    resource=url.split("/")[-1].lower()
    if resource.endswith(os.getenv("EXTENSIONS")):
        return resource.split(".")[0]
    return resource

def get_extensions():
   return os.getenv("EXTENSIONS")

def get_file_extension(file):
    #restituisce l'estensione di un file
    return file.split("/")[-1].split(".")[1]

def is_valid_url(url): 
    #verifica la validità di un url
    parsed_url=urlparse(url)
    return all([parsed_url.scheme,parsed_url.netloc])

def get_random_words(text):
    #restituisce un insieme di parole casuali di un insieme di parole
    words=text.split()
    n=random.randint(10,20)
    if(n>len(words)):
        return text
    words=random.sample(words,n)
    result_text=""
    for word in words:
        result_text+=" "+word
    return result_text

def get_clean_url(url): 
    #dato un link lo rende più leggibile per il modello di text embedding
    return re.sub(r"[\/%/-/_/\d]"," ",url)

    