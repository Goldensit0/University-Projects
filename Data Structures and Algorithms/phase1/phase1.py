from slistH import SList
from slistH import SNode

import sys

class SList2(SList):


    def delLargestSeq(self: SList):
        """
        This function travels throught the list once, using a two counters to find the largest sequences and
        some pointers to save the cut and paste nodes that will be use at the end. Pre_start saves the node previous
        to the start of the actual sequence so, in case it results being the new largest, the cut can be set again.
        The main pointer is actual_node, that follows the position in the list we are looking at.
        """
        if self.isEmpty():
            return
        highest_count = 1
        actual_count = 1
        cut = None
        paste = None
        pre_start = None
        actual_node = self._head

        # Travelling the list and finding the largest sequence
        for i in range(len(self)):
            if actual_node.next:
                if actual_node.elem == actual_node.next.elem:
                    actual_count += 1
                else:
                    if actual_count >= highest_count:
                        highest_count = actual_count
                        paste = actual_node.next
                        cut = pre_start
                    actual_count = 1
                    pre_start = actual_node
                actual_node = actual_node.next
            else:
                if actual_count >= highest_count:
                    highest_count = actual_count
                    paste = actual_node.next
                    cut = pre_start

        # Cutting the list at its largest sequence
        if cut:
            cut.next = paste
            self._size -= highest_count
        else:
            self._head = paste
            self._size -= highest_count

    def fix_loop(self):
        """
        This function will use two pointers moving at different velocities, starting from the head. If they meet
        again, it will mean a loop has been found.
        """
        fast = self._head
        slow = self._head
        check = True

        while fast.next and fast.next.next and fast != slow or check:
            check = False
            fast = fast.next.next
            slow = slow.next

        if not fast.next or not fast.next.next:
            return False


        loopnode = fast
        length = 1
        node = loopnode.next

        # We measure the length of the loop
        while node != loopnode:
            length += 1
            node = node.next

        # We place a pointer at the [length]'th node from the head
        node = self._head
        for i in range(length):
            node = node.next

        # We move pointers A and B at the same speed until they meet at the start of the loop
        A = self._head
        B = node

        while A != B:
            A = A.next
            B = B.next

        # Count until the end of the loop
        for i in range(length-1):
            A = A.next

        # Fix the loop
        A.next = None

        # Return True
        return True




    def create_loop(self, position):
        # this method is used to force a loop in a singly linked list
        if position < 0 or position > len(self) - 1:
            raise ValueError(f"Position out of range [{0} - {len(self) - 1}]")

        current = self._head
        i = 0

        # We reach position to save the reference
        while current and i < position:
            current = current.next
            i += 1

        # We reach to tail node and set the loop
        start_node = current
        print(f"Creating a loop starting from {start_node.elem}")
        while current.next:
            current = current.next        
        current.next = start_node


    def leftrightShift(self, left: bool, n: int):
        """
        This function shift n elements of the list, counting from the left or from the right.

        Four variables are needed: one to control the node that will have to point to None, another to control
        the node that will control the first node that we shift, another to control the last node shifted and
        one last variable to control the node that follows the last shifted node.

        Since shifting from left or right are different processes, the variables will also have different names
        in order to reach a better understanding.
        """

        # We will use a conditional to control that the n is a natural number and is not greater than the length.
        if len(self) > n >= 1:

            # Shifting from the left side
            if left:
                newheadnode = self._head
                lastnode = self._head
                shiftednode = self._head
                lastshiftednode = self._head
                for i in range(len(self) - 1):
                    if i < n:
                        newheadnode = newheadnode.next
                    if i < (n - 1):
                        lastshiftednode = lastshiftednode.next
                    lastnode = lastnode.next
                # Reassemble the list
                self._head = newheadnode
                lastnode.next = shiftednode
                lastshiftednode.next = None

            # Shifting from the right side
            else:
                tobelinked = self._head
                shiftednode = self._head
                lastshiftednode = self._head
                tobecut = self._head
                for i in range(len(self) - 1):
                    if i + 1 <= len(self) - n:
                        shiftednode = shiftednode.next
                    if i + 1 <= len(self):
                        lastshiftednode = lastshiftednode.next
                    if i + 1 > n:
                        tobecut = tobecut.next
                # Reassemble the list
                self._head = shiftednode
                lastshiftednode.next = tobelinked
                tobecut.next = None








if __name__=='__main__':

    l=SList2()
    print("list:",str(l))
    print("len:",len(l))

    for i in range(7):
        l.addLast(i+1)

    print(l)
    print()

    l=SList2()
    print("list:",str(l))
    print("len:",len(l))

    for i in range(7):
        l.addLast(i+1)

    print(l)
    print()

    # No loop yet, no changes applied
    l.fix_loop()
    print("No loop yet, no changes applied")
    print(l)
    print()

    # We force a loop
    l.create_loop(position=6)
    l.fix_loop()
    print("Loop fixed, changes applied")
    print(l)
    print()
    print()

    
    l = SList2()
    for i in [1,2,3,4,5]:        
        l.addLast(i)
    print(l.delLargestSeq())


    l=SList2()
    for i in range(7):
         l.addLast(i+1)

    print(l)
    l.leftrightShift(False, 2)
    print(l)
    
    