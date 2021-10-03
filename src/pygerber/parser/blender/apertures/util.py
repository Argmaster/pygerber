# -*- coding: utf-8 -*-
from __future__ import annotations

import bpy
from PyR3.shortcut.material import set_material
from PyR3.shortcut.modifiers import Boolean
from PyR3.shortcut.modifiers import Solidify
from PyR3.shortcut.context import Objects

from pygerber.constants import Polarity
from pygerber.renderer import Renderer


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

    def commit_mesh_to_root(self, ob: bpy.types.Object):
        if self.renderer.state.polarity == Polarity.DARK:
            self.commit_dark(ob)
        else:
            self.commit_clear(ob)

    def commit_clear(self, ob):
        Solidify(ob, self.thickness, offset=0, use_even_offset=True).apply()
        Boolean(self.root, ob, "DIFFERENCE").apply()
        Objects.delete(ob)

    def commit_dark(self, ob):
        set_material(ob, self.material)
        Solidify(ob, self.thickness, offset=0, use_even_offset=True).apply()
        Boolean(self.root, ob, "UNION").apply()
        Objects.delete(ob)
