# Internal Execution Model

PyGerber divides the processing of a Gerber file into three stages. The first of them is
Tokenization during which the source code is broken into short characteristic fragments
called tokens. The tokens are then passed to a parser which converts them into drawing
operations. These eventually go to one of the Backends to create a resulting
visualization that can be saved.

```mermaid
flowchart TD
    source_code([Gerber source code])

    tokenizer([Tokenizer])

    token_stream("`
    CoordinateFormat(...)
    Comment(...)
    Comment(...)
    UnitMode(...)
    LoadPolarity(...)
    Comment(...)
    ApertureAttribute(...)
    ...
    `")

    parser([Parser])

    draw_commands("`
    Rasterized2DDrawPaste(...)
    Rasterized2DDrawVectorLine(...)
    Rasterized2DDrawPaste(...)
    Rasterized2DDrawPaste(...)
    Rasterized2DDrawVectorLine(...)
    Rasterized2DDrawPaste(...)
    Rasterized2DDrawPaste(...)
    Rasterized2DDrawVectorLine(...)
    Rasterized2DDrawPaste(...)
    Rasterized2DDrawPaste(...)
    Rasterized2DDrawVectorLine(...)
    `")

    backend(["Backend, eg. Rasterized2DBackend"])

    output([Output image/model])

    handle([ResultHandle])

    source_code --> tokenizer
    tokenizer -- "tokenizer.tokenize()" --> token_stream
    token_stream --> parser
    parser -- "parser.parse()" --> draw_commands
    draw_commands --> backend
    backend -- "draw_commands.draw()" --> handle
    handle -- "handle.save()" --> output
```
