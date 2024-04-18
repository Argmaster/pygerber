# Usage

## Introduction

Since release 2.2.0 PyGerber offers interface designed for Gerber code introspection
based on `Parser2` class and
[visitor pattern](https://refactoring.guru/design-patterns/visitor). API is build around
`Parser2HooksBase` class from `pygerber.gerberx3.parser2.parser2hooks_base` module and
descendant classes passed to `Parser2` class. `Parser2` visits all tokens in Gerber AST
created by `Tokenizer` and invokes particular hooks from provided hooks class.
`Parser2HooksBase` itself doesn't implement any Gerber specific behaviors. It is just a
collection of classes with empty hook methods which can be used to implement behaviors
explained in
[The Gerber Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=71).
PyGerber provides such implementation in form of `Parser2Hooks` class, available in
`pygerber.gerberx3.parser2.parser2` module.

## Minimal example

Let's consider very simple example in which we are interested in extracting all comments
from Gerber code. Of course for such task it would be just enough to use regular
expressions, but thanks to simplicity of this task it will be easier to perceive how
hooks work.

```py linenums="1" title="test/examples/introspect_minimal_example.py"
{% include 'test/examples/introspect_minimal_example.py' %}
```

As you can see in snippet above, to inject custom hooks class one must create nested
options structure. Design decision to nest configuration like this, was made to allow
maximal customization of all parts of the `Parser2`. Indeed at each level there are few
options useful in specific situations. But as for now, let's focus on hooks themselves.

It's important to notice that hook method `on_parser_visit_token()` is overrode in
nested class, `CommentTokenHooks`, which inherits from `Parser2Hooks`. There are hooks
which are defined directly in hooks class, but they are more general, eg. for handling
exceptions. All hooks specific to particular tokens are defined in nested classes named
in way indicating what token they are concerned with, eg.
`DefineApertureObroundTokenHooks`, `ImagePolarityTokenHooks`.

Output of this code will look like this:

```log
 Ucamco ex. 2: Shapes
 A comment
 Ucamco ex. 2: Shapes
 Comment
 Units are mm
 Format specification:
  Leading zeros omitted
  Absolute coordinates
  Coordinates in 3 integer and 6 fractional digits.
 Attribute: the is not a PCB layer, it is just an
 example
 Define Apertures
 Comment
 Define the aperture macro 'THERMAL80'
 Use thermal primitive in the macro
 Define aperture 10 as a circle with diameter 0.1 mm
 Define aperture 11 as a circle with diameter 0.6 mm
 Define aperture 12 as a rectangle with size 0.6 x 0.6 mm
 Define aperture 13 as a rectangle with size 0.4 x 1 mm
 Define aperture 14 as a rectangle with size 1 x 0.4 mm
 Define aperture 15 as an obround with size 0.4 x 1 mm
 Define aperture 16 as a polygon with 3 vertices and
 circumscribed circle with diameter 1 mm
 Define aperture 19 as an instance of macro aperture
 'THERMAL80' defined earlier
 Start image generation
 A comment
 Select aperture 10 as current aperture
 Set the current point to (0, 2.5) mm
 Set linear plot mode
 Create draw with the current aperture
 Create draw with the current aperture
 Set the current point
 Create draw with the current aperture
 Create draw with the current aperture
 Set the current point.
 Create draw with the current aperture
 Select aperture 11 as current aperture
 Create flash with the current aperture (11) at (10, 10).
 Create a flash with the current aperture at (20, 10).
```

Notice that every line starts with one space, as everything directly after G04 statement
is considered a comment, including leading spaces.

## Mixed inheritance

By default `Parser2` is using `Parser2Hooks`, however, for some use cases it may be more
beneficial to use `Parser2HooksBase` class to reduce time required to traverse single
Gerber file. This is the case when one needs only selected Gerber features, eg.
attribute support. In such case, you can create new `Parser2HooksBase` derived class and
for some hook classes inherit from `Parser2Hooks` nested classes.

For example let's assume we want to extract attributes of all apertures in Gerber file.
To do it we need a working attribute cumulation logic, but at the same time let's try to
minimize time required to parse file by using only these parts of Parser2Hooks which are
necessary.

```py linenums="1" title="test/examples/introspect_mixed_inheritance.py"
{% include 'test/examples/introspect_mixed_inheritance.py' %}
```

Output of this code will look like this:

```log
D10
ApertureAttributes({'.AperFunction': 'EtchedComponent'})
D11
ApertureAttributes({'.AperFunction': 'EtchedComponent'})
D12
ApertureAttributes({'.AperFunction': 'ComponentPad'})
D13
ApertureAttributes({'.AperFunction': 'ComponentPad'})
```

Beware that there are some potential risks when using such approach. Tokens often rely
on other tokens defined before them (eg. `CoordinateFormat` relies on `UnitMode`). For
example in this case we can't inherit from
`Parser2Hooks.DefineApertureCircleTokenHooks`, as we are not including implementation of
`UnitModeTokenHooks`, so define would complain about draw units not being set, by
throwing `pygerber.gerberx3.parser2.errors2.UnitNotSet2Error`.

## Error handling

Parser2 hooks provide a way to handle errors before they are propagated to Parser2 and
cause parse interruption. However, to enable this behavior one must explicitly enable it
by setting `on_update_drawing_state_error` parameter to `Parser2OnErrorAction.UseHook`.

```python
Parser2(
    Parser2Options(
        context_options=Parser2ContextOptions(hooks=hooks),
        on_update_drawing_state_error=Parser2OnErrorAction.UseHook,
    ),
)
```

This option gives parser a chance to recover from error by passing it to one of two
hooks: `on_parser_error()` on `on_other_error()`. First one is used to handle exceptions
are not descendants of `pygerber.gerberx3.parser2.errors2.Parser2Error`, which are
expected to be thrown by parser related code, mostly when encountering unrecoverable
Gerber standard violations. They are "unrecoverable" in a sense that we can't make a
good general assumption what should we do with it.
`pygerber.gerberx3.parser2.errors2.UnitNotSet2Error` is an example of such an error,
raised when attempting to interpret Gerber coordinates before unit of distance was set
(inch/millimeter), which leaves units as undefined and neither inch nor millimeter is a
good default in general case, but one of them can be a good default in some specific
environments.

```py linenums="1" title="test/examples/introspect_handle_no_unit.py"
{% include 'test/examples/introspect_handle_no_unit.py' %}
```
