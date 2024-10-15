from pygerber.builder.gerber import GerberX3Builder


builder = GerberX3Builder()

d10 = builder.new_pad().circle(diameter=0.5)
builder.add_pad(d10, (2, 1))
builder.add_line_trace(0.1, (0, 0), (0, 1))
builder.add_line_trace(0.1, (0, 1), (2, 1))

code = builder.get_code()
print(code.dumps())
