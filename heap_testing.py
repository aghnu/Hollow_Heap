"""
CMPUT403 Winter2021 Final Project
University of Alberta
Gengyuan Huang
gengyuan@ualberta.ca
"""

# terminal color
COLOR_PASS = '\033[92m'
COLOR_WARN = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_HEAD = '\033[95m'
COLOR_DEFA = '\033[0m'

# import needed module
try:
    from hollow_heap import HollowHeap as hp
except ImportError:
    print(f"{COLOR_WARN}ERROR: ./hollow_heap.py not found{COLOR_DEFA}")
    exit(1)
import heapq as heapq                       # used for varification
from random import shuffle, seed

# set random seed
RANDOM_SEED = 120

# tests
def test_basic_operation():
    print()
    print(f"{COLOR_HEAD} * Testing Basic Operations{COLOR_DEFA}")
    # test insertion, get_min, delete_min, get_content
    mockdata = [12,3,5,678,2345,2314,22,123234,2,1,2,12,6,7,8,9,77,23,2314,22,123234,2,1,2,12,6,7]
    mockdata_sorted = sorted(mockdata)
    
    """
    ************************************
        INSERTION TEST
    ************************************
    """
    try:
        hollow_heap = hp()
        hollow_heap_items = []
        for data in mockdata:
            hollow_heap_items.append(hollow_heap.insert(data,data))
            assert(len(hollow_heap_items) == len(hollow_heap))
    except AssertionError:
        print(f"\t{COLOR_FAIL} - insert() test failed{COLOR_DEFA}")
    else:
        print(f"\t{COLOR_PASS} - insert() test passed{COLOR_DEFA}")

    """
    *************************************
        FIND_MIN & DELETE_MIN TEST
    *************************************
    """
    try:
        for _ in range(len(hollow_heap)):
            assert(mockdata_sorted.pop(0) == hp.get_content(hollow_heap.get_min()))
            hollow_heap.delete_min()
        assert(len(hollow_heap) == 0)

    except AssertionError:
        print(f"\t{COLOR_FAIL} - find_min() & delete_min() test failed{COLOR_DEFA}")
    else:
        print(f"\t{COLOR_PASS} - find_min() & delete_min() test test passed{COLOR_DEFA}")

    """
    ************************************
        CONVERT ITERABLE TEST
    ************************************
    """
    try:
        hollow_heap = hp()
        hollow_heap_items = None
        mockup_pair_list = [(str(data), data) for data in mockdata]
        mockup_pair_iter = iter(mockup_pair_list)

        hollow_heap_items = hollow_heap.convert(mockup_pair_iter)
        assert(len(hollow_heap) == len(mockup_pair_list))
        assert(len(hollow_heap) == len(hollow_heap_items))

    except AssertionError:
        print(f"\t{COLOR_FAIL} - convert() test failed{COLOR_DEFA}")
    else:
        print(f"\t{COLOR_PASS} - convert() test passed{COLOR_DEFA}")
   
    """
    ************************************
        MERGE HEAP TEST
    ************************************
    """
    try:
        hollow_heap_1 = hp([(i,i) for i in mockdata])
        hollow_heap_2 = hp([(i,i) for i in reversed(mockdata)])

        mockdata_joined = mockdata + mockdata
        mockdata_joined.sort()

        hollow_heap_1.merge_heaps(hollow_heap_2, destroy=True)
        assert(len(hollow_heap_2) == 0)

        for data in mockdata_joined:
            old_len = len(hollow_heap_1)
            assert(data == hp.get_content(hollow_heap_1.get_min()))
            hollow_heap_1.delete_min()
            assert(old_len-1 == len(hollow_heap_1))

    except AssertionError:
        print(f"\t{COLOR_FAIL} - merge() test failed{COLOR_DEFA}")
    else:
        print(f"\t{COLOR_PASS} - merge() test passed{COLOR_DEFA}")

    """
    ************************************
        DECREASE KEY TEST
    ************************************
    """
    try:
        
        hollow_heap = hp()
        hollow_heap_items = []
        for data in mockdata:
            hollow_heap_items.append(hollow_heap.insert(data,data))

        seed(RANDOM_SEED)
        shuffle(hollow_heap_items)
        for item in hollow_heap_items:
            hollow_heap.decrease_key(item, hp.get_content(item)//2)     # //2 to all key but in shuffled order
        
        assert(len(hollow_heap) == len(mockdata))

        # checking
        mockdata_sorted = sorted(mockdata)
        for data in mockdata_sorted:
            assert(hp.get_content(hollow_heap.get_min())//2 == data//2)
            hollow_heap.delete_min()

    except AssertionError:
        print(f"\t{COLOR_FAIL} - decrease_key() test failed{COLOR_DEFA}")
    else:
        print(f"\t{COLOR_PASS} - decrease_key() test passed{COLOR_DEFA}")

    """
    ************************************
        DELETE TEST
    ************************************
    """
    try:
        
        hollow_heap = hp()
        hollow_heap_items = []
        for data in mockdata:
            hollow_heap_items.append(hollow_heap.insert(data,data))
        assert(len(hollow_heap) == len(mockdata))

        # remove first half of shuffled item
        seed(RANDOM_SEED)
        shuffle(hollow_heap_items)
        # split shuffled item into two parts, todelete, tokeep
        hollow_heap_todelete = hollow_heap_items[:len(hollow_heap_items)//2]
        hollow_heap_tokeep = hollow_heap_items[len(hollow_heap_items)//2:]
        for item in hollow_heap_todelete:
            hollow_heap.delete(item)
        assert(len(hollow_heap) == len(mockdata)//2)

        # check
        hollow_heap_tokeep_value_sorted = [hp.get_content(i) for i in hollow_heap_tokeep]
        hollow_heap_tokeep_value_sorted.sort()
        for _ in range(hollow_heap):
            item = hollow_heap.get_min()
            assert(item in hollow_heap_tokeep)
            assert(item not in hollow_heap_todelete)
            



    except AssertionError:
        print(f"\t{COLOR_FAIL} - delete() test failed{COLOR_DEFA}")
    else:
        print(f"\t{COLOR_PASS} - delete() test passed{COLOR_DEFA}")

    print()

def run_test_sequence():
    # run all tests
    test_basic_operation


if __name__ == "__main__":
    test_basic_operation()
        


    
    
    

