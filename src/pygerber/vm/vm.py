"""`base` module contains definition of base `VirtualMachine` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Optional, Union

from pygerber.vm.command_visitor import CommandVisitor
from pygerber.vm.commands import EndLayer, PasteLayer, Shape, StartLayer
from pygerber.vm.rvmc import RVMC
from pygerber.vm.types.box import Box
from pygerber.vm.types.errors import (
    EmptyAutoSizedLayerNotAllowedError,
    LayerAlreadyExistsError,
    LayerNotFoundError,
    NoLayerSetError,
    NoMainLayerError,
)
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.vector import Vector

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

DrawCmdT: TypeAlias = Union[Shape, PasteLayer]


class Result:
    """The `Result` class is a wrapper around items returned from virtual machine.

    It is used as a base class for results returned from vms extending `VirtualMachine`
    class.
    """

    main_box: Box

    def __init__(self, main_box: Box) -> None:
        self.main_box = main_box


class Layer:
    """`Layer` class represents drawing space in virtual machine.

    This class has two direct subclasses: `EagerLayer` and `DeferredLayer`.
    It is necessary to distinguish between them because we need to support
    creation of layer with known size and creation of layer with size unknown at
    creation time. `EagerLayer` is used for the former and `DeferredLayer` for the
    latter.
    """

    origin: Vector
    """Origin of the layer.

    Origin point represents local coordinates of the layer center.
    """

    def __init__(self, layer_id: LayerID, origin: Vector) -> None:
        self.layer_id = layer_id
        self.origin = origin


class EagerLayer(Layer):
    """`EagerLayer` class represents drawing space of known fixed size.

    Commands executed on this layer are executed immediately.
    """

    def __init__(self, layer_id: LayerID, box: Box, origin: Vector) -> None:
        super().__init__(layer_id, origin)
        self.box = box


class DeferredLayer(Layer):
    """`DeferredLayer` class represents drawing space of size unknown at time of
    creation of layer.

    Commands executed on this layer are deferred until the layer is finished and
    size of layer can be determined.

    You cannot paste unfinished DeferredLayer into another unfinished DeferredLayer.
    """

    def __init__(
        self, layer_id: LayerID, origin: Vector, commands: list[DrawCmdT]
    ) -> None:
        super().__init__(layer_id, origin)
        self.commands = commands


class VirtualMachine(CommandVisitor):
    """Virtual machine for executing simple drawing commands."""

    MAIN_LAYER_ID: ClassVar[LayerID] = LayerID(id="%main%")

    def __init__(self) -> None:
        self.set_eager_handlers()

        self._layers: dict[LayerID, Layer] = {}
        self._layer_stack: list[Layer] = []

    def set_handlers_for_layer(self, layer: Layer) -> None:
        """Set handlers for given layer."""
        if isinstance(layer, EagerLayer):
            self.set_eager_handlers()

        elif isinstance(layer, DeferredLayer):
            self.set_deferred_handlers()

        else:
            raise NotImplementedError(type(layer))

    def set_eager_handlers(self) -> None:
        """Set handlers for eager mode."""
        self._on_shape_handler = self.on_shape_eager
        self._on_paste_layer_handler = self.on_paste_layer_eager

    def set_deferred_handlers(self) -> None:
        """Set handlers for deferred mode."""
        self._on_shape_handler = self.on_shape_deferred
        self._on_paste_layer_handler = self.on_paste_layer_deferred

    def create_eager_layer(self, layer_id: LayerID, box: Box, origin: Vector) -> Layer:
        """Create new eager layer instances (factory method)."""
        return EagerLayer(layer_id, box, origin)

    def create_deferred_layer(self, layer_id: LayerID, origin: Vector) -> Layer:
        """Create new deferred layer instances (factory method)."""
        return DeferredLayer(layer_id, origin, commands=[])

    def on_shape(self, command: Shape) -> None:
        """Visit `Shape` command."""
        self._on_shape_handler(command)

    def on_shape_eager(self, command: Shape) -> None:
        """Visit `Shape` command."""

    def on_shape_deferred(self, command: Shape) -> None:
        """Visit `Shape` command."""
        layer = self.layer
        assert isinstance(layer, DeferredLayer)
        layer.commands.append(command)

    def on_paste_layer(self, command: PasteLayer) -> None:
        """Visit `PasteLayer` command."""
        self._on_paste_layer_handler(command)

    def on_paste_layer_eager(self, command: PasteLayer) -> None:
        """Visit `PasteLayer` command.

        This method is used when currently selected layer is a eager layer.
        """

    def on_paste_layer_deferred(self, command: PasteLayer) -> None:
        """Visit `PasteLayer` command.

        This method is used when currently selected layer is a deferred layer.
        """
        layer = self.layer
        assert isinstance(layer, DeferredLayer)
        layer.commands.append(command)

    def on_start_layer(self, command: StartLayer) -> None:
        """Visit `StartLayer` command."""
        if command.id in self._layers:
            raise LayerAlreadyExistsError(command.id)

        if command.box is None:
            layer = self.create_deferred_layer(command.id, command.origin)
            self.set_layer(command.id, layer)
            self.set_deferred_handlers()

        else:
            layer = self.create_eager_layer(command.id, command.box, command.origin)
            self.set_layer(command.id, layer)
            self.set_eager_handlers()

        self.push_layer_to_stack(layer)

    def set_layer(self, layer_id: LayerID, layer: Layer) -> None:
        """Assign layer object to particular ID in layer index.

        Overwriting existing layer is not allowed.
        """
        self._layers[layer_id] = layer

    def get_layer(self, layer_id: LayerID) -> Layer:
        """Get layer by ID."""
        if layer_id not in self._layers:
            raise LayerNotFoundError(layer_id)

        return self._layers[layer_id]

    @property
    def layer(self) -> Layer:
        """Get current layer."""
        if len(self._layer_stack) == 0:
            raise NoLayerSetError

        return self._layer_stack[-1]

    def is_layer_stack_empty(self) -> bool:
        """Check if layer stack is empty."""
        return len(self._layer_stack) == 0

    def push_layer_to_stack(self, layer: Layer) -> None:
        """Push layer to layer stack."""
        self._layer_stack.append(layer)

    def pop_layer_from_stack(self) -> Layer:
        """Pop layer from layer stack."""
        assert len(self._layer_stack) > 0
        return self._layer_stack.pop()

    def on_end_layer(self, command: EndLayer) -> None:
        """Visit `EndLayer` command."""
        if len(self._layer_stack) <= 0:
            raise NoLayerSetError

        assert isinstance(command, EndLayer)

        top_layer = self.pop_layer_from_stack()

        if isinstance(top_layer, EagerLayer):
            pass

        elif isinstance(top_layer, DeferredLayer):
            box = self._calculate_deferred_layer_box(top_layer)
            if box is None:
                # Empty layers are not retained.
                raise EmptyAutoSizedLayerNotAllowedError(top_layer.layer_id)

            new_layer = self.create_eager_layer(
                top_layer.layer_id, box, top_layer.origin
            )
            self.set_layer(top_layer.layer_id, new_layer)

            self.push_layer_to_stack(new_layer)
            self.set_eager_handlers()
            self._eval_deferred_commands(top_layer.commands)
            self.pop_layer_from_stack()

        else:
            raise NotImplementedError(type(top_layer))

        if self.is_layer_stack_empty():
            self.set_eager_handlers()
            return

        # We need to set correct handler for next layer in case current layer creation
        # interrupted process of creating another eager/deferred layer.
        self.set_handlers_for_layer(self.layer)

    def _calculate_deferred_layer_box(
        self, deferred_layer: DeferredLayer
    ) -> Optional[Box]:
        commands = deferred_layer.commands
        box: Optional[Box] = None

        if len(commands) == 0:
            return None

        cmd = commands[0]

        if isinstance(cmd, Shape):
            box = cmd.outer_box

        elif isinstance(cmd, PasteLayer):
            layer = self._layers[cmd.source_layer_id]
            assert isinstance(layer, EagerLayer)
            box = layer.box + cmd.center - layer.origin

        else:
            raise NotImplementedError(type(cmd))

        for cmd in commands[1:]:
            if isinstance(cmd, Shape):
                box = box + cmd.outer_box

            elif isinstance(cmd, PasteLayer):
                layer = self._layers[cmd.source_layer_id]
                assert isinstance(layer, EagerLayer)
                box = box + (layer.box + cmd.center - layer.origin)

            else:
                raise NotImplementedError(type(cmd))

        return box

    def _eval_deferred_commands(self, commands: list[DrawCmdT]) -> None:
        for cmd in commands:
            cmd.visit(self)

    def run(self, rvmc: RVMC) -> Result:
        """Execute all commands."""
        for command in rvmc.commands:
            command.visit(self)
        layer = self._layers.get(self.MAIN_LAYER_ID, None)

        if layer is None:
            raise NoMainLayerError

        assert isinstance(layer, EagerLayer)
        return Result(layer.box)
