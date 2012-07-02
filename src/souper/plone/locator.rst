Locating the soup
=================

In Plone soups are annotated using IAnnotations.

Locating soups is a two-step process. First we need a root context, usally the
Plone Site itself, on which we look for the path of a soup::

    >>> from zope.interface import alsoProvides
    >>> from souper.plone.interfaces import ISoupAnnotatable    
    >>> plone = layer['portal']
    >>> alsoProvides(plone, ISoupAnnotatable)
    
We initialize a locator for this context::

    >>> from souper.plone.locator import StorageLocator 
    >>> locator = StorageLocator(plone)      

By default the path is ``/`` for any soup - means the same object as the root
object::

    >>> path = locator.path('mysoup')
    >>> path
    '/'

So traverse has to return the plone site itself::

    >>> locator.traverse(path)
    <PloneSite at /plone>

An empty soup is created at the first access::

    >>> locator.locate('mysoup')
    <souper.soup.SoupData object at 0x...>

But we never need the SoupData object itself, we want the soup. Thus theres is
a handy function available to fetch the soup::

    >>> from souper.soup import get_soup
    >>> soup = get_soup(plone, 'mysoup')
    >>> soup
    <souper.soup.Soup object at 0x...>
    
