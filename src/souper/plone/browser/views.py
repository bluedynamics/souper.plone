import transaction
from Acquisition import aq_inner
from zope.component import getUtilitiesFor
from souper.interfaces import ICatalogFactory
from souper.interfaces import IStorageLocator
from souper.soup import get_soup
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

    def count(self, sid):
        soup = get_soup(sid, aq_inner(self.context))
        return len(soup.storage)

    def redirect_base(self, msg):
        url = self.context.absolute_url()
        url += '/soup-controlpanel?info=%s' % msg
        self.request.RESPONSE.redirect(url)

    def storage_path(self, sid):
        locator = IStorageLocator(self.context)
        path = locator.path(sid)
        if not path.startswith('/'):
            path = '/' + path
        return path

    def reindex_soup(self):
        sid = self.request.form.get('id')
        if not sid:
            return self.redirect_base('No soup id given!')
        soup = get_soup(sid, self.context)
        soup.reindex()
        msg = '%s reindexed.' % sid
        return self.redirect_base(msg)

    def rebuild_soup(self):
        sid = self.request.form.get('id')
        if not sid:
            return self.redirect_base('No soup id given')
        soup = get_soup(sid, self.context)
        soup.rebuild()
        msg = '%s rebuilt.' % sid
        return self.redirect_base(msg)

    def clear_soup(self):
        sid = self.request.form.get('id')
        if not sid:
            return self.redirect_base('No soup id given!')
        soup = get_soup(sid, self.context)
        soup.clear()
        msg = '%s cleared.' % sid
        return self.redirect_base(msg)

    def move_storage(self):
        sid = self.request.form.get('id')
        if not sid:
            return self.redirect_base(u'No id given')
        path = self.request.form.get('path')
        locator = IStorageLocator(self.context)
        try:
            locator.traverse(path)
        except ValueError:
            return self.redirect_base(u'Desired path does not exist!')
        method = self.request.form.get('moveormount')
        if method == 'move':
            locator.move(sid, path)
            transaction.commit()
            return self.redirect_base(u'Moved storage of %s to %s' %
                                      (sid, path))
        elif method == "mount":
            locator.set_path(sid, path)
            transaction.commit()
            return self.redirect_base(u'Mounted storage %s to %s' %
                                      (sid, path))
        else:
            return self.redirect_base(u'Invalid action (move or mount only)')

    def rebuild_length(self):
        sid = self.request.form.get('id')
        if not sid:
            return self.redirect_base('No soup id given')
        soup = get_soup(sid, self.context)
        newlen = len(soup.storage.data)
        soup.storage.length.set(newlen)
        transaction.commit()
        return self.redirect_base(u'Length of storage %s is %s' %
                                  (sid, newlen))
