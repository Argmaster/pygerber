from types import SimpleNamespace
from pygerber.meta.broker import DrawingBroker
from tests.testutils.apertures import ApertureCollector, get_dummy_apertureSet


def get_dummy_broker() -> DrawingBroker:
    return DrawingBroker(get_dummy_apertureSet())


def fill_dummy_apertures(broker: DrawingBroker):
    broker.define_aperture("C", None, 10, SimpleNamespace(DIAMETER=1, HOLE_DIAMETER=0))
    broker.define_aperture("R", None, 11, SimpleNamespace(X=1, Y=1, HOLE_DIAMETER=0))
    broker.define_aperture(
        "P",
        None,
        12,
        SimpleNamespace(DIAMETER=1, VERTICES=6, ROTATION=0, HOLE_DIAMETER=0),
    )
    return broker


def get_filled_broker() -> DrawingBroker:
    return fill_dummy_apertures(get_dummy_broker())


def get_collector_spec(function, *args):
    try:
        function(*args)
    except ApertureCollector.CalledWithSpec as e:
        return e.spec
    raise Exception("Failed to catch CalledWithSpec exception.")
