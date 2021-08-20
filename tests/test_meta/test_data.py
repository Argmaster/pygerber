from pygerber.meta.data import BoundingBox, Vector2D
from unittest import TestCase, main


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

    def test_BoundingBox_add(self):
        box1 = BoundingBox(10, 23, 32, 15)
        box2 = BoundingBox(-2, 4, -1, 3)
        self.assertEqual((box1 + box2).as_tuple(), (-2, 23, 32, 3))

    def test_BoundingBox_contains(self):
        box1 = BoundingBox(-2, 23, 32, 3)
        box2 = BoundingBox(-2, 4, -1, 3)
        self.assertTrue(box1.contains(box2))

    def test_BoundingBox_pad(self):
        box = BoundingBox(-2, 23, 32, 3)
        box.pad(1)
        self.assertEqual(box.as_tuple(), (-3, 24, 33, 2))




if __name__ == "__main__":
    main()
