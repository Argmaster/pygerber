from pygerber.builder.gerber import GerberX3Builder


builder = GerberX3Builder()

d10 = (
    builder.new_pad()
    .custom()
    # Top right corner
    .add_vector_line(0.1, (0.5, 1.5), (1.5, 1.5))
    .add_vector_line(0.1, (1.5, 1.5), (1.5, 0.5))
    .add_circle(0.1, (1.5, 1.5))  # Corner
    # Bottom right corner
    .add_vector_line(0.1, (0.5, -1.5), (1.5, -1.5))
    .add_vector_line(0.1, (1.5, -1.5), (1.5, -0.5))
    .add_circle(0.1, (1.5, -1.5))  # Corner
    # Bottom left corner
    .add_vector_line(0.1, (-0.5, -1.5), (-1.5, -1.5))
    .add_vector_line(0.1, (-1.5, -1.5), (-1.5, -0.5))
    .add_circle(0.1, (-1.5, -1.5))
    # Top left corner
    .add_vector_line(0.1, (-0.5, 1.5), (-1.5, 1.5))
    .add_vector_line(0.1, (-1.5, 1.5), (-1.5, 0.5))
    .add_circle(0.1, (-1.5, 1.5))  # Corner
    .create()
)
builder.add_pad(d10, (0, 0))
builder.add_pad(d10, (4, 0))
builder.add_pad(d10, (8, 0))

code = builder.get_code()
print(code.dumps())
