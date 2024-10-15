from pygerber.builder.gerber import GerberX3Builder


builder = GerberX3Builder()

region = (
    builder.new_region((-2, 0))
    .add_line((-2, 2))
    .add_line((0, 2))
    .add_line((1, 1))
    .add_line((0, 0))
    .create()
)

code = builder.get_code()
print(code.dumps())
