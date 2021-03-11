'''sortcl: sort multiple angular power spectra in healpy input order

author: Nicolas Tessore <n.tessore@ucl.ac.uk>
license: MIT

'''

__version__ = '2021.03.11'

__all__ = [
    'index',
    'sortcl',
]


def index(pairs):
    '''assign matrix indices to a list of pairs

    Given a list of items ``x`` with ``len(x) == 2``, return a list of indices
    ``(i, j)`` in the matrix of items.

    Parameters
    ----------
    pairs : list of pairs
        An iterable of objects of length two.

    Returns
    -------
    index : list of (int, int)
        A list of sorted indices for the matrix of items.

    Examples
    --------
    >>> import sortcl
    >>> sortcl.index(['TT', 'TE', 'TB', 'EE', 'EB', 'BB'])
    [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
    >>> sortcl.index(['TT', 'EE', 'BB', 'TE', 'EB', 'TB'])
    [(0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)]

    The function only considers sorted tuples.

    >>> sortcl.index([(0, 0), (1, 0), (1, 1)])
    [(0, 0), (0, 1), (1, 1)]

    '''

    if isinstance(pairs, int):
        return [(i, i) for i in range(pairs)]
    else:
        idict = {}
        index = []
        for i, pair in enumerate(pairs):
            if len(pair) != 2:
                raise ValueError(f'{pair} at position {i} is not a pair')
            a, b = pair
            if a not in idict:
                idict[a] = len(idict)
            if b not in idict:
                idict[b] = len(idict)
            index.append(tuple(sorted([idict[a], idict[b]])))
        return index


def sortcl(cls, pairs, new=True):
    '''sort cls in healpy synalm/synfast order

    Given a list of cls and a list of pairs, return a new list of cls in the
    order that healpy's ``synalm`` and ``synfast`` expect.

    The list of pairs is any list of objects of length 2, for example strings:
    ``['TT', 'TE', 'TB']``.

    Parameters
    ----------
    cls : list
        List of objects that will be sorted.
    pairs : list of pairs
        An iterable of objects of length two.
    new : bool
        Sort along diagonals if ``True``, or along rows if ``False``.

    Returns
    -------
    sorted_cls : list
        Sorted list of objects. Missing entries are set to ``None``.

    Examples
    --------
    The typical use case is to bring a list of input cls into the right order
    to pass it to ``synalm``.

    >>> # 5 random example cls up to lmax = 1000
    >>> cls = np.random.rand(5, 1001)
    >>> pairs = ['TT', 'TE', 'TB', 'EE', 'BB']

    >>> from sortcl import sortcl
    >>> sorted_cls = sortcl(cls, pairs)

    To illustrate what's going on, we can use the fact that the cls can be any
    object, such as the labels themselves.

    >>> sortcl(pairs, pairs)
    ['TT', 'EE', 'BB', 'TE', None, 'TB']

    >>> # can also sort in old order, along rows
    >>> sortcl(pairs, pairs, new=False)
    ['TT', 'TE', 'TB', 'EE', None, 'BB']

    '''

    if len(cls) != len(pairs):
        raise ValueError('cls and pairs have different length')

    x = index(pairs)

    n = 0
    for i, j in x:
        n = max([i, j, n])
    n += 1

    sorted_cls = []

    for i in range(n):
        for j in range(i, n):
            pos = (i, j) if new is False else (j-i, j)
            try:
                k = x.index(pos)
            except ValueError:
                sorted_cls.append(None)
            else:
                sorted_cls.append(cls[k])

    return sorted_cls