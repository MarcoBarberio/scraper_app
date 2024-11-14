from transformers import AutoModelForCausalLM, AutoTokenizer
from .text_generation_interface import Text_generator_interface
import os
import torch.cuda as cuda
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
            self.model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-1.7B-Instruct")
            # con cuda si sposta il modello sulla gpu se abilitata
            if os.getenv("USE_GPU"): 
                if cuda.is_available():
                    self.model.to("cuda")
            self.tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-1.7B-Instruct")
            self.tokenizer.pad_token_id=self.tokenizer.eos_token_id
    
    def query(self,prompt):
        messages = [{"role": "user", "content": prompt}]
        input_text=self.tokenizer.apply_chat_template(messages, tokenize=False)
        inputs = self.tokenizer.encode(input_text, return_tensors="pt")
        outputs = self.model.generate(inputs, max_new_tokens=50, temperature=0.2, top_p=0.9, do_sample=True)
        # output è un insieme di token, quindi va decodificato
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)