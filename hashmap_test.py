import unittest

from hashmap import Hashmap


class TestHashmap(unittest.TestCase):
    def test_create(self):
        myMap = Hashmap()
        self.assertEqual(myMap.size(), 0)

    def test_get_empty(self):
        hashmap = Hashmap()
        try:
            hashmap.getIfExists((1, 1))
            self.assertTrue(False)
        except Exception:
            self.assertTrue(True)

    def test_add_one(self):
        hashmap = Hashmap()
        self.assertEqual(hashmap.size(), 0)
        ret = hashmap.add("a")
        self.assertEqual(hashmap.size(), 1)
        self.assertEqual(ret, (47, 0))

    def test_add_two(self):
        hashmap = Hashmap()
        self.assertEqual(hashmap.size(), 0)
        ret1 = hashmap.add("a")
        self.assertEqual(hashmap.size(), 1)
        ret2 = hashmap.add("b")
        self.assertEqual(hashmap.size(), 2)
        self.assertEqual(ret1, (47, 0))
        self.assertEqual(ret2, (48, 0))

    def test_add_one_and_update(self):
        hashmap = Hashmap()
        self.assertEqual(hashmap.size(), 0)
        hashmap.add("a")
        self.assertEqual(hashmap.size(), 1)
        hashmap.add("a")
        self.assertEqual(hashmap.size(), 1)

    def test_add_one_and_get(self):
        hashmap = Hashmap()
        val = hashmap.add("a")
        try:
            val = hashmap.getIfExists(val[0], val[1])
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

        self.assertEqual(val, "a")

    def test_add_two_update_first_and_get_first(self):
        hashmap = Hashmap()
        self.assertEqual(hashmap.size(), 0)
        hashmap.add("a")
        self.assertEqual(hashmap.size(), 1)
        hashmap.add("b")
        self.assertEqual(hashmap.size(), 2)
        val = hashmap.add("a")
        try:
            val = hashmap.getIfExists(val[0], val[1])
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)
        self.assertEqual(val, "a")
        print(hashmap)

if __name__ == '__main__':
    unittest.main()
