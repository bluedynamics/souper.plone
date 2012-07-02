z3 txng wrapper
===============

txng defaults
-------------

::

    >>> from souper.plone.ting import defaults
    >>> defaults['use_stemmer']
    False

    >>> defaults['dedicated_storage']
    True

    >>> defaults['ranking']
    False

    >>> defaults['use_normalizer']
    False

    >>> defaults['languages']
    'en'

    >>> defaults['use_stopwords']
    False

    >>> defaults['autoexpand_limit']
    4

    >>> defaults['splitter']
    'txng.splitters.simple'

    >>> defaults['index_unknown_languages']
    True

    >>> defaults['query_parser']
    'txng.parsers.en'

    >>> defaults['lexicon']
    'txng.lexicons.default'

    >>> defaults['splitter_add_chars']
    '_-'

    >>> defaults['storage']
    'txng.storages.default'

    >>> defaults['splitter_casefolding']
    True

Create normal FieldIndex
------------------------

::

    >>> from souper.plone.interfaces import INodeAttributeIndexer
    >>> from zope.catalog.field import FieldIndex
    >>> f_index = FieldIndex('foo', interface=INodeAttributeIndexer)

Create TingIndex
----------------

::
    
    >>> from souper.plone.ting import TingIndex
    >>> t_index = TingIndex('foo')
    >>> t_index._fields
    ['foo']

    >>> t_index._index.fields
    ['foo']

    >>> t_index.dedicated_storage
    False

    >>> t_index.default_fields
    ['foo']

Create Record to index
----------------------

::

    >>> from souper.plone import Record
    >>> rec = Record()
    >>> rec.attrs['foo'] = 'foo'
    >>> rec1 = Record()
    >>> rec1.attrs['foo'] = 'foobar'

Index Records
-------------

in ordinary FieldIndex::

    >>> f_index.index_doc(12345, rec)
    >>> f_index.index_doc(12346, rec1)

...and in TingIndex::

    >>> t_index.index_doc(12345, rec)
    >>> t_index.index_doc(12346, rec1)

Query Indices
-------------

in ordinary FieldIndex::

    >>> f_index.apply(2*(u'foo',))
    IFSet([12345])

    >>> f_index.apply(2*(u'foobar',))
    IFSet([12346])

...and in TingIndex::

    >>> t_index.apply(u'foo')
    IFSet([12345])

    >>> t_index.apply(u'foobar')
    IFSet([12346])

    >>> t_index.apply(u'foo*')
    IFSet([12345, 12346])

Create multi field indexing TingIndex
-------------------------------------

field names could be either a space separated string representing the list of
fields or a list or tuple with field names::

    >>> from souper.plone.ting import TingIndex
    >>> t_index = TingIndex('foo bar baz', field_callable=False)
    >>> t_index._fields
    ['foo', 'bar', 'baz']

    >>> t_index = TingIndex(['foo', 'bar', 'baz'], field_callable=False)
    >>> t_index._fields
    ['foo', 'bar', 'baz']

    >>> t_index._index.fields
    ['foo', 'bar', 'baz']

    >>> t_index.dedicated_storage
    True

    >>> t_index.default_fields
    ['foo']

Index multiple fields of records::

    >>> rec = Record()
    >>> rec.attrs['foo'] = u'foo'
    >>> rec.attrs['bar'] = u'bar'
    >>> rec.attrs['baz'] = u'baz'
    >>> t_index.index_doc(12345, rec)

    >>> rec1 = Record()
    >>> rec1.attrs['foo'] = u'foobar'
    >>> rec1.attrs['bar'] = u'barbaz'
    >>> rec1.attrs['baz'] = u'bazfoo'
    >>> t_index.index_doc(12346, rec1)

    >>> t_index.apply(u'foo::and(foo)')
    IFSet([12345])

    >>> t_index.apply({'query': u'bar::and(bar)', 'search_all_fields': True})
    IFSet([12345])

    >>> t_index.apply(u'foo::and(fo*)')
    IFSet([12345, 12346])

    >>> t_index.apply(u'foo::and(foo*)')
    IFSet([12345, 12346])

    >>> query = {
    ...     'query': u'foo::and(foo) OR bar::and(barbaz)',
    ...     'search_all_fields': True,
    ... }
    >>> t_index.apply(query)
    IFSet([12345, 12346])

    >>> query = {
    ...     'query': u'bar::and(bar*)',
    ...     'search_all_fields': True,
    ... }
    >>> t_index.apply(query)
    IFSet([12345, 12346])

Set index to catalog and search through catalog.
:: 

    >>> from zope.catalog.catalog import Catalog
    >>> catalog = Catalog()
    >>> catalog['ting'] = t_index
    
    >>> catalog.apply({'ting': query})
    IFSet([12345, 12346])

Add another record through catalog
----------------------------------

::

    >>> rec = Record()
    >>> rec.attrs['foo'] = u'aaa'
    >>> rec.attrs['bar'] = u'barrrr'
    >>> rec.attrs['baz'] = u'ccc'
    >>> catalog.index_doc(12347, rec)

    >>> catalog.apply({'ting': query})
    IFSet([12345, 12346, 12347])

    >>> query['query'] = u'foo::and(foo) OR bar::and(barrrr)'
    >>> catalog.apply({'ting': query})
    IFSet([12345, 12347])