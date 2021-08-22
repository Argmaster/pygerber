# -*- coding: utf-8 -*-
from unittest import TestCase, main

from pygerber.mathclasses import BoundingBox, Vector2D


class DataClassesTest(TestCase):
    def test_Vector2D(self):
        v = Vector2D(10, 11)
        self.assertEqual(v.x, 10)
        self.assertEqual(v.y, 11)

    def test_Vector2D_as_tuple(self):
        v = Vector2D(10, 11)
        self.assertEqual(v.as_tuple(), (10, 11))
        self.assertEqual(v[0], 10)
        self.assertEqual(v[1], 11)

    def test_Vector2D_addition(self):
        v1 = Vector2D(10, 11)
        v2 = Vector2D(4, 33)
        self.assertEqual((v1 + v2).as_tuple(), (14, 44))

    def test_BoundingBox(self):
        box = BoundingBox(-2, 4, 5, 3)
        self.assertEqual(box.left, -2)
        self.assertEqual(box.upper, 4)
        self.assertEqual(box.right, 5)
        self.assertEqual(box.lower, 3)

    def test_BoundingBox_reverse_points(self):
        box = BoundingBox(5, 3, -2, 4)
        self.assertEqual(box.left, -2)
        self.assertEqual(box.upper, 4)
        self.assertEqual(box.right, 5)
        self.assertEqual(box.lower, 3)

    def test_BoundingBox_add_bbox(self):
        box1 = BoundingBox(10, 23, 32, 15)
        box2 = BoundingBox(-2, 4, -1, 3)
        self.assertEqual((box1 + box2).as_tuple(), (-2, 23, 32, 3))

    def test_BoundingBox_add_vector(self):
        box1 = BoundingBox(-1, 1, 1, -1)
        v = Vector2D(3, 5)
        self.assertEqual((box1 + v).as_tuple(), (2, 6, 4, 4))

    def test_BoundingBox_add_fails(self):
        box1 = BoundingBox(-1, 1, 1, -1)
        self.assertRaises(TypeError, lambda: box1 + 4)

    def test_BoundingBox_contains(self):
        box1 = BoundingBox(-2, 23, 32, 3)
        box2 = BoundingBox(-2, 4, -1, 3)
        self.assertTrue(box1.contains(box2))

    def test_BoundingBox_padded(self):
        box = BoundingBox(-2, 23, 32, 3)
        box = box.padded(1)
        self.assertEqual(box.as_tuple(), (-3, 24, 33, 2))

    def test_BoundingBox_transform(self):
        box = BoundingBox(-1, 1, 1, -1)
        box = box.transform(Vector2D(3, 5))
        self.assertEqual(box.as_tuple(), (2, 6, 4, 4))

    def test_BoundingBox_size(self):
        box = BoundingBox(-1, -3, -3, -1)
        self.assertEqual(box.width(), 2)
        self.assertEqual(box.height(), 2)


if __name__ == "__main__":
    main()
