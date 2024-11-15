from .node import NodeInterface

# Nodo che contiene le informazioni di un file
class URL_node(NodeInterface):
    def __init__(self, url, depth, father, resource_name, similarity):
        self.__url = url
        self.__depth = depth
        self.__father = father
        self.__children=[]
        if self.__father:
            self.__father.add_child(self)
    
    @property
    def url(self):
        return self.__url

    @property
    def depth(self):
        return self.__depth

    @property
    def father(self):
        return self.__father
    
    def add_child(self,child):
        self.__children.append(child)

    def to_string(self):
        return "URL "+str(self.depth)+": "+self.url+ " similarity: "+str(self.similarity)