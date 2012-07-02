# -*- coding: iso-8859-15 -*-
from zope.schema import Bool, BytesLine, Int, Choice
from zope.i18nmessageid import ZopeMessageFactory as _
from zopyx.txng3.core import config
import zope.catalog.interfaces
import re

class ITingIndexSchema(zope.catalog.interfaces.IAttributeIndex):
    default_fields=BytesLine(
        title=_(u"Default fields"),
        description=_("Look in these fields by default (consider dedicated_storage=True)"),
        required=True,
        default=''
    )
    storage=Choice(
        title=_(u"Storage"),
        description=_(u"Component for storing wordID-to-documentID-mappings"),
        required=True,
        default=config.DEFAULT_STORAGE,
        vocabulary="TextIndexNG3 Storages"
    )
    dedicated_storage=Bool(
        title=_(u"Dedicated storage"),
        description=_(u"Use seperate index for each field (allows per field search)"),
        required=True,
        default=config.defaults['dedicated_storage']
    )
    languages=BytesLine(
        title=_(u"Languages"),
        description=_(u"Languages supported by this index (space seperated list)"),
        default=config.DEFAULT_LANGUAGE,
        constraint=re.compile('[a-z]+(\s+[a-z]+)*').match
    )
    use_stemmer=Bool(
        title=_(u"Stemming"),
        description=_(u"Compare words according to their word stems (a kind of similarity search)"),
        default=False,
        required=config.defaults['use_stemmer']
    )
    use_stopwords=Bool(
        title=_(u"Stopwords"),
        description=_(u"Enable to prvent looking for words like 'and' or 'a' which are unlike to be useful in search queries"),
        required=True,
        default=config.defaults['use_stopwords']
    )
    use_normalizer=Bool(
        title=_(u"Normalize"),
        description=_(u"Enable to normalize words language specific (e.g. Ã€ -> ae , Ãš -> e)"),
        required=True,
        default=config.defaults['use_normalizer']
    )
    ranking=Bool(
        title=_(u"Ranking"),
        description=_(u"Enable ranking according to word frequency of documents (selects different storage)"),
        required=True,
        default=config.defaults['ranking']
    )
    autoexpand_limit=Int(
        title=_(u"Autoexpand limit"),
        description=_(u"Lower limit for automatic right-*-wildcard-search"),
        required=True,
        default=config.defaults['autoexpand_limit']
    )
    splitter=Choice(
        title=_(u"Splitter"),
        description=_(u"Splitter to be used to turn text into words"),
        required=True,
        default=config.DEFAULT_SPLITTER,
        vocabulary="TextIndexNG3 Splitters"
    )
    lexicon=Choice(
        title=_(u"Lexicon"),
        description=_(u"Component to be used for storing word-to-id-mappings"),
        required=True,
        default=config.DEFAULT_LEXICON,
        vocabulary="TextIndexNG3 Lexicons"
    )
    index_unknown_languages=Bool(
        title=_(u"Index unknown languages"),
        description=_(u"Assigns unknown languages the first language of the languages selected for this index"),
        required=True,
        default=config.defaults['index_unknown_languages'],
    )
    splitter_additional_chars=BytesLine(
        title=_(u"Non-seperators"),
        description=_(u"Characters that should *not* be threaded as separators"),
        required=True,
        default=config.defaults['splitter_additional_chars']
    )
    splitter_casefolding=Bool(
        title=_(u"Case-insensitive"),
        description=_(u"Make this index case insensitive"),
        required=True,
        default=config.defaults['splitter_casefolding']
    )
    query_parser=Choice(
        title=_(u"Query Parser"),
        description=_(u"Parser to be used for this index"),
        required=True,
        default=config.DEFAULT_PARSER,
        vocabulary="TextIndexNG3 Query Parsers" 
    )

class ITingIndex(ITingIndexSchema, zope.catalog.interfaces.ICatalogIndex):
    pass