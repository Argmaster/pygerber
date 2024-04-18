# Build from source

To build PyGerber from source You have to set up [Development](#development) environment
first. Make sure you have `poetry` environment activated with:

```
poetry shell
```

With environment active it should be possible to build wheel and source distribution
with:

```
poetry build
```

Check `dist` directory within current working directory, `pygerber-x.y.z.tar.gz` and
`pygerber-x.y.z-py3-none-any.whl` should be there.
