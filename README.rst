Overview
========

``souper.plone`` integrates `souper <http://pypi.python.org/pypi/souper>`_
with `Plone <http://plone.org>`_

``souper.plone`` helps developers who need to store many small data records,
where heavy-weight Archetypes or Dexterity content types are too much effort
and are too slow.  E.g. if you need a queryable container for non-CMSish
content, like votes, data from a poll, orders in a webshop, measuring data,
or the like.

A Soup-container can be moved to an own ZODB mount-point and may be shared
across multiple independent Plone instances!

A control-panel provides actions to rebuild, reindex and move Soups around.


Usage
=====

``souper.plone`` adds some convenience for Plone Add-On developers. It
provides a storage locator working like so:

A ``souper.soup`` is looked up by ``id`` and needs a context.
This context is some aquisition-aware object in the Plone site.
From the context, souper tries to acquire an object implementing
``ISoupRoot`` (the *soup root*). By default, this will be the site root.
At the soup root, the ``id`` maps to a path where the soup is actually
stored as an annotation. This all happens fully transparently.
So to get the soup, one simply needs to do::

    >>> from souper.soup import get_soup
    >>> soup = get_soup('my_soup_id', context)
    >>> soup
    <souper.soup.Soup at 0x...>

If no soup was found for the given id, a new one is created as an annotation
on the ``ISoupRoot``.

It is important provide a ``CatalogFactory``.
Consult the ``souper.plone`` documentation to learn how.
Over there it's also documented how to add records, query and maintain them.

For convenience ``souper.plone`` installs a control-panel where one can
reindex and rebuild distinct soups.


Source Code
===========

The sources are in a GIT DVCS with its main branches at
`github <http://github.com/bluedynamics/souper.plone>`_.

We'd be happy to see many forks and pull-requests to make souper even better.

Maintainers are Robert Niederreiter, Jens Klein and the BlueDynamics Alliance
developer team. We appreciate any contribution and if a release is needed
to be done on pypi, please just contact one of us
`dev@bluedynamics dot com <mailto:dev@bluedynamics.com>`_


Contributors
============

- Robert Niederreiter
- Jens W. Klein
- Sven Plage
- Jean Jordaan
- Peter Mathis
- Harald Friessnegger
- Gil Forcada Codinachs
