from pygerber.builder.gerber import GerberX3Builder


builder = GerberX3Builder()

d10 = builder.new_pad().circle(diameter=0.5)

pad_0 = builder.add_pad(d10, (0, 0))
pad_1 = builder.add_pad(d10, (2, 1))

trace_0 = builder.add_trace(0.1, pad_0, (0, 1))
builder.add_trace(0.1, trace_0, pad_1)


code = builder.get_code()
print(code.dumps())
