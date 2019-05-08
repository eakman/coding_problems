import pdb
import weakref


class Node:

    __slots__ = ("key", "value", "_next", "_prev", "__weakref__")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self._next = None
        self._prev = None

    @property
    def next(self):
        if self._next:
            return self._next()
        return None

    @next.setter
    def next(self, node):
        if not node:
            self._next = None
        else:
            self._next = weakref.ref(node)
    @property
    def prev(self):
        if self._prev:
            return self._prev()
        return None

    @prev.setter
    def prev(self, node):
        if not node:
            self._prev = None
        else:
            self._prev = weakref.ref(node)

    def __eq__(self, other):
        try:
            return self.key == other.key
        except:
            return False

    def detach(self):
        if self.next:
            self.next.prev = self.prev
        if self.prev:
            self.prev.next = self.next
        self.next = None
        self.prev = None

    def __str__(self):
        return f"({self.key}, {self.value}) <-> {self.next}"



class LRUCache:
    def __init__(self, capacity):
        self.head = None
        self.tail = None
        self.map = {}
        self.capacity = capacity

    @property
    def count(self):
        return len(self.map)

    def set_head(self, node):
        if self.head:
            self.head.prev = node
        node.next = self.head
        self.head = node
        if not self.tail:
            self.tail = self.head

    def get(self, key):
        if key in self.map:
            node = self.map[key]
            if node == self.tail:
                self.tail = self.tail.prev
            if node == self.head:
                self.head = self.head.next
            node.detach()
            self.set_head(node)
            return self.head.value
        return -1

    def put(self, key, value):
        if not key in self.map:
            self.map[key] = Node(key, value)
        node = self.map[key]
        node.value = value

        if self.count == (self.capacity + 1):
            tail = self.tail
            self.tail = tail.prev
            tail.detach()
            del self.map[tail.key]

        if node == self.tail:
            self.tail = self.tail.prev
        if node == self.head:
            self.head = self.head.next

        node.detach()
        self.set_head(node)



if __name__ == '__main__':
    lc = LRUCache(1)
    lc.put("first", 1)
    pdb.set_trace()
