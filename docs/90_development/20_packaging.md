# Package

Since PyGerber is a pure Python package, there is nothing to compile and there is no
special build step before packaging.

To build PyGerber `wheel` or `sdist` package from source you have to first set up
development environment as described in [Environment setup](./10_env_setup.md) section.
After completing initial setup of development environment, you should have
[poetry](https://pypi.org/project/poetry/) installed on your system. To build both wheel
and source distribution packages, use following command:

```
poetry build
```

Check `dist` directory within current working directory, `pygerber-x.y.z.tar.gz` and
`pygerber-x.y.z-py3-none-any.whl` files should be present there. You can use `pip` to
directly install them:

!!! warning

    Replace `x.y.z` with actual version number.

```
pip install dist/pygerber-x.y.z.tar.gz
```
