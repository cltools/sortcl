# author: Nicolas Tessore <n.tessore@ucl.ac.uk>
# license: MIT
'''

Sort angular power spectra (:mod:`sortcl`)
==========================================

.. currentmodule:: sortcl

This is a minimal Python package to sort input angular power spectra into the
order expected by healpy's :func:`~healpy.sphtfunc.synalm` and
:func:`~healpy.sphtfunc.synfast` functions.

The package can be installed using pip::

    pip install sortcl

Then import the :func:`~sortcl.sortcl` function from the package::

    from sortcl import sortcl

Current functionality covers the absolutely minimal use case.  Please open an
issue on GitHub if you would like to see anything added.


Reference/API
-------------

.. autosummary::
   :toctree: api
   :nosignatures:

   sortcl
   index
   cl_indices

'''

__version__ = '2021.10.11'

__all__ = [
    'index',
    'sortcl',
    'cl_indices',
    'enumerate_cls',
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


def cl_indices(n, new=True):
    '''return array indices in healpy synalm/synfast order

    '''
    ii, jj = [], []
    for i in range(n):
        for j in range(i, n):
            ii.append(i if new is False else j-i)
            jj.append(j)
    return ii, jj


def enumerate_cls(cls, new=True):
    '''enumerate an array of cls

    Returns tuples ``i, j, cl`` where ``i, j`` are array indices and ``cl`` is
    the associated cl at that position.

    '''
    n = int((2*len(cls))**0.5)
    if len(cls) != n*(n+1)//2:
        raise TypeError('length of cls array is not a triangle number')
    return zip(*cl_indices(n), cls)


def sortcl(cls, pairs, new=True):
    '''sort cls in healpy synalm/synfast order

    Given a list of cls and a list of pairs, return a new list of cls in the
    order that healpy's :func:`~healpy.sphtfunc.synalm` and
    :func:`~healpy.sphtfunc.synfast` expect.

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

    for pos in zip(*cl_indices(n, new)):
        try:
            k = x.index(pos)
        except ValueError:
            sorted_cls.append(None)
        else:
            sorted_cls.append(cls[k])

    return sorted_cls
