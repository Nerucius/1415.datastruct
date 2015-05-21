import time
from random import randint


class Heap(object):
    """
        A Heap Data Type, implemented using Arrays.
        The elements inside this Heap are tuples with a word and an array of positions
            > Each position is a tuple with (line, pos) pairs
            > IE: ["hello", [(0,0), (2,1)...]]
        Notes: For a given index i, the left and right children are at 2i+1 and 2i+2
        Notes: For a given index i, the parent is at i/2 -1 + (i&1)
        Notes: This heap orders elements in ascending order.
            So the index[0] is the global min
    """

    def __init__(self):
        self._array = []
        self._sorted = False

    def insert(self, word, pos_tuple):
        """ Elements are left duplicated until heap_sort() is called """
        self._array += [[word, [pos_tuple]]]
        self._sorted = False

        self.up_heap(len(self._array) - 1)

    def up_heap(self, i):
        """ Recursive function that moves a node up the heap if the parent is smaller """
        # Bounds check
        if parent(i) < 0 or i == 0:
            return

        # Move up and recurse
        par = parent(i)
        if self._array[par][0] > self._array[i][0]:
            # print "moving", self._array[i][0], "up"
            self._array[par], self._array[i] = self._array[i], self._array[par]
            self.up_heap(par)

    def remove_min(self):
        """ Swaps the first and last element, then removes the last, finally fixes the Heap downwards """
        self._array[0], self._array[-1] = self._array[-1], self._array[0]
        min_val = self._array[-1]
        del self._array[-1]
        self._sorted = False

        self.down_heap()
        return min_val

    def down_heap(self, i=0):
        # Bounds check:
        arr = self._array
        max_i = len(arr) - 1
        if left(i) > max_i and right(i) > max_i:
            return

        # Readibility assigns and right node sorcery
        key = arr[i][0]
        lft = arr[left(i)][0]
        rght = "__NONE"
        if right(i) <= max_i:
            rght = arr[right(i)][0]

        # if the left child is the bigger of the two children, swap and recurse
        # print key, "left:", lft, "right:", rght
        if key > lft <= rght:
            # print "moving", arr[i][0], "down left"
            arr[i], arr[left(i)] = arr[left(i)], arr[i]
            self.down_heap(left(i))
        elif key > rght <= lft and rght is not "__NONE":
            # print "moving", arr[i][0], "down right"
            arr[i], arr[right(i)] = arr[right(i)], arr[i]
            self.down_heap(right(i))
        else:
            return

    def heap_sort(self):
        if len(self) == 0:
            return

        # First item is the root
        new_arr = [self.remove_min()]

        # From there on, keep removing the min and adding to the new list,
        # Finally point this Heap to the new sorted list, which is also a valid
        # Heap
        while len(self) > 0:
            item = self.remove_min()
            # If the words are equal, add the positions
            if new_arr[-1][0] == item[0]:
                new_arr[-1][1] += [item[1][0]]
            else:
                new_arr += [item]

        self._array = new_arr
        self._sorted = True

    def contains(self, word):
        """ Returns the node containing the word, or None if not found """
        if not self._sorted:
            print "Sorting heap before search... ",
            self.heap_sort()
            print "Done sorting."
        return self.bin_search(word)

    def bin_search(self, word, mn=0, mx=-1):
        """ Supah-Fast binary search biatch """
        if mx == -1:
            mx = len(self) - 1

        while abs(mn-mx) > 1:
            mid = mn + (mx-mn)/2

            # If we're searching very few elements, just do a linear search gosh
            # Instead of shredding the CPU cache like a fucking psycho we take advantage
            # of data-locality
            if mx - mn < 16:
                for item in self[mn:mx]:
                    if item[0] == word:
                        return item
                return None

            if self[mid][0] == word:
                return self[mid]
            else:
                if word > self[mid][0]:
                    mn = mid
                else:
                    mx = mid
        return None

    def __getitem__(self, index):
        return self._array[index]

    def __len__(self):
        return len(self._array)

    def __str__(self):
        res = "[HEAP (%d)]:\n" % len(self)
        for item in self:
            res += "\t" + str(item) + "\n"
        return res


def parent(i):
    return (i / 2) - 1 + (i & 1)


def left(i):
    return (i * 2) + 1


def right(i):
    return (i * 2) + 2


def test():
    heap = Heap()
    n = int(1e2)

    t0 = time.clock()
    for i in range(n):
        word = chr(randint(65, 90))
        pos = (randint(0, 10), randint(0, 10))
        heap.insert(word, pos)


    print "Insert time time for %d words:" % n, (time.clock() - t0) * 1e3, "ms"

    t0 = time.clock()
    heap.heap_sort()

    print "Sort time for %d entries with %d data points:" % (len(heap), n), (time.clock() - t0) * 1e3, "ms"

    print ""
    t0 = time.clock()
    print heap.contains("Z"), "\nfound in",
    print (time.clock() - t0) * 1e3, "ms", "in a heap of size", len(heap)


if __name__ == "__main__":
    test()
