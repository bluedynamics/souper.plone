from copy import deepcopy
from Acquisition import (
    aq_inner,
    aq_parent,
)
from zope.interface import implementer
from zope.annotation import IAnnotations
from souper.interfaces import IStorageLocator
from souper.soup import (
    get_soup,
    SoupData,
)
from souper.plone.interfaces import ISoupAnnotatable

CACHE_PREFIX = 'soup_storage_%s'


@implementer(IStorageLocator)
class StorageLocator(object):

    def __init__(self, context):
        self.context = context

    @property
    def root(self):
        obj = aq_inner(self.context)
        while True:
            if ISoupAnnotatable.providedBy(obj):
                return obj
            obj = aq_parent(obj)
            if not obj:
                raise AttributeError(u"Invalid soup context.")

    def storage(self, sid):
        return self.locate(sid)

    def path(self, sid):
        annotations = IAnnotations(self.root)
        key = 'soup_path_%s' % sid
        return annotations.get(key, '/')

    def traverse(self, path):
        obj = self.root
        path = path.split('/')
        for name in path:
            try:
                obj = obj[name]
            except AttributeError:
                msg = u'Object at %s does not exist.' % '/'.join(path)
                raise ValueError(msg)
        return obj

    def soupdata(self, obj, sid):
        key = 'SOUP-%s' % sid
        annotations = IAnnotations(obj)
        if not key in annotations:
            annotations[key] = SoupData()
        return annotations[key]

    def locate(self, sid):
        context = self.traverse(self.path(sid))
        return self.soupdata(context, sid)

    def _invalidate_cache(self, sid):
        key = CACHE_PREFIX % sid
        if self.context.REQUEST.get(key):
            del self.context.REQUEST[key]

    # XXX check move and relocate 
    def move(self, sid, target_path):
        target_context = self.traverse(target_path)
        target_annotations = IAnnotations(target_context)
        if sid in target_annotations:
            raise KeyError('Annotation-Key %s already used at %s' %
                           (sid, target_path))
        root_annotations = IAnnotations(self.root)
        source_data = self.storage(sid).data
        root_ann_obj = root_annotations[sid]
        if not isinstance(root_ann_obj, SoupData):
            source_annotations = IAnnotations(self.traverse(root_ann_obj))
            del source_annotations[sid]
        root_annotations[sid] = target_path
        self._invalidate_cache(sid)
        target_soup = get_soup(self.context, sid)
        # access soup.storage once if empty soup is copied. annotation is
        # created on first storage access !!!
        target_soup.storage
        for key in source_data:
            target_soup.add(deepcopy(source_data[key]))

    def relocate(self, sid, target_path):
        target_context = self.traverse(target_path)
        target_annotations = IAnnotations(target_context)
        if sid not in target_annotations:
            raise KeyError('Annotation-Key %s must exist at %s' %
                           (sid, target_path))
        root_annotations = IAnnotations(self.root)
        root_annotations[sid] = target_path
        self._invalidate_cache(sid)
        get_soup(self.context, sid)
