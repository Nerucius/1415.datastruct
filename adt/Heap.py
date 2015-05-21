class Heap(object):
    """
        A Heap Data Type, implemented using Arrays.
        The elements inside this Heap are tuples with a word and an array of positions
            > Each position is a tuple with (line, pos) pairs
            > IE: ["hello", [(0,0), (2,1)...]]
        Notes: For a given index i, the left and right children are at 2i+1 and 2i+2
        Notes: For a given index i, the parent is at i/2 -1 + i&1
        Notes: This heap orders elements in ascending order.
            So the index[0] is the global min
    """

    def __init__(self):
        self._array = []

    def insert(self, word, pos_tuple):
        """ Elements are left duplicated until heap_sort() is called """
        self._array += [(word, [pos_tuple])]

    def up_heap(self, i):
        """ Recursive function that moves a node up the heap if the parent is smaller """
        if i == 0:
            return
        par = parent(i)
        if self._array[par][0] < self._array[i][0]:
            self._array[par], self._array[i] = self._array[i], self._array[par]
            self.up_heap(par)

    def remove_min(self):
        """ Swaps the first and last element, then removes the last, finally fixes the Heap downwards """
        self._array[0], self._array[-1] = self._array[-1], self._array[0]
        del self._array[-1]
        self.down_heap()

    def down_heap(self, i=0):
        # Bounds check:
        if i == len(self._array)-1 or ():
            return

        arr = self._array
        # if the left child is the bigger of the two children, swap and recurse
        if arr[i][0] > arr[left(i)][0] and arr[left(i)][0] < arr[right(i)][0]:
            arr[i], arr[left(i)] = arr[left(i)], arr[i]
            self.down_heap(left(i))
        elif arr[i][0] > arr[right(i)][0] and arr[right(i)][0] < arr[left(i)][0]:
            arr[i], arr[right(i)] = arr[right(i)], arr[i]
            self.down_heap(right(i))
        else:
            return

    def heap_sort(self):
        pass


def parent(i):
    return i / 2 - 1 + i & 1

def left(i):
    return i*2 + 1

def right(i):
    return i * 2 + 2

def word(node):
    return node[0]

def test():
    heap = Heap()

    heap.insert("Hello", (0, 1))
    heap.insert("Alpha", (0, 2))

    print word(array[0])

if __name__ == "__main__":
    test()
