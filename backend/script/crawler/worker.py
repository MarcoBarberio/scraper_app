from ..tree.URL_node import URL_node
from ..scraper.scraper import Scraper
from ..utilities import get_resource_name
from queue import Empty

def worker(max_depth,visited_url,url_queue,result_queue,lock):
    scraper=Scraper()

    while True:
        try:
            node = url_queue.get()
        except Empty:
            continue
        #segnale di chiusura del thread
        if node is None: 
            url_queue.task_done()
            break
        if node.depth>=max_depth:
            url_queue.task_done()
            continue
        #restituisce tutti i link raggiungibili dalla pagina corrente
        print(node.url)
        links=scraper.get_data(node.url) 
        #se lo status code non è 200 c'è stato un errore nel reperimento di una pagina
        #se lo status code è 403 forse ci sono informazioni prese con selenium
        if links["response_code"] not in [200, 403]:
            url_queue.task_done()
            continue
        for link in links["redirect_links"]:
            with lock:                  
                #visited_url contiene i link già visitati e il suo accesso deve avvenire in mutua esclusione                
                if link in visited_url: 
                    continue
                visited_url.add(link)
                         
            new_node=URL_node(link,node.depth+1,node)
            url_queue.put(new_node)
        # i risultati dello scraping vengono messi nel rispettivo array
        for data in links["plain_text"]:
            result_queue.append(data)    
        url_queue.task_done()
    
