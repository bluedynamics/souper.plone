###############################################################################
# * This code has been contribued by Ivo van der Wijk
# * This code was improved by Frank Burkhardt
# * More improvements and tests by Simon Pamies
# * Stripped down dependencies to zope.catalog and txng core stuff by 
#   Robert Niederreiter
###############################################################################

import persistent
import BTrees
from zope.interface import implementer
from zope.component import createObject
from zope.index import interfaces
import zope.catalog.attribute
import zope.catalog.text
import zope.index.interfaces

from zopyx.txng3.core import config
from zopyx.txng3.core.index import Index
from zopyx.txng3.core.content import IndexContentCollector
from zopyx.txng3.core.interfaces import (
    IStorageWithTermFrequency,
    IIndexableContent,
)
from souper.plone.interfaces.ting import ITingIndex

defaults = {
    'use_stemmer': config.defaults['use_stemmer'],
    'dedicated_storage': config.defaults['dedicated_storage'],
    'ranking': config.defaults['ranking'],
    'use_normalizer': config.defaults['use_normalizer'],
    'languages': config.DEFAULT_LANGUAGE,
    'use_stopwords': config.defaults['use_stopwords'],
    'autoexpand_limit': config.defaults['autoexpand_limit'],
    'splitter': config.DEFAULT_SPLITTER,
    'index_unknown_languages': config.defaults['index_unknown_languages'],
    'query_parser': config.DEFAULT_PARSER,
    'lexicon': config.DEFAULT_LEXICON,
    'splitter_add_chars': config.defaults['splitter_additional_chars'],
    'storage': config.DEFAULT_STORAGE,
    'splitter_casefolding': config.defaults['splitter_casefolding']
}


@implementer(IIndexableContent)
class SoupIndexableContent(object):

    def __init__(self, context):
        self.context = context

    def indexableContent(self, fields):
        icc = IndexContentCollector()
        for field in fields:
            if field not in self.context.attrs:
                continue
            text = self.context.attrs[field]
            if not isinstance(text, basestring):
                # todo: handle binary data here
                msg = u'node attribute %s is not a string type'
                raise ValueError(msg % field)
            if not isinstance(text, unicode) \
               and isinstance(text, basestring):
                text = unicode(text, encoding='utf-8')
            icc.addContent(field, text)
        return icc


@implementer(zope.index.interfaces.IInjection,
             zope.index.interfaces.IStatistics,
             zope.index.interfaces.IIndexSearch,
             ITingIndex)
class TingIndex(zope.catalog.text.TextIndex,
                persistent.Persistent):

    def __init__(self,
                 field_name=None,
                 interface=None,
                 field_callable=False,
                 use_stemmer=defaults['use_stemmer'],
                 dedicated_storage=defaults['dedicated_storage'],
                 ranking=defaults['ranking'],
                 use_normalizer=defaults['use_normalizer'],
                 languages=defaults['languages'],
                 use_stopwords=defaults['use_stopwords'],
                 autoexpand_limit=defaults['autoexpand_limit'],
                 splitter=defaults['splitter'],
                 index_unknown_languages=defaults['index_unknown_languages'],
                 query_parser=defaults['query_parser'],
                 lexicon=defaults['lexicon'],
                 splitter_additional_chars=defaults['splitter_add_chars'],
                 storage=defaults['storage'],
                 splitter_casefolding=defaults['splitter_casefolding'],
                 asIFSet=True):
        if ranking:
            util = createObject(storage)
            if not IStorageWithTermFrequency.providedBy(util):
                raise ValueError("This storage cannot be used for ranking")
        if isinstance(field_name, basestring):
            _fields = field_name.split(' ')
        else:
            _fields = field_name
        zope.catalog.attribute.AttributeIndex.__init__(
            self, _fields[0], interface, field_callable)
        if len(_fields) < 2:
            dedicated_storage = False
        _default_fields = [_fields[0]]
        self._index = Index(
            fields=_fields,
            languages=languages.split(' '),
            use_stemmer=use_stemmer,
            dedicated_storage=dedicated_storage,
            ranking=ranking,
            use_normalizer=use_normalizer,
            use_stopwords=use_stopwords,
            storage=storage,
            autoexpand_limit=autoexpand_limit,
            splitter=splitter,
            lexicon=lexicon,
            index_unknown_languages=index_unknown_languages,
            query_parser=query_parser,
            splitter_additional_chars=splitter_additional_chars,
            splitter_casefolding=splitter_casefolding
        )
        self.languages = languages
        self.use_stemmer = use_stemmer
        self.dedicated_storage = dedicated_storage
        self.ranking = ranking
        self.use_normalizer = use_normalizer
        self.use_stopwords = use_stopwords
        self.interface = interface
        self.storage = storage
        self.autoexpand_limit = autoexpand_limit
        self.default_fields = _default_fields
        self._fields = _fields
        self.splitter = splitter
        self.lexicon = lexicon
        self.index_unknown_languages = index_unknown_languages
        self.query_parser = query_parser
        self.splitter_additional_chars = splitter_additional_chars
        self.splitter_casefolding = splitter_casefolding
        self._asIFSet = asIFSet

    def clear(self):
        self._index.clear()

    def documentCount(self):
        """See interface IStatistics
        """
        return len(self._index.getStorage(self.default_fields[0]))

    def wordCount(self):
        """See interface IStatistics
        """
        return len(self._index.getLexicon())

    def index_doc(self, docid, value):
        """See interface IInjection
        """
        if value is not None:
            self._index.index_object(value, docid)

    def unindex_doc(self, docid):
        """See interface IInjection
        """
        self._index.unindex_object(docid)

    def apply(self, query):
        kw = dict()
        if isinstance(query, dict):
            kw.update(query)
            query = kw['query']
            del kw['query']
        res = self._index.search(query, **kw).getDocids()
        if self._asIFSet:
            return BTrees.IFBTree.IFSet(res)
        return res
