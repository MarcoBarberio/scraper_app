from .text_generation_interface import Text_generator_interface
import google.generativeai as gemini
import os
import re
class Text_generator(Text_generator_interface):
     #il modello deve essere creato in singleton. 
    _instance = None 
    def __new__(cls): 
        #Viene chiamato da init per istanziare una istanza senza attributi
        if cls._instance is None:
            cls._instance = super(Text_generator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        #nel caso sia la prima volta che viene chiamato il costruttore l'istanza non ha attributi
        if not hasattr(self, 'model'): 
            gemini.configure(api_key=os.environ["GEMINI_API_KEY"])
            self.model=gemini.GenerativeModel("gemini-1.5-flash")
    
    def query(self,prompt):
        prompt=self._clean_text(prompt)
        return self.model.generate_content(prompt)
    
    # ripulisce il testo derivato dallo scraping
    def _clean_text(self,text):
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text