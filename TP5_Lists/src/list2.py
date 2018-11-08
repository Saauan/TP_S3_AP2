#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`list` module

:author: FIL - Faculté des Sciences et Technologies - 
         Univ. Lille <http://portail.fil.univ-lille1.fr>_

:date: 2017, september

Provides 

- a class :class:`List` for mutable lists
- an exception :class:`ListError` 


Lists are either empty, either essentially objects with two composants :

#. a *head* composant which represent the head value  of the list,
#. and a *tail* composant which is represent the tail of the list

"""


class ListError(Exception):
    """
    Exception used by methods

    * ``__init__``
    * ``head``
    * ``tail``
    * ``set_head``
    * ``set_tail``

    of class :class:`List`.
    """
    def __init__(self, msg):
        self.message = msg

class List():
    """
    :param args: 
    :type args: tuple
    :build: a new empty list if args is empty, 
            or a list whose head is first element of args, 
            and tail list is second element of args.
    :UC: len(args) in {0, 2} 
         and if len(args) == 2, args[1] must be a List
    :raise: :class:`ListError` if UC is not satisfied

    >>> list = List()
    >>> list.is_empty()
    True
    >>> list.head()
    Traceback (most recent call last):
      ...
    ListError: head: empty list
    >>> list2 = List(1, list)
    >>> list2.is_empty()
    False
    >>> list2.head()
    1
    >>> list2.tail().is_empty()
    True
    >>> print(List(2, list2))
    [2, 1]
    >>> print(list2)
    [1]
    >>> list3 = List(2, list2)
    >>> list3.set_head(0)
    >>> print(list3)
    [0, 1]
    >>> list3.set_tail(List())
    >>> print(list3)
    [0]
    """
    
    def __init__(self, *args):
        """
        :param args: 
        :type args: tuple
        :build: a new empty list if args is empty, 
                or a list whose head is first element of args, 
                and tail list is second element of args.
        :UC: len(args) in {0, 2} 
             and if len(args) == 2, is_instance(args[1], List)
        """
        if len(args) == 0:
            self.__content = dict()
        elif len(args) == 2:
            if isinstance(args[1], List):
                self.__content = {'head' : args[0],
                                  'tail' : args[1]}
            else:
                raise ListError('bad type for second argument')
        else:
            raise ListError('bad number of arguments')


    def is_empty(self):
        """
        :return:
           - True if self is empty
           - False otherwise
        :rtype: bool
        :UC: none
        """
        return len(self.__content) == 0

    def head(self):
        """
        :return: head element of self
        :raise: :class:`ListError` if self is empty
        """
        try:
            return self.__content['head']
        except KeyError:
            raise ListError('head: empty list')

    def tail(self):
        """
        :return: tail list of self
        :raise: :class:`ListError` if self is empty
        """
        try:
            return self.__content['tail']
        except KeyError:
            raise ListError('tail: empty list')



    def set_head(self, x):
        """
        :param x:
        :type x: any
        :return: None
        :side effect: replace head element of self with x.
        :UC: self must be non empty
        :raise: :class:`ListError` if self is empty
        """
        try:
            self.__content['head'] = x
        except KeyError:
            raise ListError('set_head: empty list')

    def set_tail(self, l):
        """
        :param l:
        :type l: List
        :return: None
        :side effect: replace head element of self with x.
        :UC: self must be non empty
        :raise: :class:`ListError` if self is empty or if l is not a List
        """
        if isinstance(l, List):
            try:
                self.__content['tail'] = l
            except KeyError:
                raise ListError('set_tail: empty list')
        else:
            raise ListError('set_tail: argument is not a list')
        
    def __str__(self):
        """
        :return: a string representation of list self
        :rtype: str
        :UC: none
        """
        def str_content(self, item_number=0):
            if self.is_empty():
                return ''
            elif item_number == 50:
                return ', ...'
            else:
                comma = '' if item_number == 0 else ', '
                return comma + str(self.head()) + str_content(self.tail(), item_number + 1)
            
        return '[{:s}]'.format(str_content(self))

    def __repr__(self):
        """
        :return: a string representation of list self
        :rtype: str
        :UC: none
        """
        def str_content(self, item_number=0):
            if self.is_empty():
                return ''
            elif item_number == 50:
                return ', ...'
            else:
                comma = '' if item_number == 0 else ', '
                return comma + str(self.head()) + str_content(self.tail(), item_number + 1)
            
        return '[{:s}]'.format(str_content(self))
    
    def __len__(self):
        '''
        :return: length of self
        :rtype: int
        :UC: none
        '''
        if self.is_empty():
            return 0
        else:
            return 1 + self.tail().__len__()

    def cont(self, L2):
        """
        Concatenates 2 Lists

        :param L1, L2: (List)
        :return: A concatenated List
        :returntype: List
        :UC: None
        :Example:

        >>> L1 = List(1, List(2, List(3, List())))
        >>> L2 = List(4, List(5, List(6, List())))
        >>> L3 = L1.cont(L2)
        >>> print(L3)
        [1, 2, 3, 4, 5, 6]
        """
        L1 = self
        if L2.is_empty():
            return L1
        if L1.is_empty():
            return L2
        else:
            return List(L1.head(), L1.tail().cont(L2))
    

    def __add__(self,L2):
        """
        Concatenates 2 Lists

        :Example:

        >>> L1 = List(1, List(2, List(3, List())))
        >>> L2 = List(4, List(5, List(6, List())))
        >>> L3 = L1 + L2
        >>> print(L3)
        [1, 2, 3, 4, 5, 6]
        """
        return self.cont(L2)
    
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)
