# -*- coding: utf-8 -*-
from __future__ import annotations

import bpy

from PyR3.shortcut.modifiers import Boolean
from pygerber.constants import Polarity
from pygerber.renderer import Renderer
from PyR3.shortcut.context import Objects
from PyR3.shortcut.material import set_material


class BlenderUtilMethods:

    renderer: Renderer

    @property
    def root(self):
        return self.renderer.root

    @property
    def material(self):
        return self.renderer.material

    @property
    def thickness(self):
        if self.renderer.state.polarity == Polarity.DARK:
            return self.renderer.thickness
        else:
            return self.renderer.thickness * 2

    @property
    def inner_thickness(self):
        if self.renderer.state.polarity == Polarity.DARK:
            return self.renderer.thickness * 2
        else:
            return self.renderer.thickness * 3

    def commit_mesh_to_root(self, ob: bpy.types.Object):
        if self.renderer.state.polarity == Polarity.DARK:
            self.commit_dark(ob)
        else:
            self.commit_clear(ob)

    def commit_clear(self, ob):
        Boolean(self.root, ob, "DIFFERENCE").apply()
        Objects.delete(ob)

    def commit_dark(self, ob):
        set_material(ob, self.material)
        Boolean(self.root, ob, "UNION").apply()
        Objects.delete(ob)
