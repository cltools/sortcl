
sortcl
======

**sort multiple angular power spectra in healpy input order**

This is a minimal Python package to sort input angular power spectra `cls`
into the order expected by healpy's `synalm` and `synfast` functions.

The package can be installed using pip:

    pip install sortcl

Then import the `sortcl` function from the package:

    from sortcl import sortcl

Current functionality covers the absolutely minimal use case.  Please open an
issue on GitHub if you would like to see anything added.


Documentation
=============

```py
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
```
