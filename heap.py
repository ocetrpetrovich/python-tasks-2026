from collections.abc import Callable, Iterator, Iterable
from typing import Protocol, Self


class SupportsLessOrEqual(Protocol):
    """Типы, которые можно сравнивать при помощи <=."""
    def __le__(self, other: Self, /) -> bool: ...


class Heap[T]:
    """Класс реализующий кучу в Python.

    key (_key) - функция-ключ, по которому сравниваются элементы.
    Аналогично key из sorted. Вычисляется только при push.

    reverse (_reverse) - флаг для обозначения обратного порядка.
    Аналогично reverse из sorted.

    _storage - список хранящий элементы, их ключи и id
    (то есть [..., (key, id, value), ...]).

    id элемента - "номер" элемента. Показывает на каком по-счёту push
    (в том числе через extend) элемент попал в кучу.
    Нужен для стабильности (порядок вставки равен порядку удаления).
    """
    def __init__(
            self,
            items: Iterable[T] = (),
            /,
            *,
            key: Callable[[T], SupportsLessOrEqual] = lambda item: item,
            reverse: bool = False
    ):
        """Заполняет кучу элементами из items через heapify."""
        self._storage: list[tuple[SupportsLessOrEqual, int, T]] = []  # [..., (key, id, value), ...]
        self._key: Callable[[T], SupportsLessOrEqual] = key
        self._reverse: bool = reverse
        self._id_counter: int = 0

        # heapify
        for item in items:
            self._storage.append((self._key(item), self._id_counter, item))
            self._id_counter += 1
        for index in range(len(self._storage) // 2 - 1, -1, -1):
            self._sift_down(index)

    def _parent(self, index: int) -> int:
        """По индексу ребёнка возращает индекс родителя.

        Для корня возращает его самого (что удобно для _sift_up).
        """
        return 0 if index == 0 else (index - 1) // 2

    def _left(self, index: int) -> int:
        """По индексу родителя возращает индекс левого ребёнка.

        Если он отсутствует, возращает самого родителя (что удобно для _sift_down).
        """
        return left if (left := index * 2 + 1) < len(self._storage) else index

    def _right(self, index: int) -> int:
        """По индексу родителя возращает индекс правого ребёнка.

        Если он отсутствует, возращает самого родителя (что удобно для _sift_down).
        """
        return right if (right := index * 2 + 2) < len(self._storage) else index

    def _less_or_equal(self, first: int, second: int, /) -> bool:
        """Проверяет выполнено ли правило кучи для элементов,
        которые стоят на индексах first и second в storage_.

        Не совсем правило кучи, потому что first и second могут быть любыми.
        """
        if first == second:
            return True
        first_key, first_id, _ = self._storage[first]
        second_key, second_id, _ = self._storage[second]
        if first_key <= second_key:
            if second_key <= first_key:
                return first_id <= second_id
            return not self._reverse
        return self._reverse

    def _swap(self, first: int, second: int, /):
        """Меняет местами элементы, которые стоят на индексах first и second в storage_."""
        self._storage[first], self._storage[second] = self._storage[second], self._storage[first]

    # heapify_up
    def _sift_up(self, index: int, /):
        """Делает sift up - проталкивает элемент по индексу index максимально наверх."""
        while not self._less_or_equal(parent := self._parent(index), index):
            self._swap(parent, index)
            index = parent

    # heapify_down
    def _sift_down(self, index: int, /):
        """Делает sift down - проталкивает элемент по индексу index максимально вниз."""
        while True:
            left = self._left(index)
            right = self._right(index)
            left_f = not self._less_or_equal(index, left)
            right_f = not self._less_or_equal(index, right)
            if not left_f and not right_f:
                break
            if left_f and right_f:
                left_f = self._less_or_equal(left, right)
            if left_f:
                self._swap(index, left)
                index = left
            else:
                self._swap(index, right)
                index = right

    def push(self, item: T, /):
        """Добавляет элемент в кучу."""
        self._storage.append((self._key(item), self._id_counter, item))
        self._id_counter += 1

        self._sift_up(len(self._storage) - 1)

    def pop(self) -> T:
        """Удаляет минимальный элемент из кучи (тот же, который возращает get).

        IndexError, если куча пуста.
        """
        if not self._storage:  # len(self._storage) == 0
            raise IndexError("pop from empty Heap")
        self._swap(0, len(self._storage) - 1)
        _, _, item = self._storage.pop()
        if self._storage:
            self._sift_down(0)
        return item

    def get(self) -> T:
        """
        Возразает минимальный элемент из кучи.

        При равных ключах возращает тот элемент, что был добавлен раньше.
        IndexError, если куча пуста.
        """
        if not self._storage:
            raise IndexError("get from empty Heap")
        return self._storage[0][2]

    def extend(self, items: Iterable[T], /):
        """Делает push по каждому элементу items."""
        for item in items:
            self.push(item)

    def clear(self):
        """Удаляет все элементы кучи. Эффективнее pop, так как не делает _sift_down."""
        self._storage.clear()

    def __len__(self) -> int:
        """Возращает кол-во элементов в куче."""
        return len(self._storage)

    def __bool__(self) -> bool:
        """True, если куча не пуста, False иначе."""
        return bool(self._storage)

    def __contains__(self, item: T) -> bool:
        """Проверяет, что элемент находится в куче."""
        return item in map(lambda s: s[2], self._storage)

    def __iter__(self) -> Iterator[T]:
        """Возращает итератор на кучу. Первый элемент минимален."""
        return map(lambda s: s[2], self._storage)

    def copy(self) -> Heap[T]:
        """Возращает копию кучи."""
        copy = Heap[T](key=self._key, reverse=self._reverse)
        copy._storage = self._storage.copy()
        copy._id_counter = self._id_counter
        return copy

    # is_valid_heap
    def _assert_is_valid_heap(self):
        """Проверяет, что правило кучи выполнено."""
        for index in range(len(self._storage)):
            assert self._less_or_equal(self._parent(index), index)


def heap_sort[T](
        items: list[T],
        /,
        *,
        key: Callable[[T], SupportsLessOrEqual] = lambda item: item,
        reverse: bool = False
):
    """Сортирует данный массив при помощи Heap.

    Занимаем O(n) доп. памяти (чтобы этого избежать, нужно изменить реализацию Heap так,
    чтобы можно было использовать данный массив для хранения кучи. Но это плохо сочетается
    с кастомным key и философией Python).
    """
    h = Heap(items, key=key, reverse=reverse)
    items.clear()
    while h:
        items.append(h.pop())


empty = Heap([])
assert len(empty) == 0
assert not empty
assert list(empty) == []
assert 1 not in empty
try:
    empty.pop()
except IndexError:
    pass
else:
    assert False
try:
    empty.get()
except IndexError:
    pass
else:
    assert False

single = Heap([7])
assert len(single) == 1 and bool(single)
assert single.get() == 7
assert 7 in single and 6 not in single
assert single.pop() == 7
assert not single and len(single) == 0

source = [5, -1, 3, 5, 0, -4, 2, 3]
heap = Heap(source)
assert len(heap) == len(source)
heap._assert_is_valid_heap()
assert [heap.pop() for _ in range(len(source))] == sorted(source)
assert not heap

heap = Heap([4, 1, 3])
assert heap.get() == 1 and len(heap) == 3
heap.push(0)
heap.push(2)
assert heap.get() == 0
heap._assert_is_valid_heap()
assert heap.pop() == 0
assert heap.get() == 1 and len(heap) == 4
heap._assert_is_valid_heap()

mixed = Heap()
for number in [6, 2, 8, 1, 5]:
    mixed.push(number)
    mixed._assert_is_valid_heap()
    assert mixed.get() == min(mixed)
for expected in [1, 2, 5, 6, 8]:
    assert mixed.pop() == expected
    mixed._assert_is_valid_heap()
assert not mixed

by_length = Heap(["ccc", "a", "bb", "d"], key=len)
assert [by_length.pop() for _ in range(4)] == ["a", "d", "bb", "ccc"]

max_heap = Heap([3, 1, 4, 1, 5], reverse=True)
max_heap._assert_is_valid_heap()
assert [max_heap.pop() for _ in range(5)] == [5, 4, 3, 1, 1]

extended = Heap([3])
extended.extend([1, 2])
assert len(extended) == 3 and 2 in extended and 4 not in extended
extended.clear()
assert not extended and len(extended) == 0

original = Heap([2, 1])
clone = original.copy()
clone.push(0)
assert clone.pop() == 0
assert original.pop() == 1 and clone.pop() == 1
assert original.pop() == 2 and clone.pop() == 2
assert not original and not clone

empty_array = []
heap_sort(empty_array)
assert empty_array == []

single_array = [42]
heap_sort(single_array)
assert single_array == [42]

array = [3, -1, 2, 3, 0, -5]
heap_sort(array)
assert array == [-5, -1, 0, 2, 3, 3]

key_array = ["ccc", "a", "bb"]
heap_sort(key_array, key=len)
assert key_array == ["a", "bb", "ccc"]

reverse_array = [1, 3, 2]
heap_sort(reverse_array, reverse=True)
assert reverse_array == [3, 2, 1]
