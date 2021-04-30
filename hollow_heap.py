"""
CMPUT403 Winter2021 Final Project
University of Alberta
Gengyuan Huang
gengyuan@ualberta.ca

a python implementation of Hollow Heap base on 
Thomas Dueholm Hansen, Haim Kaplan, Robert E. Tarjan, Uri Zwick 's paper
https://arxiv.org/abs/1510.06535

Usage:
    In your code, import HollowHeap class
    for detailed documentation on HollowHeap, please check HollowHeap
    all other functions/classes in this file is designed to be priviate

this code is tested on python 3.8.5
please check README.m for more detail about this project
"""

from copy import deepcopy

class HollowHeap:
    """
    a hollow heap python implemenation
    it supports following public method
    ********************************************
    HollowHeap.get_content(heap_item)        O(1)
        - parameters:
            heap_item   -> HeapItem
        -return:
            content     -> any type

    ********************************************
    self.convert(iteral)                    O(N)
        - parameters:
            iteral      -> iterable
        - return:
            None
    
    ********************************************
    self.insert(value, key)                 O(1)
        - parameters:
            value       -> any type 
            key         -> int
        - return:
            item        -> HeapItem
    
    ********************************************
    self.get_min()                          O(1)
        - return:
            item        -> HeapItem
    
    ********************************************
    self.delete_min()                    O(logn)
        - return:
            None
    
    ********************************************
    self.merge_heap(heap, destory=True)     O(1)
        - parameters:
            heap        -> HollowHeap
            destory     -> boolean
        - return:
            None

    ********************************************
    self.decrease_key(heap_item, key)       O(1)
        - parameters:
            heap_item   -> HeapItem
            key         -> int
        - return:
            None
    
    ********************************************
    self.delete(heap_item)               O(logn)
        - parameters:
            heap_item   -> HeapItem
        - return:
            None
    
    ********************************************
    """

    def __init__(self, iteral=None):
        """
        constructor method. if iteral is present, this iteral object
        will be used to initialize this heap, O(N) if iteral is present,
        else it has O(1)
        
        Parameters:
            iteral      -> iterable (contains 2-tuple (value, key) pair)
        Return:
            heap        -> HollowHeap
        """
        
        self.heap = None
        if iteral != None:
            self.convert(iteral)        # calling self.convert to add all item
    
    def convert(self, iteral):
        """
        this method clear the heap and convert the given iterable into 
        hollowheap 
        
        Parameters:
            iteral      -> iterable (contains 2-tuple (value, key) pair)
        Return:
            None

        Note:
            if iterable doesnt contain 2-tuple (value, key) pair, assertion error
            will rise
        """

        for i in iteral:
            assert(len(i) == 2)
            assert(type(i[1]) == int)
            self.insert(*i)
    
    def insert(self, item_content, key):
        """
        this function create an heap item object with given content
        and then create a new node and insert the node into given heap

        Parameters:
            value       -> any type 
            key         -> int 
        Return:
            item        -> HeapItem
        """
        e = _HeapItem(text=item_content)
        self.heap=_insert(e, key, self.heap)

        # return e
        return e

    def get_min(self):
        """
        this function returns a heap item that contains the minimal key

        Return:
            heap_item   -> HeapItem
        """

        return _find_min(self.heap)

    def delete_min(self):
        """
        this function deletes the minimal node without return it

        Return:
            None
        """
        self.heap=_delete_min(self.heap)

    def merge_heaps(self, heap, destroy=True):
        """
        this function merge given heap into this heap
        destory is default to True, which destroy the given heap
        heapitem from given heap is now pointing to nodes inside this heap
        if destory is set to False, a deepcopy is performed on given heap and
        will not affect any old reference in given heap

        Parameters:
            heap        -> HollowHeap
            destroy     -> boolean
        Return:
            None
        """

        heap_copy = heap if destroy else deepcopy(heap)
        self.heap = _meld(self.heap,heap_copy.heap)
        heap_copy.heap = None 

    def decrease_key(self, heap_item, key):
        """
        this function decrease the key of given heap_item to key

        Parameters:
            heap_item   -> HeapItem
            key         -> int
        Return:
            None
        """

        assert(heap_item.node.key > key)
        self.heap = _decrease_key(heap_item, key, self.heap)

    def delete(self, heap_item):
        """
        this function deletes a heap_item from the heap

        Parameters:
            heap_item   -> HeapItem
        Return:
            None
        """

        self.heap = _delete(heap_item, self.heap)

    @staticmethod
    def get_content(heap_item):
        """
        this function returns the content that is 
        stored inside an _HeapItem objects

        Paramters:
            heap_item   -> HeapItem
        Return:
            content     -> any type
        """
        return heap_item.text

# private dataclass that is used by HollowHeap
# are hidden from user
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
# are hidden from user
# these code are based on the pseudocode provided in Hansen et al.(2015)'s paper
# https://arxiv.org/abs/1510.06535
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
    if u is h:      # "is" compares if its the same reference
        u.key = k
        return h

    v = _make_node(e,k)
    
    u.item = None

    if u.rank > 2:
        v.rank = u.rank - 2     # core of hollow heap
    v.child = u                 # make u hollow, make v the second parent of v
    u.ep = v

    return _link(v,h)

def _delete_min(h):
    return _delete(h.item, h)

def _destroy_node(n):
    n.item = None
    n.child = None
    n.next_sib = None
    n.extr_prt = None
    n.key = -1
    n.rank = -1

def _delete(e,h):
    e.node.item = None
    e.node = None

    if h.item != None:      # not root deleteion
        return h

    # init
    max_rank = 0
    A = dict()

    # remove hollow nodes
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
        # destroy v
        _destroy_node(v)
    # _do_unranked-links()
    for i in range(max_rank+1):
        if i in A:
            if h == None:
                h = A[i]
            else:
                h = _link(h, A[i])
            del A[i]

    return h


            
