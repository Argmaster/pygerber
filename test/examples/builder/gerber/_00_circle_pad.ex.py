from pygerber.builder.gerber import GerberX3Builder


builder = GerberX3Builder()

d10 = builder.new_pad().circle(diameter=0.5)
builder.add_pad(d10, (2, 1))

code = builder.get_code()
print(code.dumps())
