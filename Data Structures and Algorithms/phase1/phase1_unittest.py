
import unittest
from phase1 import SList2

class Test(unittest.TestCase):


    #setUp is a method which is run before a test method is executed.
    #This is useful if you need some data (for example) to be present before running a test.
    def setUp(self):
        # Empty list
        self.empty_list = SList2()
        self.expected_empty = SList2()

        # One element list
        self.one_element = SList2()
        self.one_element.addLast(1)

        # Simple several elements list
        self.simple_list = SList2()
        self.expected_simple = SList2()
        for i in range(10):
            self.simple_list.addLast(i+1)
            self.expected_simple.addLast(i+1)

        # Sequences of same elements list
        self.sequences_list = SList2()
        self.expected_sequences = SList2()
        for i in [1,1,2,2,2,3,3,3,3,4,4,4,5,5,5,5,6,6,7,8,8,8]:
            self.sequences_list.addLast(i)
        for i in [1,1,2,2,2,3,3,3,3,4,4,4,6,6,7,8,8,8]:
            self.expected_sequences.addLast(i)

        # Largest at the start
        self.largest_start_list = SList2()
        self.expected_start = SList2()
        for i in [1,1,1,1,2,2,2,3,3,4,4,4,5,6]:
            self.largest_start_list.addLast(i)
        for i in [2,2,2,3,3,4,4,4,5,6]:
            self.expected_start.addLast(i)

        # Lists for tests for leftrightShift
        self.shiftedlist = SList2()
        self.expected_True3 = SList2()
        self.expected_True7 = SList2()
        self.expected_True1 = SList2()
        self.expected_False1 = SList2()
        self.expected_False6 = SList2()
        self.expected_False9 = SList2()
        self.expected_nochange = SList2()
        for i in [1,2,3,4,5,6,7,8,9,10]:
            self.shiftedlist.addLast(i)
            self.expected_nochange.addLast(i)
        for i in [4,5,6,7,8,9,10,1,2,3]:
            self.expected_True3.addLast(i)
        for i in [8,9,10,1,2,3,4,5,6,7]:
            self.expected_True7.addLast(i)
        for i in [2,3,4,5,6,7,8,9,10,1]:
            self.expected_True1.addLast(i)
        for i in [10,1,2,3,4,5,6,7,8,9]:
            self.expected_False1.addLast(i)
        for i in [5,6,7,8,9,10,1,2,3,4]:
            self.expected_False6.addLast(i)
        for i in [2,3,4,5,6,7,8,9,10,1]:
            self.expected_False9.addLast(i)


    """
    Function 1 --- delLargestSeq --- tests
    """
    # Case 1 - Empty list
    def test_delLargestSeq1(self):
        self.empty_list.delLargestSeq()
        self.assertEqual(str(self.empty_list), str(self.expected_empty))
        self.assertEqual(len(self.empty_list), len(self.expected_empty))

    # Case 2 - One element list
    def test_delLargestSeq2(self):
        self.one_element.delLargestSeq()
        self.assertEqual(str(self.one_element), str(self.expected_empty))
        self.assertEqual(len(self.one_element), len(self.expected_empty))

    # Case 3 - One to 10 list
    def test_delLargestSeq3(self):
        self.simple_list.delLargestSeq()
        self.expected_simple.removeLast()
        self.assertEqual(str(self.simple_list), str(self.expected_simple))
        self.assertEqual(len(self.simple_list), len(self.expected_simple))

    # Case 4 - Different sequences list
    def test_delLargestSeq4(self):
        self.sequences_list.delLargestSeq()
        self.assertEqual(str(self.sequences_list), str(self.expected_sequences))
        self.assertEqual(len(self.sequences_list), len(self.expected_sequences))

    # Case 5 - Largest sequence at the start
    def test_delLargestSeq5(self):
        self.largest_start_list.delLargestSeq()
        self.assertEqual(str(self.largest_start_list), str(self.expected_start))
        self.assertEqual(len(self.largest_start_list), len(self.expected_start))

    """
    Function 2 --- fixloop --- tests
    """
    # Case 1 - No loop
    def test_fix_loop1(self):
        self.assertEqual(self.simple_list.fix_loop(), False)
        self.assertEqual(str(self.simple_list), "1,2,3,4,5,6,7,8,9,10")

    # Case 2 - Loop at head
    def test_fix_loop2(self):
        self.simple_list.create_loop(0)
        self.assertEqual(self.simple_list.fix_loop(), True)
        self.assertEqual(str(self.simple_list), "1,2,3,4,5,6,7,8,9,10")

    # Case 3 - Loop at second node
    def test_fix_loop3(self):
        self.simple_list.create_loop(1)
        self.assertEqual(self.simple_list.fix_loop(), True)
        self.assertEqual(str(self.simple_list), "1,2,3,4,5,6,7,8,9,10")

    # Case 4 - Loop at end node
    def test_fix_loop4(self):
        self.simple_list.create_loop(len(self.simple_list)-1)
        self.assertEqual(self.simple_list.fix_loop(), True)
        self.assertEqual(str(self.simple_list), "1,2,3,4,5,6,7,8,9,10")

    # Case 5 - Other list try - other node
    def test_fix_loop5(self):
        self.sequences_list.create_loop(len(self.sequences_list)-5)
        self.assertEqual(self.sequences_list.fix_loop(), True)
        self.assertEqual(str(self.sequences_list), "1,1,2,2,2,3,3,3,3,4,4,4,5,5,5,5,6,6,7,8,8,8")

    """
    Function 3 --- leftrightShift --- tests
    """
    # Case 1 - Shift True 3
    def test_leftrightShift1(self):
        self.shiftedlist.leftrightShift(True, 3)
        self.assertEqual(str(self.shiftedlist),str(self.expected_True3))
        self.assertEqual(len(self.shiftedlist),10)

    # Case 2 - Shift True 7
    def test_leftrightShift2(self):
        self.shiftedlist.leftrightShift(True, 7)
        self.assertEqual(str(self.shiftedlist),str(self.expected_True7))
        self.assertEqual(len(self.shiftedlist),10)
    # Case 3 - Shift True 1
    def test_leftrightShift3(self):
        self.shiftedlist.leftrightShift(True, 1)
        self.assertEqual(str(self.shiftedlist),str(self.expected_True1))
        self.assertEqual(len(self.shiftedlist),10)

    # Case 4 - Shift False 1
    def test_leftrightShift4(self):
        self.shiftedlist.leftrightShift(False, 1)
        self.assertEqual(str(self.shiftedlist),str(self.expected_False1))
        self.assertEqual(len(self.shiftedlist),10)

    # Case 5 - Shift False 6
    def test_leftrightShift5(self):
        self.shiftedlist.leftrightShift(False, 6)
        self.assertEqual(str(self.shiftedlist),str(self.expected_False6))
        self.assertEqual(len(self.shiftedlist),10)

    # Case 6 - Shift False 9
    def test_leftrightShift6(self):
        self.shiftedlist.leftrightShift(False, 9)
        self.assertEqual(str(self.shiftedlist),str(self.expected_False9))
        self.assertEqual(len(self.shiftedlist),10)

    # Case 7 - Shift True Empty
    def test_leftrightShift7(self):
        self.empty_list.leftrightShift(True, 1)
        self.assertEqual(str(self.empty_list),str(self.expected_empty))
        self.assertEqual(len(self.empty_list),0)

    # Case 8 - Shift False Empty
    def test_leftrightShift8(self):
        self.empty_list.leftrightShift(False, 1)
        self.assertEqual(str(self.empty_list),str(self.expected_empty))
        self.assertEqual(len(self.empty_list),0)


    # Case 9 - Shift True Higher
    def test_leftrightShift9(self):
        self.shiftedlist.leftrightShift(True, 100)
        self.assertEqual(str(self.shiftedlist),str(self.expected_nochange))
        self.assertEqual(len(self.shiftedlist),10)

    # Case 10 - Shift False Higher
    def test_leftrightShift10(self):
        self.shiftedlist.leftrightShift(False, 100)
        self.assertEqual(str(self.shiftedlist),str(self.expected_nochange))
        self.assertEqual(len(self.shiftedlist),10)



