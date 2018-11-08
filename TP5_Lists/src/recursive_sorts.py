#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`recursive_sorts` module

:author: Tristan Coignion, Ajwad Tayebi, Logan Becquembois

:date: 2018, November

Provides recursive sorts for the list2 module, namely:

- two recursives sorts ``mergesort`` and ``quicksort``
- functions to convert from list to List ``native2list`` and ``list2native``

"""

from list2 import List, ListError
from copy import copy

def compare(a, b):
    """
    Compares a and b 
    If a > b, returns 1
    If a = b, returns 0
    If a < b, returns -1

    :param a, b: (object which supports "<", ">" and "=" and of the same type) the two objects we want to compare
    :return: the result of the comparison
    :returntype: int
    :UC: a and b are of the same type and support comparison
    :Examples:

    >>> compare(5,3)
    1
    >>> compare("a", "c")
    -1
    >>> compare([1,2,3], [2,3,4])
    -1
    >>> compare(42,42)
    0
    """
    assert type(a) == type(b), "a and b must be of the same type !"
    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0

def compare_reverse(a, b):
    """
    Compares a and b 
    If a > b, returns -1
    If a = b, returns 0
    If a < b, returns 1

    :param a, b: (object which supports "<", ">" and "=" and of the same type) the two objects we want to compare
    :return: the result of the comparison
    :returntype: int
    :UC: a and b are of the same type and support comparison
    :Examples:

    >>> compare_reverse(5,3)
    -1
    >>> compare_reverse("a", "c")
    1
    >>> compare_reverse([1,2,3], [2,3,4])
    1
    >>> compare_reverse(42,42)
    0
    """
    assert type(a) == type(b), "a and b must be of the same type !"
    if a < b:
        return 1
    elif a > b:
        return -1
    else:
        return 0

def native2list(l):
    """
    Converts a native list to our List

    :param l: (list) a list
    :return: the converted list
    :returntype: (List)
    :UC: None
    :Examples:

    >>> l = [1,2,3]
    >>> L = native2list(l)
    >>> isinstance(L, List)
    True
    >>> L.head() == 1 and L.tail().head() == 2 and L.tail().tail().head() == 3
    True
    >>> l = [1,[2,3,4],5]
    >>> L = native2list(l)
    >>> isinstance(L.tail().head(), List)
    True
    """
    assert type(l) == list, "The argument l is not a list"
    if l == []:
        return List()
    elif type(l[0]) == list:
        return List(native2list(l[0]), native2list(l[1:]))
    else:
        return List(l[0], native2list(l[1:]))

def list2native(L):
    """
    Converts a list of our type to a native list

    :param L: (List) a List
    :return: the converted List
    :returntype: list
    :UC: None
    :Examples:

    >>> L = List(1,List(2,List(3,List())))
    >>> l = list2native(L)
    >>> isinstance(l, list)
    True
    >>> l
    [1, 2, 3]

    >>> L = List(1, List(List(2, List(3, List())), List(4, List())))
    >>> l = list2native(L)
    >>> l
    [1, [2, 3], 4]
    """
    assert isinstance(L, List), "The argument L is not a List"
    if L.is_empty():
        return []
    elif isinstance(L.head(), List):
        return [list2native(L.head())] + list2native(L.tail())
    else:
        return [L.head()] + list2native(L.tail())

def is_sorted(L, comp=compare):
    """
    Predicates wether a list is sorted or not according
    to the order passed as a paramater using the comparison
    function of values -1, 0, or 1

    :param l: (list) the list we want to check
    :param comp: (function) [DEFAULT=compare] the comparison function
    :return: True if the List is sorted, False otherwise
    :returntype: Bool
    :UC: None
    :Example:

    >>> L1 = native2list([1,2,3,4,5])
    >>> L2 = native2list([5,4,3,2,1])
    >>> L3 = native2list([1,5,4,3,2])
    >>> is_sorted(L1, comp=compare)
    True
    >>> is_sorted(L3, comp=compare)
    False
    >>> is_sorted(L2, comp=compare_reverse)
    True
    >>> is_sorted(L3, comp=compare_reverse)
    False
    """
    while not L.tail().is_empty():
        if comp(L.head(), L.tail().head()) == 1:
            return False
        L = L.tail()
    return True

def split(L):
    """
    return a couple (L1, L2) of lists

    :param L:
    :type L: List
    :return: a couple of two Lists of equal length
    :rtype: tuple
    :UC: none
    :Examples:

    >>> L = native2list([3, 1, 4, 1, 5, 9, 2])
    >>> L1, L2 = split(L)
    >>> L3 = L1 + L2
    >>> len(L3) == len(L)
    True
    >>> print(L3)
    [3, 4, 5, 2, 1, 1, 9]
    """
    assert isinstance(L, List), "L is not a List !"
    n = len(L)
    if n == 0:
        return (List(), List())
    elif n == 1:
        return (L, List())
    else:
        L1, L2 = split(L.tail().tail())
        return (List(L.head(), List()) + L1, List(L.tail().head(), List()) + L2)

def merge(L1, L2, comp=compare):
    """
    return a List containing all elements de L1 and L2.
    If L1 and L2 are sorted, so is the returned List.

    :param L1:
    :type L1: List
    :param L2:
    :type L2: List
    :param comp: (optional) comparison function (default value is compare)
    :return: a merged list from L1 and L2
    :rtype: List
    :UC: elements of L1 and L2 are comparable
    :Examples:

    >>> L1, L2 = native2list([1,3,4,9]), native2list([1,2,5])
    >>> print(merge(L1, L2))
    [1, 1, 2, 3, 4, 5, 9]
    """
    assert isinstance(L1, List) and isinstance(L2, List), "L1 and L2 are not Lists !"
    if L1.is_empty():
        return copy(L2)
    elif L2.is_empty():
        return copy(L1)
    else:
        cmp = comp(L1.head(), L2.head())
        if cmp <= 0:
            return List(L1.head(), List()) + merge(L1.tail(), L2, comp=comp)
        else:
            return List(L2.head(), List()) + merge(L1, L2.tail(), comp=comp)

def mergesort(L, comp=compare):
    """
    return a new list containing elements of L sorted by ascending order.

    :param L: a List to sort
    :type L: List
    :param comp: (optional) comparison function (default value is compare)
    :return: a new List containing elements of L in ascending order
    :rtype: List
    :UC: elements of L are comparable
    :Examples:

    >>> print(mergesort(native2list([3, 1, 4, 1, 5, 9, 2])))
    [1, 1, 2, 3, 4, 5, 9]
    >>> import random
    >>> n = random.randrange(20)
    >>> L = native2list([random.randrange(20) for k in range(n)])
    >>> L1 = mergesort(L)
    >>> len(L1) == len(L)
    True
    >>> is_sorted(L1)
    True
    """
    n = len(L)
    if n <= 1:
        return copy(L)
    else:
        L1, L2 = split(L)
        L1s = mergesort(L1, comp=comp)
        L2s = mergesort(L2, comp=comp)
        return merge(L1s, L2s, comp=comp)

def partition(x, L, comp=compare):
    """
    return a couple (L1,L2) of lists with elements of L1 <= x
    and elements of L2 > x.

    :param x: a pivot
    :param L:
    :type L: List
    :param comp: (optional) comparison function (default value is compare)
    :return: a couple of two lists with elements of L1 <= x
             and elements of L2 > x
    :rtype: tuple
    :UC: x must be comparable with elements of l

    :Examples:

    >>> print(partition(3, native2list([1, 4, 1, 5, 9, 2])))
    ([1, 1, 2], [4, 5, 9])
    >>> print(partition(10, native2list([1, 4, 1, 5, 9, 2])))
    ([1, 4, 1, 5, 9, 2], [])
    >>> print(partition(3, List()))
    ([], [])
    """
    if L.is_empty():
        return (List(), List())
    else:
        L1, L2 = partition(x, L.tail(), comp=comp)
        cmp = comp(L.head(), x)
        if cmp < 1:
            return (List(L.head(), List()) + L1, L2)
        else:
            return (L1, List(L.head(), List()) + L2)

def quicksort(L, comp=compare):
    """
    return a new list containing elements of L sorted by ascending order.

    :param L: a List to sort
    :type L: List
    :param comp: (optional) comparison function (default value is compare)
    :return: a new List containing elements of L in ascending order
    :rtype: List
    :UC: elements of L are comparable
    :Examples:

    >>> quicksort(native2list([3, 1, 4, 1, 5, 9, 2]))
    [1, 1, 2, 3, 4, 5, 9]
    >>> import random
    >>> n = random.randrange(20)
    >>> L = native2list([random.randrange(20) for k in range(n)])
    >>> L1 = quicksort(L)
    >>> len(L1) == len(L)
    True
    >>> is_sorted(L1)
    True
    """
    n = len(L)
    if n <= 1:
        return copy(L)
    else:
        L1, L2 = partition(L.head(), L.tail(), comp=comp)
        L1s = quicksort(L1, comp=comp)
        L2s = quicksort(L2, comp=comp)
        return L1s + List(L.head(), List()) + L2s

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)