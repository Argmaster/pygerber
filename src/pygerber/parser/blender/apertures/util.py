# -*- coding: utf-8 -*-
from __future__ import annotations

import bpy
from PyR3.shortcut.context import Objects
from PyR3.shortcut.material import set_material
from PyR3.shortcut.modifiers import Boolean, Solidify

from pygerber.constants import Polarity
from pygerber.renderer import Renderer


class BlenderUtilMethods:

    renderer: Renderer

    @property
    def tree(self) -> Objects:
        return self.renderer.tree

    @tree.setter
    def tree(self, value: Objects):
        self.renderer.tree = value

    @property
    def material(self):
        return self.renderer.material

    @property
    def thickness(self):
        if self.renderer.state.polarity == Polarity.DARK:
            return self.renderer.thickness
        else:
            return self.renderer.thickness * 2.0

    @property
    def inner_thickness(self):
        if self.renderer.state.polarity == Polarity.DARK:
            return self.renderer.thickness * 2.0
        else:
            return self.renderer.thickness * 3.0

    def commit_mesh_to_root(self, ob: bpy.types.Object):
        if self.renderer.state.polarity == Polarity.DARK:
            set_material(ob, self.renderer.material)
            if self.tree is not None:
                self.commit_dark(ob)
            else:
                self.tree = Objects([ob])
        else:
            if self.tree is not None:
                self.commit_clear(ob)

    def commit_clear(self, ob):
        for submesh in self.tree:
            Boolean(submesh, ob, "DIFFERENCE").apply()
        Objects.delete(ob)

    def commit_dark(self, ob):
        self.tree.append(ob)

    def solidify(self, ob, thickness):
        Solidify(ob, float(thickness), offset=0.0, use_even_offset=True).apply()
