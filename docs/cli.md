# PyGerber CLI

**CLI** offers You two ways of rendering

-   single-file, when You have to specify path to file and colors to use
-   multi-file, based on specfile, it renders multiple layers and joins them into one image



### Getting help

To request help, use good old `--help` or `-h`

```bash
$ python -m pygerber -h
```
### Specifying rendering engine
All rendering commands require You to specify rendering engine:
- Pillow for 2D, using `--pillow` or `-p`
- Blender for 3D, using `--blender` or `-b`

### Rendering single file
Single-file mode requires You to pass `--file` flag, followed by path to gerber file You want to render. You can optionally provide `--colors` flag followed by one of predefined color set names, see them in [`specfile.md`](https://github.com/Argmaster/pygerber/blob/main/examples/specfile.md).
```bash
$ python -m pygerber --pillow --file "tests/gerber/s5.grb" -s "render.png"
Rendering D:\dev\pygerber\tests\gerber\s5.grb as FILE
Saving to D:\dev\pygerber\render.png
Successfully saved image 1006x887, 6.9 KiB.
```


### Rendering multiple files

Multi-file mode allows You to use all three specfile formats: **JSON**, **YAML** and **TOML**. For more information about what specfile should contain, see [`specfile.md`](https://github.com/Argmaster/pygerber/blob/main/examples/specfile.md). You can specify specfile path and format via one of `--json` `--yaml` `--toml` followed by `file path`

```bash
$ python -m pygerber --pillow --toml "tests/gerber/pillow/specfile.toml" -s "render.png"
Rendering ...\tests\gerber\pillow\specfile.toml as TOML
Saving to ...\render.png
Successfully saved image 1398x711, 28.0 KiB.
```
