from zope.interface import Interface


class ISouperLayer(Interface):
    """Browser Layer for soup related views"""


class ISoupRoot(Interface):
    """Marker for root object used to persist soup mapping.
    """
