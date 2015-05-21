from random import randint
from time import clock

# Constants
KEY = 0
VAL = 1


class HashMap(object):
    """
        A HashMap structure for storing words and word position in entries.
        The hashmap has a main array that contains "buckets" of data:
        each bucket is itself an array of entries, one entry is as such:
            [key, [values...]]
            where key: word, values: positions
        So a bucket wil have this form:
            [ [key, [values...]]... ]
        And the main array is a list of those buckets.
        The hash function determines the bucket, and from there on, the correct place in
        the bucket must be searched manually.
    """

    def __init__(self, cap=16):
        """
            Inits a hashmap object. Default initial capacity is 16.
            :param cap: Initial size of the HashMap
        """

        self._array = [None] * cap
        self._size = cap
        self._count = 0
        self._fillrate = 0

    def put(self, key, value):
        # print self._size, "-",
        hs = self.hash(key)

        # Python sometimes fucks up tuples, wrapping them in an array
        # this fixes it
        if len(value) == 1:
            value = value[0]

        if not self._array[hs]:
            # print "new bucket:\t", hs, key, value
            self._array[hs] = [[key, [value]]]  # Create a new bucket

        else:
            for entry in self._array[hs]:  # Looking at entries inside the bucket
                if entry[KEY].lower() == key.lower():
                    # print "new value:\t", hs, key, value
                    entry[VAL] += [value]  # If the key matches, add the new value to the value array
                    return

            # If not found, add new entry in the bucket
            # print "new entry:\t", hs, key, value
            self._array[hs] += [[key, [value]]]

        self.check_fillrate()

    def get(self, key):
        if not self._array[self.hash(key)]:
            return None

        for entry in self._array[self.hash(key)]:
            if entry[KEY] == key:
                return entry

        return None

    def hash(self, key):
        """ Implementation of the DJB2 hashing algorithm. Certainly not the best hash ever but
            works good enough, and it's *FAST* """
        adr = 5381
        for c in key:
            adr = ((adr << 5) + adr) + ord(c)

        # Since our map's size is a power of 2, we can use the AND operator to trim to size
        # Which is MUUUUUCH faster than modulo
        return int(adr & (self._size - 1))

    def get_fillrate(self):
        return self._fillrate

    def check_fillrate(self):
        """ Calculates the Map fill rate, if it's over 0.8, it rehashes the table """
        filled = 0

        for bucket in self._array:
            if bucket is not None:
                filled += 1

        self._fillrate = float(filled) / self._size
        if self._fillrate > 0.8:
            # Fill rate too high, rehash
            self._rehash()

    @staticmethod
    def random_words(count):
        index = randint(0, 349899)

        f = open("../dictionary.txt")
        lines = f.readlines()
        for i in range(count):
            yield lines[index].split()[0]
            index = (index + 1) % 349900

    def get_array(self):
        return self._array

    def _rehash(self):
        """ Rehashes the entire table if the fill rate surpasses an imposed limit.
            By doing this we can guarantee a quick lookup time.
        """
        # print "Rehashing to:", self._size * 2

        self._size *= 2
        new_hash = HashMap(self._size)

        for bucket in self._array:
            if bucket:
                for entry in bucket:
                    for val in entry[VAL]:
                        # Needs to be put value per value or python freaks out
                        # Some perf is lost but whatchu' gon' do
                        new_hash.put(entry[KEY], val)

        self._array = new_hash.get_array()

    def __str__(self):
        res = "[HashMap]\n"
        i = 0
        for bucket in self._array:
            res += "%d) %s\n" % (i, bucket)
            i += 1
        return res

    def __getitem__(self, index):
        return self._array[index]

    def __len__(self):
        return self._size


def test():
    hashmap = HashMap(16)

    for word in hashmap.random_words(256):
        hashmap.put(word, (0, randint(0, 32)))

    print hashmap
    print hashmap.get_fillrate()

    for word in hashmap.random_words(100):
        found = hashmap.get(word)
        if found:
            print word, "found"

    t0 = clock()
    for word in hashmap.random_words(1000000):
        hashmap.hash(word)
    print "Hashed 1 Million words in:", (clock()-t0)*1e3,"ms"


if __name__ == "__main__":
    test()