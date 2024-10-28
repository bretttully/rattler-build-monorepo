from nm_b import __version__
from nm_b.some_func import func_b


def test_version():
    assert __version__ >= "0.0.0"


def test_func_b():
    assert func_b() is None
