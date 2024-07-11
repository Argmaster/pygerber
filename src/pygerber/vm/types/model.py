"""`model` module definition of common base class for all `VirtualMachine` related
model types.
"""

from __future__ import annotations

from pydantic import BaseModel


class VMModelType(BaseModel):
    """Common base class for all VM model types."""
