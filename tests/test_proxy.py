import unittest
from jnius import autoclass, java_method, PythonJavaClass, cast

class TestImplemIterator(PythonJavaClass):
    __javainterfaces__ = [
        #'java/util/Iterator',
        'java/util/ListIterator', ]

    def __init__(self, collection, index=0):
        super(TestImplemIterator, self).__init__()
        self.collection = collection
        self.index = index

    @java_method('()Z')
    def hasNext(self):
        return self.index < len(self.collection.data)

    @java_method('()Ljava/lang/Object;')
    def next(self):
        obj = self.collection.data[self.index]
        self.index += 1
        return obj

    @java_method('()Z')
    def hasPrevious(self):
        return self.index >= 0

    @java_method('()Ljava/lang/Object;')
    def previous(self):
        self.index -= 1
        obj = self.collection.data[self.index]
        return obj

    @java_method('()I')
    def previousIndex(self):
        return self.index - 1

    @java_method('()Ljava/lang/String;')
    def toString(self):
        return repr(self)

    @java_method('(I)Ljava/lang/Object;')
    def get(self, index):
        return self.collection.data[index - 1]

    @java_method('(Ljava/lang/Object;)V')
    def set(self, obj):
        self.collection.data[self.index - 1] = obj


class TestImplem(PythonJavaClass):
    __javainterfaces__ = ['java/util/List']

    def __init__(self, *args):
        super(TestImplem, self).__init__(*args)
        self.data = list(args)

    @java_method('()Ljava/util/Iterator;')
    def iterator(self):
        it = TestImplemIterator(self)
        return it

    @java_method('()Ljava/lang/String;')
    def toString(self):
        return repr(self)

    @java_method('()I')
    def size(self):
        return len(self.data)

    @java_method('(I)Ljava/lang/Object;')
    def get(self, index):
        return self.data[index]

    @java_method('(ILjava/lang/Object;)Ljava/lang/Object;')
    def set(self, index, obj):
        old_object = self.data[index]
        self.data[index] = obj
        return old_object

    @java_method('()[Ljava/lang/Object;')
    def toArray(self):
        return self.data

    @java_method('()Ljava/util/ListIterator;')
    def listIterator(self):
        it = TestImplemIterator(self)
        return it

    @java_method('(I)Ljava/util/ListIterator;',
                         name='ListIterator')
    def listIteratorI(self, index):
        it = TestImplemIterator(self, index)
        return it

class ProxyTest(unittest.TestCase):
    def test_proxy(self):
        collection = range(10)
        a = TestImplem(*collection)

        out = []
        iterator = a.listIterator()
        while iterator.hasNext():
            out.append(iterator.next())
        self.assertEqual(out, collection)

        Collections = autoclass('java.util.Collections')
        self.assertEqual(max(collection), Collections.max(a))

        Collections.reverse(a)
        collection.reverse()

        a2 = cast('java/util/Collection', a.j_self)

        self.assertEqual(collection, a2.toArray())
