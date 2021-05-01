# Hollow Heap
CMPUT403 Winter2021 Final Project<br>
University of Alberta<br>
Gengyuan Huang<br>
gengyuan@ualberta.ca<br>

hollow_heap.py is a python implementation of Hollow Heap base on <br>
Thomas Dueholm Hansen, Haim Kaplan, Robert E. Tarjan, Uri Zwick 's paper <br>
https://arxiv.org/abs/1510.06535

## Description
Hollow Heap provides all the functionity of a binary heap. But all operations except *delete* and *delete_min* takes O(1) worst case. *delete* and *delete_min* takes O(logN) on a heap with N items.

Hollow Heap provides the same efficiency as the Fibonacci heap, but instead of using a set of trees, Hollow Heap uses DAG. This python implementation of the Hollow Heap is a two-parent hollow heap.

## Usage:
Place hollow_heap.py on the same directory as your code.
In your code, import HollowHeap

```python
import HollowHeap
```

## Testing:
To test hollow_heap.py, place heap_testing.py in the same directory as hollow_heap.py and run:

```bash
python3 heap_testing.py
```

## Methods
- ***insert(value, key): HeapItem***
    - this function create an heap item object with given content and then create a new node and insert the node into given heap
    - Time complexity: O(1)
- ***convert(iteral): List***
    - this method clear the heap and convert the given iterable into hollowheap 
    - Time complexity: O(N)
- ***get_min(): HeapItem***
    - this function returns a heap item that contains the minimal key
    - Time complexity: O(1)
- ***delete_min()***
    - this function deletes the minimal node without return it
    - Time complexity: O(logn)
- ***merge_heap(heap)***
    - this function merge given heap into this heap destory is default to True, which destroy the given heap heapitem from given heap is now pointing to nodes inside this heap if destory is set to False, a deepcopy is performed on given heap and will not affect any old reference in given heap
    - Time complexity: O(1)
- ***decrease_key(heap_item, key)***
    - this function decrease the key of given heap_item to key
    - Time complexity: O(1)
- ***delete(heap_item)***
    - this function deletes a heap_item from the heap
    - Time complexity: O(logn)
- ***get_content(heap_item): any type***
    - this function returns the content that is stored inside an _HeapItem objects
    - Time complexity: O(1)
- ***set_contentheap_item, new_value)***
    - this function change the content inside a heap item
    - Time complexity: O(1)

## Files
 - HollowHeap/
    - heap_testing.py
    - hollow_heap.py
    - test_output_screenshot.png
    - README.md

## Outputs
 - ***heap_testing.py***
    - test log is printed to stdin
    - color is used for displaying the result
        - green: pass
        - red: fail
        - yellow: description
        - blue: description
        - purple: name of the test class
    - each test class are grouped together and seperated by "----"
    - test classes
        - Basic Operations
            - testing specific method of the HollowHeap
        - Edge Cases
            - testing edge cases
        - General Usage
            - stress testing large data with mixed use of operations on one heap
    - test data
        - *Basic operations* and *General Usage* use random generated and shuffled mockup data (random seed is pre-chosen, so result can be replicate)
        - Some tests in *Edge Cases* use pre-defined mockup data, random generated and shuffled mockup data are also used (random seed is pre-chosen)
    - check test_output_screenshot.png for example of the output

 - ***hollow_heap***
    - class *HollowHeap* is exposed to user
    - methods of *HollowHeap* are documented in README and inside hollow_heap.py
    - the use of the *HollowHeap* is stright forward. use it as a custom python object. call method by "object.method()"
    - *HollowHeap* doesnt support hashing, and the HeapItem is not destoried when deleted or removed from a heap. User should only modify *HollowHeap* by using provided public methods.
    - file also contains private class and methods that should stay private. They are two static method of *HollowHeap* that can be used by user to retrieve value from a HeapItem

## Resources List
* Thomas Dueholm Hansen, Haim Kaplan, Robert E. Tarjan, Uri Zwick's paper "Hollow Heaps" <br>
[arXiv:1510.06535](https://arxiv.org/abs/1510.06535) [cs.DS]