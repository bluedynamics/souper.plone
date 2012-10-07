Overview
========

``souper.plone`` integrates `souper <http://pypi.python.org/pypi/souper>`_ 
with `Plone <http://plone.org>`_ 

``souper.plone`` addresses developers with the need to solve the problem to 
store tiny entities of mass-data, where heavy weight Archetypes or 
Dexterity are too much effort and are to slow. I.e if you need a queryable 
container for non-CMSish content, like votes, data from a poll, orders in a 
webshop, measuring data, or alike.  

A Soup-container can be moved to an own ZODB mount-point and may be shared
across multiple independent Plone instances!

A control-panel provides actions to rebuild, reindex and move Soups around.


Usage
=====

``souper.plone`` offers some convinience for Plone Add-On developers. It 
provides a storage locator working like so:

A ``souper.soup`` is looked up by ``id`` and needs a context. This context is 
some Aquisition aware obejct in the plone site. It is used to acquire it's 
parent until ``ISoupRoot`` is found (which is by default the site root). At 
the soup root the ``id`` maps to a path where the soup is actually stored as
an annotation. This all happens fully transparent. So to get the soup one 
need to do just do::

    >>> from souper.soup import get_soup
    >>> soup = get_soup(context, 'my_soup_id')
    >>> soup
    <souper.soup.Soup at 0x...>

If no soup was found for given id, a new one is created and annotated by default
to the ``ISoupRoot``.

It is important provide a CatalogFactory. Consult the ``souper.plone`` 
documentation to learn how. Over there its also documented how to add records, 
query and maintain them.

For convinience ``souper.plone`` installs a control-panel where one can reindex
and rebuild distinct soups. 


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

- Robert Niederreiter <rnix [at] squarewave [dot] at>

- Jens W. Klein <jk [at] kleinundpartner [dot] at>

- Sven Plage
