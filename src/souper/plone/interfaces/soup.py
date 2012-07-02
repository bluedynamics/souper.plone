from zope.interface import (
    Interface,
    Attribute,
)


class ISoupLayer(Interface):
    """Browser Layer for soup related views"""


class ISoupAnnotatable(Interface):
    """Marker for persisting soup data.
    """
