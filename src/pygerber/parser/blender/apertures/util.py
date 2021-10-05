# -*- coding: utf-8 -*-
from __future__ import annotations

import bpy
from PyR3.shortcut.context import Objects
from PyR3.shortcut.modifiers import Boolean
from PyR3.shortcut.modifiers import Solidify
from PyR3.shortcut.modifiers import Decimate
from PyR3.shortcut.edit import Edit
from PyR3.shortcut.mesh import join
from PyR3.shortcut.transform import Transform
from PyR3.shortcut.material import set_material

from pygerber.constants import Polarity
from pygerber.renderer import Renderer


class BlenderUtilMethods:

    renderer: Renderer

    @property
    def root(self) -> bpy.types.Object:
        return self.renderer.root

    @root.setter
    def root(self, value: bpy.types.Object):
        self.renderer.root = value

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
            if self.root is not None:
                self.commit_dark(ob)
            else:
                self.root = ob
                set_material(self.root, self.renderer.material)
        else:
            if self.root is not None:
                self.commit_clear(ob)

    def commit_clear(self, ob):
        if self.__is_dirty:
            self.clean_mesh()
        Boolean(self.root, ob, "DIFFERENCE").apply()
        Objects.delete(ob)

    __is_dirty = False
    # try using separate dark objects
    def commit_dark(self, ob):
        Boolean(self.root, ob, "UNION").apply()
        # Objects.select(ob)
        # Transform.scale((1, 1, 0.5))
        # Transform.apply(do_scale=True)
        # Boolean(ob, self.root, "DIFFERENCE").apply()
        # Transform.scale((1, 1, 2))
        # Transform.apply(do_scale=True)
        # join(self.root, ob)
        self.__is_dirty = True
        #    Decimate(self.root, decimate_type="DISSOLVE").apply()
        #    print(f"{len(edit.vertices())} {len(edit.edges())} {len(edit.faces())}")
        #    bpy.ops.mesh.dissolve_limited()
        #    edit.remove_doubles()
        #    print(f"{len(edit.vertices())} {len(edit.edges())} {len(edit.faces())}")
        # Boolean(self.root, ob, "UNION").apply()
        # Decimate(self.root, decimate_type="DISSOLVE").apply()
        try:
            Objects.delete(ob)
        except Exception:
            pass

    def clean_mesh(self):
        with Edit(self.root) as edit:
            edit.deselect_all()
            edit.select_vertices(lambda co: co.z < 0)
            edit.delete_vertices()
            for vert in edit.vertices():
                vert.co.z = 0
            print(f"{len(edit.vertices())} {len(edit.edges())} {len(edit.faces())}")
        #Boolean(self.root, None, "UNION").apply(operand_type="COLLECTION")
        Decimate(self.root, decimate_type="DISSOLVE").apply()
        self.solidify(self.root, self.renderer.thickness)
        #with Edit(self.root) as edit:
        #    edit.deselect_all()
        #    bpy.ops.mesh.select_non_manifold()
        #    edit.delete_faces()
        #    print(f"{len(edit.vertices())} {len(edit.edges())} {len(edit.faces())}")
        self.__is_dirty = False

    def solidify(self, ob, thickness):
        Solidify(ob, thickness, offset=0, use_even_offset=True).apply()
