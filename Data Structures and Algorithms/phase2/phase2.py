"""
@author: EDA Team
"""

# Classes provided by EDA Team
from bintree import BinaryNode
from bst import BinarySearchTree
from dlist import DList

# Exercise #1
class BST2(BinarySearchTree):
    def find_dist_k(self, n: int, k: int) -> list:
        # n = element of the node
        # k = distance
        # CREATE A LIST WITH THE NODES BETWEEN THE ONE WE SEARCH AND THE ROOT (route until node).
        # Execute the recursion (downwards) with all the nodes of the list and the respective distance.

        # We save the route until the node in a Dlist
        ruta = DList()
        node = self._root
        while node is not None and node.elem != n:
            ruta.add_last(node)
            if n > node.elem:
                node = node.right
            else:
                node = node.left
        lista_de_nodos = []
        self._find_dist_k(node, lista_de_nodos, k)
        for i in range(len(ruta)):
            self._find_dist_k(ruta.tail.elem, lista_de_nodos,k-1-i,node)
            node = ruta.tail.elem
            ruta.remove_last()
        return lista_de_nodos

    def _find_dist_k(self, node, lista:list, k:int, route_avoid=None):
        if node is None:
            return
        if node == route_avoid:
            return
        if k == 0:
            lista.append(node.elem)
            return
        if route_avoid is not None:
            self._find_dist_k(node.left, lista, k - 1, route_avoid)
            self._find_dist_k(node.right, lista, k - 1, route_avoid)
        else:
            self._find_dist_k(node.left, lista, k-1)
            self._find_dist_k(node.right, lista, k-1)
        return

# Exercise #2
def create_tree(input_tree1: BinarySearchTree, input_tree2: BinarySearchTree, opc: str) -> BinarySearchTree:
    # merge (Union)
    # intersection
    # difference
    """
    Since the exercise says 'returns a new tree', we have to generate an independent tree.
    """
    newtree1 = BinarySearchTree()
    if opc == "merge":
        copy(input_tree1,newtree1)
        merge(input_tree2,newtree1)
        return newtree1
    elif opc == "intersection":
        intersection(input_tree1,input_tree2,newtree1)
        return newtree1
    elif opc == "difference":
        difference(input_tree1,input_tree2,newtree1)
        difference(input_tree2,input_tree1,newtree1)
        return newtree1
    else:
        return None

def copy(copytree, pastetree):
    _copy(copytree.root, pastetree)

def _copy(copynode, pastetree):
    if copynode is None:
        return
    pastetree.insert(copynode.elem)
    _copy(copynode.left, pastetree)
    _copy(copynode.right, pastetree)

def merge(second_tree, searchin_tree):
    _merge(second_tree.root, searchin_tree)

def _merge(node, searchin):
    if node is None:
        return
    pointer = searchin.root
    # We make sure it is not None. We will also use pointer to get out of the loop
    while pointer is not None:
        # Higher value -> we go right
        if node.elem > pointer.elem:
            # Not at the end yet, there might be coincidence
            if pointer.right is not None:
                pointer = pointer.right
            # We arrive at the end with no coincidence, we add the node
            else:
                pointer.right = BinaryNode(node.elem)
                # We set the pointer to None so we can get out of the loop
                pointer = None
        # Lower value -> we go left
        elif node.elem < pointer.elem:
            # Not at the end yet, there might be coincidence
            if pointer.left is not None:
                pointer = pointer.left
            # We arrive at the end with no coincidence, we add the node
            else:
                pointer.left = BinaryNode(node.elem)
                # We set pointer to None (so we can get out of the loop)
                pointer = None
        # The value is equal -> the element is already in the tree -> we go out of the loop
        else:
            pointer = None

    # We apply the recursion to the next nodes.
    _merge(node.left, searchin)
    _merge(node.right, searchin)

def intersection(t1, t2, pastetree):
    _intersection(t1.root, t2, pastetree)

def _intersection(node, searchtree, pastetree):
    if node is None:
        return
    # Pointer will travel the searchtree
    pointer = searchtree.root
    # We make sure it is not None. We will also use pointer to get out of the loop
    while pointer is not None:
        # Higher -> right
        if node.elem > pointer.elem:
            # If the right node were None, we would get out (no coincidence found)
            pointer = pointer.right
        # Lower -> left
        elif node.elem < pointer.elem:
            # If the left node were None, we would get out (no coincidence found)
            pointer = pointer.left
        # We found a coincidence -> the element is part of the intersection
        else:
            # We add it to the pastetree
            pastetree.insert(node.elem)
            # Pointer = None so we can get out of the loop.
            pointer = None

    # We apply the recursion to the next nodes.
    _intersection(node.left, searchtree, pastetree)
    _intersection(node.right, searchtree, pastetree)

def difference(t1,t2,paste):
    _difference(t1.root,t2,paste)


def _difference(node, searchtree, pastetree):
    if node is None:
        return
    # Pointer will travel the searchtree
    if searchtree.root is None:
        return
    pointer = searchtree.root
    # Control variable
    control = True
    while control:
        # We make sure pointer is not None.
        if pointer is not None:
            # Higher -> right
            if node.elem > pointer.elem:
                pointer = pointer.right
            # Lower -> left
            elif node.elem < pointer.elem:
                pointer = pointer.left
            # We found a coincidence -> the element is part of the intersection -> the element is not on the difference
            else:
                control = False
        # The element was not found -> the element is in the difference
        else:
            pastetree.insert(node.elem)
            # Changing the control variable so we get out of the loop
            control = False


    # We apply the recursion to the next nodes.
    _difference(node.left, searchtree, pastetree)
    _difference(node.right, searchtree, pastetree)


# Some usage examples
if __name__ == '__main__':
    # input_list_01 = [5, 1, 7, 9, 23]
    # input_list_02 = [1, 9, 11]
    input_list_01 = [5, 12, 2, 1, 3, 9]
    input_list_02 = [9, 3, 21]

    # Build and draw first tree
    tree1 = BinarySearchTree()
    for x in input_list_01:
        tree1.insert(x)
    tree1.draw()

    # Build and draw second tree
    tree2 = BinarySearchTree()
    for x in input_list_02:
        tree2.insert(x)
    tree2.draw()

    function_names = ["merge", "intersection", "difference"]

    for op_name in function_names:
        res = create_tree(tree1, tree2, op_name)
        print(f"-- Result for {op_name} method. #{res.size()} nodes")
        res.draw()
