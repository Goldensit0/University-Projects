# -*- coding: utf-8 -*-
"""
Test program comparing solutions with the builtin list-based one.

@author: EDA Team
"""

# Classes provided by EDA Team
from phase2 import BST2
from bst import BinarySearchTree
import phase2
import unittest



class Test(unittest.TestCase):
    def setUp(self):
        # First tree for the both functions
        self.first_tree = BST2()
        for e in [14,11,18,10,13,16,19,5,12,15,17,30,4,6,29,31,2,8,24,33,1,3,7,9,23,25,32,34,21,27,36,20,22,26,28,35,37]:
            self.first_tree.insert(e)
        # Second tree for the second function
        # Also, I redid the first tree in order for the tree to be a bst object (not a BST2)
        self.first_tree_bst = BinarySearchTree()
        for e in [14,11,18,10,13,16,19,5,12,15,17,30,4,6,29,31,2,8,24,33,1,3,7,9,23,25,32,34,21,27,36,20,22,26,28,35,37]:
            self.first_tree_bst.insert(e)
        self.second_tree = BinarySearchTree()
        # removed several nodes and added 66,47,92,101 in order for a more differentiable result
        for e in [13,16,19,5,12,31,2,8,24,33,1,3,7,21,27,36,20,22,26,28,66,47,92,101]:
            self.second_tree.insert(e)


    # All tests for the first function contain "sort" in order to return the elements ordered. The elements are the same,
    # but the algorithm starts reading from the node we count the distance to downwards.
    def test_1st_1(self):
        lista_de_nodos = self.first_tree.find_dist_k(30,0)
        self.assertEqual([30], lista_de_nodos)
        self.assertEqual(1, len(self.first_tree.find_dist_k(30,0)))
    def test_1st_2(self):
        lista_de_nodos = self.first_tree.find_dist_k(30,2)
        self.assertEqual([24,33,18], lista_de_nodos)
        self.assertEqual(3, len(self.first_tree.find_dist_k(30,2)))
    def test_1st_3(self):
        lista_de_nodos = self.first_tree.find_dist_k(12,6)
        self.assertEqual([2,8,15,17,30], lista_de_nodos)
        self.assertEqual(5, len(self.first_tree.find_dist_k(12,6)))
    def test_1st_4(self):
        lista_de_nodos = self.first_tree.find_dist_k(17,7)
        self.assertEqual([23 , 25 , 32 , 34, 4 , 6], lista_de_nodos)
        self.assertEqual(6, len(self.first_tree.find_dist_k(17,7)))
    def test_1st_5(self):
        lista_de_nodos = self.first_tree.find_dist_k(26,9)
        self.assertEqual([36,15,17,11], lista_de_nodos)
        self.assertEqual(4, len(self.first_tree.find_dist_k(26,9)))

    def test_2nd_merge(self):
        # Union of the two trees
        merge = BinarySearchTree()
        for e in [14,11,18,10,13,16,19,5,12,15,17,30,4,6,29,31,2,8,24,33,1,3,7,9,23,25,32,34,21,27,36,20,22,26,28,35,37,
                  66,47,92,101]:
            merge.insert(e)
        self.assertEqual(merge, phase2.create_tree(self.first_tree_bst,self.second_tree,"merge"))
    def test_2nd_intersection(self):
        # Intersection of the two trees
        intersection = BinarySearchTree()
        for e in [5,2,1,3,8,7,13,12,16,19,24,21,20,22,27,26,28,31,33,36]:
            intersection.insert(e)
        self.assertEqual(intersection, phase2.create_tree(self.first_tree_bst,self.second_tree,"intersection"))

    def test_2nd_difference(self):
        # Difference of the two trees
        difference = BinarySearchTree()
        for e in [14,11,18,10,15,30,4,17,29,32,6,9,23,34,25,35,37,66,47,92,101]:
            difference.insert(e)
        self.assertEqual(difference, phase2.create_tree(self.first_tree_bst, self.second_tree, "difference"))


# Some usage examples
if __name__ == '__main__':
    unittest.main()
