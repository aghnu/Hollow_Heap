# CMPUT403 Winter2021 Final Project
# University of Alberta
# Gengyuan Huang
# gengyuan@ualberta.ca

from copy import deepcopy

class HollowHeap:
    """
    a hollow heap that supports
        -
        -
        -
        -
    """
    def __init__(self):
        self.heap = None
    
    def insert(self, item_content, key):
        """
        this function create an heap item object with given content
        and then create a new node and insert the node into given heap
        """
        e = _HeapItem(text=item_content)
        self.heap=_insert(e, key, self.heap)

        # return e
        return e

    def get_min(self):
        """
        this function returns a heap item 
        that contains the minimal key
        """
        return _find_min(self.heap)

    def delete_min(self):
        self.heap=_delete_min(self.heap)

    def merge_heaps(self, heap, destory=True):
        """
        """
        heap_copy = heap if destory else deepcopy(heap)
        self.heap = _meld(self.heap,heap_copy.heap)
        heap_copy.heap = None 

    def decrease_key(self, heap_item, key):
        """
        """
        self.heap = _decrease_key(heap_item, key, self.heap)

    def delete(self, heap_item, heap):
        self.heap = _delete(heap_item, self.heap)

    @staticmethod
    def get_content(heap_item):
        """
        this function returns the content that is 
        stored inside an _HeapItem objects
        """
        return heap_item.text

# private dataclass that is used by HollowHeap
class _HeapItem:
    """
    a private dataclass, used for storing
    the state of an item that belongs to a hollow node
    """
    def __init__(self, node=None, text=None):
        self.node = node     # node that contains this _HeapItem
        self.text = text     # actually content stored in this _HeapItem

class _HeapNode:
    """
    a private dataclass, used for storing 
    the state of a node that belongs to a hollow heap
    """
    # pointers
    def __init__(self, item=None, child=None, next_sib=None, extr_prt=None, key=0, rank=0):
        
        self.item = item            # _HeapItem, None indicating this node is hollow
        self.child = child          # first child, None indicating there is no children
        self.next_sib = next_sib    # next sibling, None indicating this is the last children
        self.extr_prt = extr_prt    # second parent, None indicating there is no second parent

        # data
        self.key = key          # key of the node
        self.rank = rank        # rank of the node

# private functions that is used by HollowHeap
def _add_child(v,w):
    # v, w are nodes
    # make v to be w's child
    # make w to be v's parent
    v.next_sib = w.child
    w.child = v

def _link(v,w):
    # v, w are nodes
    if v.key >= w.key:
        _add_child(v,w)
        return w
    else:
        _add_child(w,v)
        return v

def _make_node(e,k):
    # e is a heap item
    # k is the key
    u = _HeapNode(item=e,key=k,rank=0)
    e.node = u
    return u

def _insert(e,k,h):
    # h is a heap node
    return _meld(_make_node(e,k),h)

def _meld(g,h):
    # g, h are heap nodes
    if g == None:
        return h
    if h == None:
        return g
    return _link(g,h)

def _find_min(h):
    if h == None:
        return None
    else:
        return h.item

def _decrease_key(e,k,h):
    u = e.node
    if u is h:
        u.key = k
        return h

    v = _make_node(e,k)
    
    u.item = None

    if u.rank > 2:
        v.rank = u.rank - 2
    v.child = u
    u.ep = v

    return _link(v,h)

def _delete_min(h):
    return _delete(h.item, h)

def _delete(e,h):
    e.node.item = None
    e.node = None

    if h.item != None:
        return h

    max_rank = 0
    A = dict()
    while h != None:
        w = h.child
        v = h
        h = h.next_sib
        while w != None:
            u = w
            w = w.next_sib
            if u.item == None:
                if u.extr_prt == None:
                    u.next_sib = h
                    h = u
                else:
                    if u.extr_prt is v:
                        w == None
                    else:
                        u.next_sib = None
                    u.extr_prt = None
            else:
                # _do_ranked_links(u)
                while u.rank in A:
                    u = _link(u,A[u.rank])
                    del A[u.rank]
                    u.rank = u.rank + 1
                A[u.rank] = u
                max_rank = max(u.rank, max_rank)
    
    # _do_unranked-links()
    for i in range(max_rank+1):
        if i in A:
            if h == None:
                h = A[i]
            else:
                h = _link(h, A[i])
            del A[i]

    return h


            
