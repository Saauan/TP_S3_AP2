#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`list` module

:author: FIL - Faculté des Sciences et Technologies - 
         Univ. Lille <http://portail.fil.univ-lille1.fr>_

:date: 2017, september

Provides 

- a class :class:`List` for non mutable lists
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
    >>> len(List(1, List(2, List(3, List()))))
    3
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
                return (comma + str(self.head()) +
                        str_content(self.tail(), item_number + 1))
                
            
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
    
    
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)
