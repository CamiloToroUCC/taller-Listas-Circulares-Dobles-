class Node:
    """
    Cada nodo almacena y tiene punteros que permiten recorrer la lista
    en ambas direcciones.
    """
    def __init__(self, data):
        self.data = data      # dato del nodo 
        self.next = None      # puntero al siguiente nodo
        self.prev = None      # puntero al nodo anterior

class CircularDoublyLinkedList:
    # La ultima posicion se conecta de nuevo con el inicio, lo que facilita el recorrido cíclico
    def __init__(self):
        self.head = None  # La lista inicia vacía

    def insert(self, data):
        # Si la lista est vacía el nodo se auto-referencia en sus punteros next y prev
        newNode = Node(data)
        if not self.head:
            self.head = newNode
            newNode.next = newNode    # Como es el único nodo se apunta ael mismo
            newNode.prev = newNode
        else:
            last = self.head.prev
            last.next = newNode        # ultimo nodo apunta al nuevo nodo
            newNode.prev = last        # nuevo nodo apunta hacia atras
            newNode.next = self.head   # siguiente es la cabeza
            self.head.prev = newNode   # headd actualiza su puntero 'prev' al nuevo nodo

    def traverse(self):
        # Recorre la lista circular y devuelve una lista con los datos almacenados
        elements = []
        if not self.head:
            return elements
        current = self.head
        while True:
            elements.append(current.data)
            current = current.next
            if current == self.head:
                break
        return elements
