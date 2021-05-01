"""
CMPUT403 Winter2021 Final Project
University of Alberta
Gengyuan Huang
gengyuan@ualberta.ca

Usage:
    python3 ./heap_testing
    hollow_heap.py needs to be placed in working directory of heap_testing.py
"""

# terminal color
COLOR_PASS = '\033[92m'
COLOR_ORAN = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_HEAD = '\033[95m'
COLOR_DEFA = '\033[0m'
COLOR_BLUE = '\033[94m'

# import needed module
try:
    from hollow_heap import HollowHeap as hp
except ImportError:
    print(f"{COLOR_ORAN}ERROR: ./hollow_heap.py not found{COLOR_DEFA}")
    exit(1)
from random import shuffle, seed, randint

# set random seed
RANDOM_SEED = 231

# tests
def test_basic_operation():
    print(f"{COLOR_HEAD} * Testing Basic Operations{COLOR_DEFA}")
    # test insertion, get_min, delete_min, get_content

    for i in range(2):
        # run twice
        #   first time, small test set with narrow value
        #   second time, large test set with wide value

        if i==0:
            print(f"\n\t{COLOR_BLUE} * Small data with narrow value:{COLOR_DEFA}")
            seed(RANDOM_SEED)
            mockdata = [randint(0, 10**2) for i in range(10**3)]
            shuffle(mockdata)
        else:
            print(f"\n\t{COLOR_BLUE} * Large data with wide value:{COLOR_DEFA}")
            seed(RANDOM_SEED)
            mockdata = [randint(0, 10**10) for i in range(10**4)]
            shuffle(mockdata)
        
        
        """
        ************************************
            INSERTION TEST
        ************************************
        """
        mockdata_sorted = sorted(mockdata)
        try:
            hollow_heap = hp()
            hollow_heap_items = []
            for data in mockdata:
                hollow_heap_items.append(hollow_heap.insert(data,data))
                assert(len(hollow_heap_items) == len(hollow_heap))
        except AssertionError:
            print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - insert() test failed")
        else:
            print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - insert() test passed")

        """
        *************************************
            FIND_MIN & DELETE_MIN TEST
        *************************************
        """
        try:
            hollow_heap = hp()
            hollow_heap_items = []
            for _ in range(len(hollow_heap)):
                assert(mockdata_sorted.pop(0) == hp.get_content(hollow_heap.get_min()))
                hollow_heap.delete_min()
            assert(len(hollow_heap) == 0)

        except AssertionError:
            print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - get_min() & delete_min() test failed")
        else:
            print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - get_min() & delete_min() test passed")

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
            print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - convert() test failed")
        else:
            print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - convert() test passed")
    
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
            print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - merge() test failed")
        else:
            print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - merge() test passed")

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
            print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - decrease_key() test failed")
        else:
            print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - decrease_key() test passed")

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
            assert(len(hollow_heap) == len(hollow_heap_tokeep))

            # check
            hollow_heap_tokeep_value_sorted = [hp.get_content(i) for i in hollow_heap_tokeep]
            hollow_heap_tokeep_value_sorted.sort()
            hollow_heap_tokeep_value_sorted_iter = iter(hollow_heap_tokeep_value_sorted)
            for _ in range(len(hollow_heap)):
                item = hollow_heap.get_min()
                assert(item in hollow_heap_tokeep)          # check if item is in to keep
                assert(item not in hollow_heap_todelete)    # check if any deleted item got returned
                assert(hp.get_content(item) == next(hollow_heap_tokeep_value_sorted_iter))  # check if heap order is correct
                hollow_heap.delete_min()

        except AssertionError:
            print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - delete() test failed")
        else:
            print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - delete() test passed")

def test_general_usage():
    test_description_str = \
        """
        Test Data:
            This test uses a randomly generated and shuffled 
            dataset of size 30^4. Item value is generated 
            randomly from range(0, 10^10+1) with a pre-chosen 
            seed.
        
        Process:
            1. divide test data (already shuffled) into 3 
                equal length part.
            2. they are used as delete_set, decrease_set,
                and insert set
            3. create two heap called delete_heap and 
                decrease_heap
            4. init hollow_heap by merge from the two heap 
                (testing merge)
            5. for data in insert set:
                    do following operation on hollow_heap: 
                        delete(delete_set.pop())
                        # pre-chosen random seed
                        decrease(decrease_set[randomIndex]) 
                        insert(data)
                # iterate len(mockdata)//3 times
            6. construct a list from items (without knonw 
                the order), sort the list
            7. pop heap and compare

        Verification:
            Heap property (get_min() always returns a node 
            with min key) is verified using a sorted_list. 
            sorted_list.pop() is viewed as a correct heap.
            len(delete_set), len(decrease_set), and 
            len(insert_set) are also checked
        
        * This test will take a while ~10s
        """

    print(f"{COLOR_HEAD} * Testing General Usage{COLOR_DEFA}")
    print(f"\t{COLOR_ORAN}"+ test_description_str +f"{COLOR_DEFA}")



    seed(RANDOM_SEED)
    mockdata = [randint(0, 10**10) for i in range(30**4)]
    shuffle(mockdata)

    """
    ************************************
        MIX OPERATION TEST
    ************************************
    """
    # each loop do:
    #   delete
    #   decrease    (randomly choisen, new_key = old_key//2)
    #   insert

    # mock data is randomly seperated to 3 part
    #   delete_set
    #   decrease_set
    #   insert_set

    # result is verified using python sorted list
    # due to large data, performace maybe slow

    try:
        _run_mix_operation(mockdata)

    except AssertionError:
        print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - test mix operation failed")
    else:
        print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - test mix operation passed")

def test_edge_cases():
    print(f"{COLOR_HEAD} * Testing Edge Cases{COLOR_DEFA}")
    print()

    """
    *************************************
        ZERO TEST
    *************************************
    """
    try:
        mockdata = [0]*10**3
        _run_mix_operation(mockdata)

    except AssertionError:
        print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - test zeros failed")
    else:
        print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - test zeros passed")

    """
    *************************************
        ONE TEST
    *************************************
    """
    try:
        mockdata = [0]*10**3
        _run_mix_operation(mockdata)

    except AssertionError:
        print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - test ones failed")
    else:
        print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - test ones passed")

    """
    *************************************
        LARGE VALUE TEST
    *************************************
    """
    try:
        mockdata = [10**20]*10**3
        _run_mix_operation(mockdata)

    except AssertionError:
        print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - test large value failed")
    else:
        print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - test large value passed")

    """
    *************************************
        MIX ONES ZEROS TEST
    *************************************
    """
    try:
        mockdata = [0,1]*10**3
        _run_mix_operation(mockdata)

    except AssertionError:
        print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - test mix ones zeros failed")
    else:
        print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - test mix ones zeros passed")

    """
    *************************************
        EMPTY TEST
    *************************************
    """
    try:
        hollowhp = hp()
        assert(hollowhp.get_min() == None)
        assert(hollowhp.delete_min() == None)
        assert(hollowhp.insert(None, None) == None)
        assert(hollowhp.convert([]) == [])

    except AssertionError:
        print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - test empty failed")
    else:
        print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - test empty passed")

    """
    *************************************
        NEW KEY TEST
    *************************************
    """
    try:
        hollowhp = hp([(0,0)])
        hollowhp.decrease_key(hollowhp.get_min(), 1)

    except AssertionError:
        # note: reversed for this test cases
        print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - test bigger new key passed")
    else:
        print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - test bigger new key failed")

    """
    *************************************
        NEGATIVE KEY TEST
    *************************************
    """
    try:
        seed(RANDOM_SEED)
        mockdata = [randint(-(10**6), 0) for _ in range(10**3)]
        _run_mix_operation(mockdata)

    except AssertionError:
        print(f"\t{COLOR_FAIL}[failed]{COLOR_DEFA} - test negative key failed")
    else:
        print(f"\t{COLOR_PASS}[passed]{COLOR_DEFA} - test negative key passed")

def _run_mix_operation(dataset):
    seed(RANDOM_SEED)
    # mockdata is randomly generated and shuffled using given seed
    mockdata_delete = dataset[len(dataset)//3*0:len(dataset)//3*1]
    mockdata_decrease = dataset[len(dataset)//3*1:len(dataset)//3*2]
    mockdata_insert = dataset[len(dataset)//3*2:len(dataset)//3*3]

    # init items list, storing heap items from each dataset type
    # all items presented in following list is currenly inside heap
    
    hollow_heap_del = hp()
    hollow_heap_dec = hp()
    
    mockdata_delete_items = \
        hollow_heap_del.convert([(i,i) for i in mockdata_delete])
    mockdata_decrease_items = \
        hollow_heap_del.convert([(i,i) for i in mockdata_decrease])
    mockdata_insert_items = []

    # populate heap with mockdata_delete and mockdata_decrease using merge and convert
    hollow_heap = hp()
    hollow_heap.merge_heaps(hollow_heap_del)
    hollow_heap.merge_heaps(hollow_heap_dec)
    
    for data in mockdata_insert:
        # iterate len(mockdata)//3 times
        # each time will perform 3 operations, insert, decrease, delete

        # delete
        hollow_heap.delete(mockdata_delete_items.pop())

        # decrease_key
        selected_item = mockdata_decrease_items[randint(0,len(mockdata_decrease_items)-1)]

        # new key, also test negative
        # there is chance of 1/100 that a positive key will be decrase to -1
        # this random is also controlled by seed
        key = hp.get_content(selected_item)
        if key >= 0:
            if randint(0,100) == 0:
                new_key = -1
            else:
                new_key = key//2
        else:
            new_key = key - 10

        hollow_heap.decrease_key(selected_item, new_key)
        hp.set_content(selected_item, new_key)      # udpate its value, used for varification

        # insertion
        mockdata_insert_items.append(hollow_heap.insert(data, data))

    # varification
    # first construct correct result using python
    assert(len(mockdata_delete_items) == 0)
    assert(len(mockdata_insert_items) == len(mockdata_decrease_items))

    result_list_sorted = \
        [hp.get_content(i) for i in mockdata_insert_items] + \
        [hp.get_content(i) for i in mockdata_decrease_items]
    result_list_sorted.sort()

    # checking
    for data in result_list_sorted:
        assert(hp.get_content(hollow_heap.get_min()) == data)
        hollow_heap.delete_min()

def run_test_sequence():
    # run all tests
    print("-------------------------------------------------------")
    test_basic_operation()
    print("-------------------------------------------------------")
    test_edge_cases()
    print("-------------------------------------------------------")
    test_general_usage()
    print("-------------------------------------------------------")

if __name__ == "__main__":
    run_test_sequence()