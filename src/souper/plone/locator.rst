Locating the soup
=================

In Plone soups are annotated using IAnnotations.

Locating soups is a two-step process. First we need a root context, usually the
Plone Site itself, on which we look for the path of a soup::

    >>> from zope.interface import alsoProvides
    >>> from souper.plone.interfaces import ISoupRoot
    >>> plone = layer['portal']
    >>> alsoProvides(plone, ISoupRoot)

We initialize a locator for this context::

    >>> from souper.plone.locator import StorageLocator
    >>> locator = StorageLocator(plone)

By default the path is ``/`` for any soup - means the same object as the root
object (path relative to ``ISoupRoot``)::

    >>> path = locator.path('mysoup')
    >>> path
    '/'

So traverse has to return the Plone site itself::

    >>> locator.traverse(path)
    <PloneSite at /plone>

The second step now is to get the soupdata from an annotation. An empty soup is
created at the first access::

    >>> locator.storage('mysoup')
    <souper.soup.SoupData object at 0x...>

But we never need the SoupData object itself, we want the soup. Thus theres is
a handy function available to fetch the soup::

    >>> from souper.soup import get_soup
    >>> get_soup('mysoup', plone)
    <souper.soup.Soup object at 0x...>

Now lets check if this works still if we change the location of the soup::

    >>> try:
    ...    locator.set_path('otherssoup', '/subfolder')
    ... except KeyError as e:
    ...    print(e)
    'subfolder'


So first we need the subfolder::

    >>> from plone import api
    >>> portal = api.portal.get()
    >>> name = api.content.create(container=portal, type='Folder', id='subfolder')

And now we can annotate soupdata to it::

    >>> locator.set_path('otherssoup', '/subfolder')
    >>> locator.path('otherssoup')
    '/subfolder'

    >>> get_soup('othersoup', plone)
    <souper.soup.Soup object at 0x...>

Move soup between locations
===========================

First some preparations, in order to add records we need a simple catalog::

    >>> from zope.interface import implementer
    >>> from zope.component import provideUtility
    >>> from repoze.catalog.catalog import Catalog
    >>> from repoze.catalog.indexes.field import CatalogFieldIndex
    >>> from souper.interfaces import ICatalogFactory
    >>> from souper.soup import NodeAttributeIndexer
    >>> @implementer(ICatalogFactory)
    ... class MySoupCatalogFactory(object):
    ...     def __call__(self, context):
    ...         catalog = Catalog()
    ...         indexer = NodeAttributeIndexer('name')
    ...         catalog['name'] = CatalogFieldIndex(indexer)
    ...         return catalog
    >>> provideUtility(MySoupCatalogFactory(), name="mysoup")

And add some records to ``mysoup``::

    >>> soup = get_soup('mysoup', plone)
    >>> from souper.soup import Record
    >>> record = Record()
    >>> record.attrs['name'] = 'Willi'
    >>> intid = soup.add(record)
    >>> record = Record()
    >>> record.attrs['name'] = 'Anneliese'
    >>> intid = soup.add(record)
    >>> from repoze.catalog.query import Eq
    >>> [r for r in soup.query(Eq('name', 'Willi'))]
    [<Record object 'None' at ...>]

Now lets move this to subfolder::

    >>> old_data = soup.data
    >>> locator.move('mysoup', '/subfolder')
    >>> movedsoup = get_soup('mysoup', plone)
    >>> movedsoup
    <souper.soup.Soup object at 0x...>

    >>> movedsoup.data is not old_data
    True

    >>> [r for r in movedsoup.query(Eq('name', 'Willi'))]
    [<Record object 'None' at ...>]

