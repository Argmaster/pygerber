from __future__ import annotations

import time
from typing import TYPE_CHECKING

import pytest

from pygerber.vm.commands.layer import EndLayer, StartLayer
from pygerber.vm.commands.paste import PasteLayer
from pygerber.vm.commands.shape import Shape
from pygerber.vm.rvmc import RVMC
from pygerber.vm.types.box import Box
from pygerber.vm.types.errors import (
    EmptyAutoSizedLayerNotAllowedError,
    LayerAlreadyExistsError,
    LayerNotFoundError,
    NoLayerSetError,
)
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.vector import Vector
from pygerber.vm.vm import DeferredLayer, EagerLayer, Layer, VirtualMachine

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestVirtualMachine:
    def check_eager_handlers(self, vm: VirtualMachine) -> None:
        assert vm._on_shape_handler == vm.on_shape_eager
        assert vm._on_paste_layer_handler == vm.on_paste_layer_eager

    def check_deferred_handlers(self, vm: VirtualMachine) -> None:
        assert vm._on_shape_handler == vm.on_shape_deferred
        assert vm._on_paste_layer_handler == vm.on_paste_layer_deferred

    def test_set_handlers_for_layer_eager(self, mocker: MockerFixture) -> None:
        vm_mock = mocker.MagicMock(VirtualMachine)
        VirtualMachine.set_handlers_for_layer(
            vm_mock,
            EagerLayer(
                layer_id=LayerID(id="layer"), box=Box(), origin=Vector(x=0, y=0)
            ),
        )
        vm_mock.set_eager_handlers.assert_called_once()

    def test_set_handlers_for_layer_deferred(self, mocker: MockerFixture) -> None:
        vm_mock = mocker.MagicMock(VirtualMachine)
        VirtualMachine.set_handlers_for_layer(
            vm_mock,
            DeferredLayer(
                layer_id=LayerID(id="layer"), origin=Vector(x=0, y=0), commands=[]
            ),
        )
        vm_mock.set_deferred_handlers.assert_called_once()

    def test_set_handlers_for_layer_other(self, mocker: MockerFixture) -> None:
        vm_mock = mocker.MagicMock(VirtualMachine)
        with pytest.raises(NotImplementedError):
            VirtualMachine.set_handlers_for_layer(
                vm_mock,
                Layer(layer_id=LayerID(id="layer"), origin=Vector(x=0, y=0)),
            )

    def test_set_eager_handlers_for_layer(self, mocker: MockerFixture) -> None:
        vm = VirtualMachine()
        vm._on_shape_handler = mocker.MagicMock()
        vm._on_paste_layer_handler = mocker.MagicMock()
        vm.set_eager_handlers()

        self.check_eager_handlers(vm)

    def test_set_deferred_handlers_for_layer(self, mocker: MockerFixture) -> None:
        vm = VirtualMachine()
        vm._on_shape_handler = mocker.MagicMock()
        vm._on_paste_layer_handler = mocker.MagicMock()
        vm.set_deferred_handlers()

        self.check_deferred_handlers(vm)

    def test_create_eager_layer(self) -> None:
        vm = VirtualMachine()
        layer = vm.create_eager_layer(
            layer_id=LayerID(id="layer"), origin=Vector(x=0, y=0), box=Box()
        )
        assert isinstance(layer, EagerLayer)
        assert layer.layer_id == LayerID(id="layer")
        assert layer.box == Box()
        assert layer.origin == Vector(x=0, y=0)

    def test_create_deferred_layer(self) -> None:
        vm = VirtualMachine()
        layer = vm.create_deferred_layer(
            layer_id=LayerID(id="layer"), origin=Vector(x=0, y=0)
        )
        assert isinstance(layer, DeferredLayer)
        assert layer.layer_id == LayerID(id="layer")
        assert layer.origin == Vector(x=0, y=0)

    def test_on_shape_eager(self, mocker: MockerFixture) -> None:
        vm = VirtualMachine()
        on_shape_eager = mocker.spy(vm, vm.on_shape_eager.__name__)
        vm.set_eager_handlers()
        shape_mock = mocker.MagicMock()
        vm.on_shape(shape_mock)

        on_shape_eager.assert_called_once_with(shape_mock)

    def test_on_shape_deferred_no_layer_selected_error(
        self, mocker: MockerFixture
    ) -> None:
        vm = VirtualMachine()
        vm.set_deferred_handlers()
        shape_mock = mocker.MagicMock()

        with pytest.raises(NoLayerSetError):
            vm.on_shape(shape_mock)

    def test_on_shape_deferred(self, mocker: MockerFixture) -> None:
        vm = VirtualMachine()
        vm.set_deferred_handlers()
        shape_mock = mocker.MagicMock()

        vm.on_start_layer(StartLayer(id=LayerID(id="layer")))

        vm.on_shape(shape_mock)

        assert isinstance(vm.layer, DeferredLayer)
        assert shape_mock in vm.layer.commands

    def test_on_paste_layer_eager(self, mocker: MockerFixture) -> None:
        vm = VirtualMachine()
        on_paste_layer_eager = mocker.spy(vm, vm.on_paste_layer_eager.__name__)
        vm.set_eager_handlers()
        paste_layer_mock = mocker.MagicMock()
        vm.on_paste_layer(paste_layer_mock)

        on_paste_layer_eager.assert_called_once_with(paste_layer_mock)

    def test_on_paste_layer_deferred_no_layer_selected_error(
        self, mocker: MockerFixture
    ) -> None:
        vm = VirtualMachine()
        vm.set_deferred_handlers()
        paste_layer_mock = mocker.MagicMock()

        with pytest.raises(NoLayerSetError):
            vm.on_paste_layer(paste_layer_mock)

    def test_on_paste_layer_deferred(self, mocker: MockerFixture) -> None:
        vm = VirtualMachine()
        vm.set_deferred_handlers()
        paste_layer_mock = mocker.MagicMock()

        vm.on_start_layer(StartLayer(id=LayerID(id="layer")))

        vm.on_paste_layer(paste_layer_mock)

        assert isinstance(vm.layer, DeferredLayer)
        assert paste_layer_mock in vm.layer.commands

    def test_on_start_layer_eager(self) -> None:
        vm = VirtualMachine()
        cmd = StartLayer(
            id=LayerID(id="layer"),
            box=Box(),
            origin=Vector(x=0, y=0),
        )
        vm.on_start_layer(cmd)

        assert isinstance(vm.layer, EagerLayer)
        assert len(vm._layer_stack) == 1
        self.check_eager_handlers(vm)

    def test_on_start_layer_deferred(self) -> None:
        vm = VirtualMachine()
        vm.set_deferred_handlers()
        cmd = StartLayer(id=LayerID(id="layer"))
        vm.on_start_layer(cmd)

        assert isinstance(vm.layer, DeferredLayer)
        assert len(vm._layer_stack) == 1
        self.check_deferred_handlers(vm)

    def test_on_start_layer_deferred_layer_already_exists_error(self) -> None:
        vm = VirtualMachine()
        vm.on_start_layer(StartLayer(id=LayerID(id="layer"), box=Box()))
        with pytest.raises(LayerAlreadyExistsError):
            vm.on_start_layer(
                StartLayer(id=LayerID(id="layer"), box=None, origin=Vector(x=0, y=0))
            )

    def test_on_start_layer_eager_layer_already_exists_error(self) -> None:
        vm = VirtualMachine()
        vm.on_start_layer(
            StartLayer(id=LayerID(id="layer"), box=Box(), origin=Vector(x=0, y=0))
        )
        with pytest.raises(LayerAlreadyExistsError):
            vm.on_start_layer(
                StartLayer(id=LayerID(id="layer"), box=Box(), origin=Vector(x=0, y=0))
            )

    def test_get_layer(self) -> None:
        vm = VirtualMachine()
        vm.on_start_layer(
            StartLayer(id=LayerID(id="layer"), box=Box(), origin=Vector(x=0, y=0))
        )
        assert vm.get_layer(LayerID(id="layer")) == vm.layer

    def test_get_layer_layer_not_found(self) -> None:
        vm = VirtualMachine()
        with pytest.raises(LayerNotFoundError):
            vm.get_layer(LayerID(id="layer"))

    def test_on_end_layer_eager(self, mocker: MockerFixture) -> None:
        vm = VirtualMachine()
        layer_id = LayerID(id="layer")

        vm.on_start_layer(StartLayer(id=layer_id, box=Box(), origin=Vector(x=0, y=0)))
        vm.on_shape(mocker.MagicMock())
        vm.on_end_layer(EndLayer())

        assert layer_id in vm._layers
        assert len(vm._layer_stack) == 0

    def test_on_end_layer_deferred(self) -> None:
        vm = VirtualMachine()
        layer_id = LayerID(id="layer")

        vm.on_start_layer(StartLayer(id=layer_id, box=None, origin=Vector(x=0, y=0)))
        vm.on_shape(Shape.new_circle((0, 0), 1, is_negative=False))
        vm.on_end_layer(EndLayer())

        assert layer_id in vm._layers
        assert len(vm._layer_stack) == 0

    def test_on_end_layer_deferred_empty_auto_sized_layer_not_allowed(self) -> None:
        vm = VirtualMachine(fail_on_empty_auto_sized_layer=True)
        vm.on_start_layer(
            StartLayer(id=LayerID(id="layer"), box=None, origin=Vector(x=0, y=0))
        )
        with pytest.raises(EmptyAutoSizedLayerNotAllowedError):
            vm.on_end_layer(EndLayer())

    def test_on_end_layer_deferred_empty_auto_sized_layer(self) -> None:
        vm = VirtualMachine()
        vm.run(
            RVMC(
                commands=[
                    StartLayer(
                        id=LayerID(id="layer"), box=None, origin=Vector(x=0, y=0)
                    ),
                    EndLayer(),
                ]
            )
        )

    def test_on_end_layer_no_layer_set_error(self) -> None:
        vm = VirtualMachine()
        with pytest.raises(NoLayerSetError):
            vm.on_end_layer(EndLayer())

    def test_on_layer_end_other(self, mocker: MockerFixture) -> None:
        vm = VirtualMachine()

        vm._layer_stack.append(mocker.MagicMock())
        with pytest.raises(NotImplementedError):
            vm.on_end_layer(EndLayer())

    def test_on_end_layer_correct_handler_reassignment(self) -> None:
        vm = VirtualMachine()

        vm.on_start_layer(
            StartLayer(id=LayerID(id="%main%"), box=None, origin=Vector(x=0, y=0))
        )
        vm.on_shape(Shape.new_circle((0, 0), 1, is_negative=False))

        vm.on_start_layer(
            StartLayer(
                id=LayerID(id="secondary"),
                box=Box.from_center_width_height((1, 1), 2, 2),
                origin=Vector(x=0, y=0),
            )
        )
        self.check_eager_handlers(vm)

        vm.on_shape(Shape.new_circle((1, 1), 1, is_negative=False))
        vm.on_end_layer(EndLayer())

        self.check_deferred_handlers(vm)

        vm.on_end_layer(EndLayer())

        self.check_eager_handlers(vm)

    def test_calculate_deferred_layer_box_shape(self) -> None:
        vm = VirtualMachine()

        box = vm._calculate_deferred_layer_box(
            DeferredLayer(
                layer_id=LayerID(id="layer"),
                origin=Vector(x=0, y=0),
                commands=[Shape.new_circle((0, 0), 1, is_negative=False)],
            )
        )
        assert isinstance(box, Box)

    def test_calculate_deferred_layer_box_paste_layer(self) -> None:
        vm = VirtualMachine()

        layer_id = self._visit_layer_cmd(vm)

        box = vm._calculate_deferred_layer_box(
            DeferredLayer(
                layer_id=LayerID(id="layer"),
                origin=Vector(x=0, y=0),
                commands=[
                    PasteLayer(
                        source_layer_id=layer_id,
                        center=Vector(x=0, y=0),
                        is_negative=False,
                    )
                ],
            )
        )
        assert isinstance(box, Box)

    def _visit_layer_cmd(self, vm: VirtualMachine) -> LayerID:
        layer_id = LayerID(id=f"layer-{time.time():.0f}")

        StartLayer(id=layer_id, box=Box()).visit(vm)
        Shape.new_circle((0, 0), 1, is_negative=False).visit(vm)
        EndLayer().visit(vm)

        return layer_id

    def test_calculate_deferred_layer_box_other(self, mocker: MockerFixture) -> None:
        vm = VirtualMachine()

        with pytest.raises(NotImplementedError):
            vm._calculate_deferred_layer_box(
                DeferredLayer(
                    layer_id=LayerID(id="layer"),
                    origin=Vector(x=0, y=0),
                    commands=[mocker.MagicMock()],
                )
            )

    def test_calculate_deferred_layer_box_shape_and_paste(self) -> None:
        vm = VirtualMachine()

        layer_id = self._visit_layer_cmd(vm)

        box = vm._calculate_deferred_layer_box(
            DeferredLayer(
                layer_id=LayerID(id="layer"),
                origin=Vector(x=0, y=0),
                commands=[
                    Shape.new_circle((0, 0), 1, is_negative=False),
                    PasteLayer(source_layer_id=layer_id, center=Vector(x=0, y=0)),
                ],
            )
        )
        assert isinstance(box, Box)

    def test_calculate_deferred_layer_box_paste_and_shape(self) -> None:
        vm = VirtualMachine()

        layer_id = self._visit_layer_cmd(vm)

        box = vm._calculate_deferred_layer_box(
            DeferredLayer(
                layer_id=LayerID(id="layer"),
                origin=Vector(x=0, y=0),
                commands=[
                    Shape.new_circle((0, 0), 1, is_negative=False),
                    PasteLayer(source_layer_id=layer_id, center=Vector(x=0, y=0)),
                ],
            )
        )
        assert isinstance(box, Box)

    def test_calculate_deferred_layer_box_shape_and_other(
        self, mocker: MockerFixture
    ) -> None:
        vm = VirtualMachine()

        with pytest.raises(NotImplementedError):
            vm._calculate_deferred_layer_box(
                DeferredLayer(
                    layer_id=LayerID(id="layer"),
                    origin=Vector(x=0, y=0),
                    commands=[
                        Shape.new_circle((0, 0), 1, is_negative=False),
                        mocker.MagicMock(),
                    ],
                )
            )
