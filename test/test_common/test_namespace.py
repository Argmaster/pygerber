from __future__ import annotations

import pytest

from pygerber.common.namespace import Namespace


def test_not_instantiable() -> None:
    class A(Namespace):
        a: int = 1

    assert A.a == 1
    with pytest.raises(TypeError):
        A()
