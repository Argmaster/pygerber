"""The `signals` module contains the signals (exceptions) used by the optimizer passes
to alter code structure.
"""

from __future__ import annotations


class BaseSignal(Exception):  # noqa: N818
    """Base class for all signals."""


class DeepDiscardNode(BaseSignal):
    """Signal to discard currently visited node the node from File node.

    This signal travels to the very bottom of AST walker and discards currently visited
    node of File. As a result invoking this signal in for example subnode of `AB`, will
    discard whole `AB` node.
    """


class ShallowDiscardNode(BaseSignal):
    """Signal to discard currently visited node from the parent node.

    This signal discards currently visited node from the parent node. As a result
    invoking this signal in for example subnode of `AB`, will discard only this subnode
    of `AB`.
    """
