class Hashmap:
    def __init__(self):
        self._size = 0
        self._capacity = 50
        self._elems = [list() for _ in range(self._capacity)]

    def _hash(self, m):
        return sum(map(ord, m)) % self._capacity

    def size(self) -> int:
        return self._size

    def getIfExists(self, hsh, pos_in_list):
        return self._elems[hsh][pos_in_list]

    def add(self, key):
        hashval = self._hash(key)
        linkList = self._elems[hashval]
        for i in range(len(linkList)):
            if linkList[i] == key:
                return hashval, i
        linkList.append(key)
        self._size += 1
        return hashval, len(linkList) - 1

    def __str__(self):

        def linkList_to_string(lst):
            return "[" + ",".join(map(lambda node: str(node), lst)) + "]"

        return "\n".join(map(linkList_to_string, self._elems))
