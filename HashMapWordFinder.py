from adt.HashMap import HashMap
import time

class HashmapWordFinder(object):

    def __init__(self):
        self.hash = HashMap()

    def append_text(self, filename):
        f = open(filename)
        line_n = 0

        for line in f:
            # line = re.sub(r'\W+', '', line)
            # print line

            # For each line, insert each separate word in the tree
            pos = 0
            for word in line.split():
                self.insert_word(word.lower(), line_n, pos)
                pos += 1
            line_n += 1

        f.close()

    def insert_word(self, word, line, pos):
        self.hash.put(word, (line, pos))

    def find_occurences(self, word):
        return self.hash.get(word)

    def view_index(self):
        print " WORD          | Positions"
        print "--------------------------------------------"
        for bucket in self.hash:
            if bucket:
                for entry in bucket:
                    print " %12s | %s" % (entry[0], entry[1])
        print "--------------------------------------------"

def main():
    HWF = HashmapWordFinder()

    t0 = time.clock()
    HWF.append_text("largeText.txt")
    t_insert = (time.clock() - t0) * 1e3

    f = open("dictionary.txt", "r")
    t0 = time.clock()
    for line in f:
        for word in line.split():
            found = HWF.find_occurences(word)
            if found:
                print "Found %s at %s" %(word, found[1])
    t_search = (time.clock() - t0) * 1e3
    f.close

    print "\nINDEX:"
    HWF.view_index()

    print "\nTimes:"
    print " Insertion: %.3fms\n Dic. Search: %.3fms" %(t_insert, t_search)
    print " HasMap size:", len(HWF.hash), "buckets at", HWF.hash.get_fillrate(), "fill rate"

if __name__ == "__main__":
    main()