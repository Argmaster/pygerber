from pygerber.builder.gerber import GerberX3Builder


builder = GerberX3Builder()

d10 = (
    builder.new_pad()
    .custom()
    .add_circle(0.2, (1, 1))
    .add_circle(0.2, (-1, 1))
    .add_circle(0.2, (1, -1))
    .add_circle(0.2, (-1, -1))
    .add_vector_line(0.15, (1, 1), (-1, -1))
    .add_vector_line(0.15, (-1, 1), (1, -1))
    .create()
)
builder.add_pad(d10, (0, 0))
builder.add_pad(d10, (3, 0))
builder.add_pad(d10, (6, 0))

code = builder.get_code()
print(code.dumps())
