from nm_c import __version__
from nm_c.some_func import func_c


def test_version():
    assert __version__ >= "0.0.0"


def test_func_a():
    assert func_c() is None
