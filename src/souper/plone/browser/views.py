import transaction
from Acquisition import aq_inner
from zope.component import (
    getUtility,
    getUtilitiesFor,
)
from zope.component.interfaces import ComponentLookupError
from souper.interfaces import (
    ISoup,
    ICatalogFactory,
    IStorageLocator,
)
from souper.soup import (
    get_soup,
)
from Products.Five import BrowserView

class SoupAdmin(BrowserView):

    @property
    def info(self):
        return self.request.form.get('info', '')

    @property
    def existing_soups(self):
        ret = list()
        for name, soup in getUtilitiesFor(ICatalogFactory):
            ret.append(name)
        return ret

    def count(self, soup):
        soup = getSoup(aq_inner(self.context), soup)
        return len(soup.storage)

    def redirect_base(self, msg):
        url = self.context.absolute_url()
        url += '/soup-controlpanel?info=%s' % msg
        self.request.RESPONSE.redirect(url)

    def storage_path(self, id):
        try:
            path = StorageLocator(self.context).path(id)
        except KeyError, e:
            path = '/ (not initialized yet)'
        else:
            if not path.startswith('/'):
                path = '/' + path
        return path

    def reindex_soup(self):
        id = self.request.form.get('id')
        if not id:
            return self.redirect_base('No id')
        soup = getSoup(self.context, id)
        soup.reindex()
        msg = '%s reindexed.' % id
        return self.redirect_base(msg)

    def rebuild_soup(self):
        id = self.request.form.get('id')
        if not id:
            return self.redirect_base(msg)
        soup = getSoup(self.context, id)
        soup.rebuild()
        msg = '%s rebuilt.' % id
        return self.redirect_base(msg)

    def move_storage(self):
        id = self.request.form.get('id')
        if not id:
            return self.redirect_base(u'No id given')
        path = self.request.form.get('path')
        if not path:
            return self.redirect_base(u'No path given')
        locator = StorageLocator(self.context)
        try:
            target = locator.traverse(path)
        except ValueError:
            return self.redirect_base(u'Desired path not exists')
        method = self.request.form.get('moveormount')
        if method == 'move':
            locator.move(id, path)
            transaction.commit()
            return self.redirect_base(u'Moved storage of %s to %s' % (id, path))
        elif method == "mount":
            locator.relocate(id, path)
            transaction.commit()
            return self.redirect_base(u'Mounted storage %s to %s' % (id, path))
        else:
            return self.redirect_base(u'Invalid action (move or mount only)')

    def rebuild_length(self):
        id = self.request.form.get('id')
        if not id:
            return self.redirect_base(msg)
        soup = getSoup(self.context, id)
        newlen = len(soup.storage.data)
        soup.storage.length.set(newlen)
        transaction.commit()
        return self.redirect_base(u'Length of storage %s is %s' % (id, newlen))
