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
object (path relative to ``ISoupAnnotatable``)::

    >>> path = locator.path('mysoup')
    >>> path
    '/'

So traverse has to return the plone site itself::

    >>> locator.traverse(path)
    <PloneSite at /plone>

The second step now is to get the soupdata from an annotation. An empty soup is
created at the first access::

    >>> locator.storage('mysoup')
    <souper.soup.SoupData object at 0x...>

But we never need the SoupData object itself, we want the soup. Thus theres is
a handy function available to fetch the soup::

    >>> from souper.soup import get_soup
    >>> get_soup(plone, 'mysoup')
    <souper.soup.Soup object at 0x...>
    
Now lets check if this works still if we change the location of the soup::

    >>> try:
    ...    locator.set_path('otherssoup', '/subfolder')
    ... except KeyError, e:
    ...    print e
    'subfolder'

    
So first we need the subfolder::

    >>> name = plone.invokeFactory('Folder', 'subfolder')
    >>> locator.set_path('otherssoup', '/subfolder')
    >>> locator.path('otherssoup')
    '/subfolder'

    >>> get_soup(plone, 'othersoup')
    <souper.soup.Soup object at 0x...>
    

