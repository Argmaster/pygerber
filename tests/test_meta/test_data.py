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
        box = BoundingBox((-2, 4), (-1, 3))
        self.assertEqual(box.left_x, -2)
        self.assertEqual(box.top_y, 3)
        self.assertEqual(box.right_x, 4)
        self.assertEqual(box.bottom_y, -1)

    def test_BoundingBox_add(self):
        box1 = BoundingBox((10, 23), (32, 15))
        box2 = BoundingBox((-2, 4), (-1, 3))
        #self.assertEqual((box1 + box2).as_tuples(), ((-2, 4), (-2, -1)))


if __name__ == "__main__":
    main()
