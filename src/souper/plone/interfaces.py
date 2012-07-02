from zope.interface import (
    Interface,
    Attribute,
)


class ISouperLayer(Interface):
    """Browser Layer for soup related views"""


class ISoupAnnotatable(Interface):
    """Marker for persisting soup data.
    """
