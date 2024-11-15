from .crawler_interface import Crawler_interface
from ..utilities import is_valid_url
from ..tree.URL_node import URL_node
from queue import Queue
import threading
from .worker import worker

#Data una pagina, fa lo scrape fino ad un livello fissato. Restituisce una coda con i risultato dello scrape
class Crawler(Crawler_interface):
    def __init__(self):
        self._n_threads=30
    
    def crawl(self,root_url,max_depth):
        if not is_valid_url(root_url):
            return
        
        root=URL_node(root_url,0,None)
        #Coda che contiene le pagine web da cui prendere le informazioni. Queue è threadsafe
        url_queue=Queue() 
        url_queue.put(root)
        #Array di file che contengono preferibilmente bilanci di sosteniblità
        result_queue=[] 
        visited_url=set()
        lock=threading.Lock()
        threads=[]
        
        for i in range(self._n_threads):
            thread=threading.Thread(target=worker,args=(max_depth,visited_url,url_queue,result_queue,lock))
            #ogni thread naviga le pagine e ne estrae i link
            thread.start()
            threads.append(thread)
        url_queue.join()
        #Segnale di terminazione dei thread
        for thread in threads:
            url_queue.put(None)
        #join dei thread
        for thread in threads:
            thread.join()
       
        return result_queue