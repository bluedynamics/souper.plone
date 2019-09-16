from copy import deepcopy
from Acquisition import aq_inner
from Acquisition import aq_parent
from persistent.mapping import PersistentMapping
from zope.interface import implementer
from zope.annotation import IAnnotations
from souper.interfaces import IStorageLocator
from souper.soup import SoupData
from souper.soup import get_soup
from souper.plone.interfaces import ISoupRoot

CACHE_PREFIX = 'soup_storage_%s'
SOUPPATHS = 'SOUPPATHS'
SOUPKEY = 'SOUP-%s'


@implementer(IStorageLocator)
class StorageLocator(object):

    def __init__(self, context):
        self.context = context

    def storage(self, sid):
        """return SoupData for the given soup id
        """
        context = self.traverse(self.path(sid))
        return self.soupdata(context, sid)

    @property
    def root(self):
        """ Find the root in the soup, place where path's mapping is located.
        """
        obj = aq_inner(self.context)
        while True:
            if ISoupRoot.providedBy(obj):
                return obj
            obj = aq_parent(obj)
            if not obj:
                raise AttributeError(u"Invalid soup context '%s;." %
                                     self.context)

    def path(self, sid):
        """path to object with soupdata annotations for given soup id.
        relative to root.
        """
        paths = IAnnotations(self.root).get(SOUPPATHS, {})
        return paths.get(sid, '/')

    def set_path(self, sid, newpath):
        """maps path to object with soupdata annotations for given soup id.
        it does not check if there is already a soup before nor does it warn if
        there was a soup at the old location.
        """
        self.traverse(newpath)  # check if newpath is ok
        paths = IAnnotations(self.root).get(SOUPPATHS, None)
        if paths is None:
            paths = PersistentMapping()
            IAnnotations(self.root)[SOUPPATHS] = paths
        paths[sid] = newpath
        self._invalidate_cache(sid)

    def traverse(self, path):
        """traverse to path relative to soups root and return the object there.
        """
        obj = self.root
        path = [_ for _ in path.split('/') if _]
        for name in path:
            try:
                obj = obj[name]
            except AttributeError:
                msg = u'Object at %s does not exist.' % '/'.join(path)
                raise ValueError(msg)
        return obj

    def soupdata(self, obj, sid):
        """fetches the soup data from objects annotations.
        """
        key = SOUPKEY % sid
        annotations = IAnnotations(obj)
        if key not in annotations:
            annotations[key] = SoupData()
        return annotations[key]

    def _invalidate_cache(self, sid):
        """invalidates a cache on REQUEST
        """
        # XXX unused (at the moment)
        key = CACHE_PREFIX % sid
        if self.context.REQUEST.get(key):
            del self.context.REQUEST[key]

    def move(self, sid, target_path, force=False):
        """moves soup with name ``sid`` to a other target object.
        target_path is the relative path to soup root.
        if force is true any existing soup with the same name is overwritten.
        """
        source_obj = self.traverse(self.path(sid))
        source_annotations = IAnnotations(source_obj)
        source_data = self.storage(sid)
        target_obj = self.traverse(target_path)
        target_annotations = IAnnotations(target_obj)
        datakey = SOUPKEY % sid
        if datakey in target_annotations and not force:
            raise KeyError('Annotation-Key %s already used at %s' %
                           (datakey, target_path))
        self.set_path(sid, target_path)
        target_annotations[sid] = SoupData()
        target_soup = get_soup(sid, self.context)
        for intid in source_data.data:
            target_soup.add(deepcopy(source_data.data[intid]))
        del source_annotations[datakey]
        self._invalidate_cache(sid)
