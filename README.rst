Overview
========

``souper.plone`` provides a container for persistent records which are
queryable. It is a genric storage for mass-data in an isolated container.
Light-weight records based on
`node.ext.zodb <https://github.com/bluedynamics/node.ext.zodb>`_
are stored in an ``IOBTree``. ``repoze.catalog`` in used to
index values of interest. ``souper.plone`` is based on the framework 
independent base package `souper <https://github.com/bluedynamics/souper>`_.

``souper.plone`` is no out-of-the-box package! It addresses developers
with the need to solve the problem to store tiny entities of mass-data, where
heavy weight Archetypes or Dexterity are too much effort and are to slow. I.e
if you need a queryable container for non-CMSish content, like votes, data from
a poll, orders in a webshop, measuring data, or alike.

A Soup-container can be moved to an own ZODB mount-point and may be shared
across multiple independent Plone instances.

A control-panel provides actions to rebuild, reindex and move Soups around.



Usage
=====

XXX UPDATE ME

``SoupData`` objects are stored as annotation to an object providing the
``ISoupAnnotatable`` interface.

For use inside Plone, provide ``ISoupAnnotatable`` via ``five.implements`` on
the plone site object usind ZCML::

    <five:implements
        class="Products.CMFPlone.Portal.PloneSite"
        interface="souper.plone.interfaces.ISoupAnnotatable" />

``SoupData`` is looked up by ``id`` for a given context. This context acquires
it's parent until ``ISoupAnnotatable`` is found, on which the ``SoupData`` is
annotated by ``id``. Use ``getSoup`` function for this::

    >>> from souper.plone import getSoup
    >>> soup = getSoup(context, 'my_soup_id')
    >>> soup
    <souper.plone.soup.Soup at 0x...>

If no ``SoupData`` is found for given id, a new one is created and annotated
to ``ISoupAnnotatable``.

We must provide an ``ICatalogFactory`` implementation for each soup, registered
as utility under the same ``id`` as ``SoupData`` is annotated.

Make sure that Catalog is re-created each time catalog factory gets called. this
is needed for correct record reindexing::

    >>> from zope.interface import implements
    >>> from zope.catalog.catalog import Catalog
    >>> from zope.catalog.field import FieldIndex
    >>> from souper.plone.interfaces import ICatalogFactory
    >>> from souper.plone.interfaces import INodeAttributeIndexer
    >>> class MyCatalogFactory(object):
    ...     implements(ICatalogFactory)
    ...
    ...     def __call__(self):
    ...         catalog = Catalog()
    ...         catalog[u'name'] = FieldIndex(field_name='name',
    ...                                       interface=INodeAttributeIndexer)
    ...         return catalog

ZCML::

    <utility
        name="my_soup_id"
        factory=".mymodule.MyCatalogFactory"
        provides="souper.plone.interfaces.ICatalogFactory" />

A Soup can only contain ``Records``. A Record is a simple persistent object
which accepts any keyword arguments on ``__init__`` time. This arguments are
used as Record properties.

Create a Record and add it to soup::

    >>> from souper.plone import Record
    >>> record = Record()
    >>> record['user'] = 'user1'
    >>> record_id = soup.add(record)

Check querying::

    >>> [r for r in soup.query(user=('user1', 'user1')]
    [<Record object 'None' at ...>]

    >>> [r for r in soup.query(user=2*('nonexist',))]
    []

Add some more Records::

    >>> record = Record()
    >>> record.attrs['user'] = 'user1'
    >>> record_id = soup.add(record)
    >>> record = Record()
    >>> record.attrs['user'] = 'user2'
    >>> record_id = soup.add(record)
    >>> u1records = [r for r in soup.query(user=2*('user1',))]
    >>> len(u1records)
    2

Change user attribute of one record::

    >>> u1records[0].attrs['user'] = 'user2'

The query still returns the old result. The Record must be reindexed::

    >>> len([r for r in soup.query(user=2*('user1',))])
    2

    >>> soup.reindex([u1records[0]])
    >>> len([r for r in soup.query(user=2*('user1,)')])
    1

    >>> len([r for r in soup.query(user=2*('user2,)')])
    2

You can reindex all records in soup at once::

    >>> len([r for r in soup.query(user=2*('user3',))])
    0

    >>> all = [r for r in soup.data.values()]
    >>> all = sorted(all, key=lambda x: x.attrs['user'])
    >>> len(all)
    3

    >>> all[-1].attrs['user'] = 'user3'
    >>> soup.reindex()
    >>> len([r for r in soup.query(user=2*('user3',))])
    1

You can also rebuild the catalog. In this case the catalog factory is called
again and the new catalog is used.

Add index with key name in catalog factory source::

    >>> from zope.catalog.field import FieldIndex

    >>> catalog[u'name'] = FieldIndex(field_name='name',
    ...                               interface=INodeAttributeIndexer)

Set name attribute on some record data, rebuild soup and check results::

    >>> all[0].attrs['name'] = 'name'
    >>> all[1].attrs['name'] = 'name'
    >>> all[2].attrs['name'] = 'name'
    >>> soup.rebuild()
    >>> len([r for r in soup.query(name=2*('name',))])
    3

Delete records::

    >>> del soup[all[0]]
    >>> len([r for r in soup.query(name=2*('name',))])
    2

For huge expected results we can query LazyRecords. They return the real record
on call::

    >>> lazy = [l for l in soup.lazy(name=2*('name',))]
    >>> lazy
    [<souper.plone.soup.LazyRecord object at ...>,
    <souper.plone.soup.LazyRecord object at ...>]

    >>> lazy[0]()
    <Record object 'None' at ...>


Text Index NG 3 support
=======================

This package provides a zope3 index wrapper for textindexng3. It is located at
``souper.plone.ting.TingIndex``.

You can use textindexng3 to index multiple fields of record at once, and make
complex queries to this index. See
`Products.TextIndexNG3 <http://pypi.python.org/pypi/Products.TextIndexNG3>`_
for more information.

I you want to use textindexng3 with ``souper.plone``, make sure package
``zopyx.txng3.core`` is installed and it's ZCML is loaded. ``zopyx.txng3.core``
is NO hard dependency of ``souper.plone``.

A ``TingIndex`` just expects field names as space separated string, or as
iterable. A catalog factory using ``TingIndex`` looks like this (here we do not
need the INodeAttributeIndexer!)::

    >>> class TingCatalogFactory(object):
    ...     implements(ICatalogFactory)
    ...
    ...     def __call__(self):
    ...         catalog = Catalog()
    ...         catalog[u'ting'] = TingIndex(field_name=('foo', 'bar', 'baz'))
    ...         return catalog

Register this catalog factory as utility, we use ``tingsoup`` in this
example.

Query textindexng3 using soup::

    >>> soup = getSoup(site, 'tingsoup')
    >>> soup
    <Soup at tingsoup>

Index some records::

    >>> record = Record()
    >>> record.attrs['foo'] = 'foo'
    >>> record.attrs['bar'] = 'bar'
    >>> record.attrs['baz'] = 'baz'
    >>> record_id = soup.add(record)
    
    >>> record = Record()
    >>> record.attrs['foo'] = 'foobar'
    >>> record.attrs['bar'] = 'barbaz'
    >>> record.attrs['baz'] = 'bazfoo'
    >>> record_id = soup.add(record)
    
    >>> record = Record()
    >>> record.attrs['foo'] = 'aaa'
    >>> record.attrs['bar'] = 'barrrr'
    >>> record.attrs['baz'] = 'ccc'
    >>> record_id = soup.add(record)

and query them::

    >>> query = {
    ...     'query': u'bar::and(bar*)',
    ...     'search_all_fields': True,
    ... }
    >>> [r.bar for r in soup.query(ting=query)]
    ['bar', 'barbaz', 'barrrr']

History and design decisions
============================

First we thought it's a good idea to persist the soup data in persistent local
components. That was quite a mistake, at least in Plone context, because
GenericSetup purges local components when applying base profiles - what you're
normally not doing, but experience shows that shit happens ;). So we changed
the storage location to annotations on an acquireable, ``ISoupAnnotatable``
providing context.

Further the soup API was designed as utility, which was basically a good idea,
but caused troubles when looking up ``SoupData`` after the storage location
changed.  We used ``getSiteManager`` to access the Acquisition context, and
encountered inconsistencies for accessing the Acquisition context from different
site managers in Plone.
This problem forced us more or less to abandon the utility pattern, the
soup object itself now acts as adapter for context and is looked up via
``getSoup`` instead of a utility lookup.

    >>> from souper.plone import getSoup
    >>> soup = getSoup(context, 'mysoup')

In earlier days and before version 3 of this package was named
``cornerstone.soup``. There will be no upgrade path to ``souper.plone```.
If you used it in past keep on using the 2.x releases. It works fine and will
be supported for some time.

Source Code and Contributions
=============================

If you want to help with the development (improvement, update, bug-fixing, ...)
of ``souper.plone`` this is a great idea!

The code is located in the
`github collective <https://github.com/collective/souper.plone>`_.

You can clone it or `get access to the github-collective
<http://collective.github.com/>`_ and work directly on the project.

Maintainers are Jens Klein, Robert Niederreiter and the BlueDynamics Alliance
developer team. We appreciate any contribution and if a release is needed
to be done on pypi, please just contact one of us
`dev@bluedynamics dot com <mailto:dev@bluedynamics.com>`_


Contributors
============

  * Robert Niederreiter <rnix@squarewave.at>
  * Jens Klein <jens@bluedynamics.com>
  * Sven Plage
